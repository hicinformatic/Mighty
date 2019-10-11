from django.conf import settings
from mighty.functions import logger
from mighty.apps.authenticate.backends import TwoFactorBackend
from mighty.apps.authenticate import _
from mighty.models import authenticate as models
from mighty.apps.authenticate.models import STATUS_PREPARE, STATUS_SENT, STATUS_RECEIVED
import requests, json

class SendinblueBackend(TwoFactorBackend):
    def send_sms(self, user, backend_path):
        code = user.get_code()
        sms = _.tpl_txt %(settings.TWOFACTOR["site"], code)
        url = "https://api.sendinblue.com/v3/transactionalSMS/sms"
        payload = {
            "sender": settings.TWOFACTOR["sender_name"],
            "recipient": user.phone, 
            "content": sms,
            "type": "transactional"
        }
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'api-key': settings.SENDINBLUE['api-key']
        }
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        logger('authenticate', 'info', response.text)
        sms = models.Sms(user=user, sms=sms, response=response.text, backend=backend_path)
        sms.save()
        return True

    def check_sms(self, sms):
        response = json.loads(sms.response)
        if 'messageId' in response:
            messageid = response['messageId']
            url = "https://api.sendinblue.com/v3/transactionalSMS/statistics/events?limit=1"
            querystring = {"messageId": messageid}
            headers = {
                'accept': "application/json",
                'api-key': settings.SENDINBLUE['api-key']
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            logger('authenticate', 'info', response.text)
            response = json.loads(response.text)
            response = response['events'].pop()
            if response['event'] in [ 'sent', ]:
                sms.status = STATUS_SENT
            elif response['event'] in [ 'delivered', 'accepted', 'replies']:
                sms.status = STATUS_RECEIVED
            else:
                sms.error('status', response)
            sms.save()
        return response

    def send_email(self, user, backend_path):
        code = user.get_code()
        subject = _.tpl_subject % settings.TWOFACTOR["site"]
        html = _.tpl_html %(settings.TWOFACTOR["site"], code)
        txt = _.tpl_txt %(settings.TWOFACTOR["site"], code)
        url = 'https://api.sendinblue.com/v3/smtp/email'
        payload = {
            "sender": {
                "email": settings.TWOFACTOR["sender_email"],
                "name": settings.TWOFACTOR["sender_name"],
            },
            "to": [{"email": user.email,},],
            "replyTo": {
                "email": settings.TWOFACTOR["reply_email"],
                "name": settings.TWOFACTOR["reply_name"],
            },
            "subject": subject,
            "htmlContent": html,
            "textContent": txt,
        }
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'api-key': settings.SENDINBLUE['api-key']
        }
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        email = models.Email(user=user, subject=subject, html=html, txt=txt, response=response.text, backend=backend_path)
        logger('authenticate', 'info', response.text)
        email.save()
        return True

    def check_email(self, email):
        response = json.loads(email.response)
        if 'messageId' in response:
            messageid = response['messageId']
            url = "https://api.sendinblue.com/v3/smtp/statistics/events"
            querystring = {"messageId": messageid}
            headers = {
                'accept': "application/json",
                'api-key': settings.SENDINBLUE['api-key']
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            logger('authenticate', 'info', response.text)
            response = json.loads(response.text)
            if 'events' in response:
                response = response['events'].pop()
                if response['event'] in [ 'requests', ]:
                    email.status = STATUS_SENT
                elif response['event'] in [ 'delivered', 'opened', 'clicks']:
                    email.status = STATUS_RECEIVED
                else:
                    email.error('status', response)
                email.save()
        return response