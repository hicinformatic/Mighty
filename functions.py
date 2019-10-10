from django.utils.six.moves import input
from mighty.apps import MightyConfig
from Crypto import Cipher, Random
import base64, datetime, string, random, unicodedata, re

BS = MightyConfig.Crypto.BS
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def test(input_str=None):
    return True if str(input_str).strip().lower().replace(' ', '') not in MightyConfig.Test.search else False

def key(size=32):
    return ''.join(random.choice(string.hexdigits) for x in range(size))

def randomcode(stringLength):
    letters = "123456789"
    return ''.join(random.choice(letters).upper() for i in range(stringLength))

def encrypt(key, raw):
    raw = pad(raw)
    iv = Random.new().read(Cipher.AES.block_size)
    cipher = Cipher.AES.new(key, Cipher.AES.MODE_CFB, iv)
    return base64.b64encode(iv+cipher.encrypt(raw)) 

def decrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = Cipher.AES.new(key, Cipher.AES.MODE_CFB, iv)
    return unpad(cipher.decrypt(enc[16:]))

def boolean_input(question, default='n'):
    result = input("%s " % question)
    while len(result) < 1 or result[0].lower() not in "yn":
        result = input("Please answer yes(y) or no(n), default(%s): " % default)
    return result[0].lower() == 'y'

def make_searchable(input_str):
    for i in MightyConfig.Test.replace:
        input_str = input_str.replace(i, ' ')
    input_str = re.sub(" +", " ", input_str)
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def image_directory_path(instance, filename):
    directory = str(instance.__class__.__name__).lower()
    date = datetime.datetime.now()
    ext = filename.split('.')[-1:]
    return "{0}/{1}/{2}/{3}.{4}".format(directory, date.year, date.month, instance.uid, ext)

#0 	Emergency 	  emerg (panic)	 Système inutilisable.
#1 	Alert 	      alert          Une intervention immédiate est nécessaire.
#2 	Critical 	  crit 	         Erreur critique pour le système.
#3 	Error 	      err (error) 	 Erreur de fonctionnement.
#4 	Warning 	  warn (warning) Avertissement (une erreur peut intervenir si aucune action n'est prise).
#5 	Notice 	      notice  	     Evénement normal méritant d'être signalé.
#6 	Informational info 	         Pour information.
#7 	Debugging 	  debug 	     Message de mise au point.
def logger(app, lvl, msg, user=None):
    code = getattr(MightyConfig.Log, MightyConfig.Log.format_code.format(lvl))
    if code <= MightyConfig.Log.log_level:
        if user is not None:
            msg = MightyConfig.Log.format_user.format(user.username, user.id, msg)
        if MightyConfig.Log.log_type == 'syslog':
            logger_syslog(app, lvl, code, msg)
        elif MightyConfig.Log.log_type == 'file':
            logger_file(app, lvl, code, msg)
        else:
            logger_console(app, lvl, code, msg)

def logger_syslog(app, lvl, code, msg):
    syslog.openlog(logoption=syslog.LOG_PID)
    syslog.syslog(code, MightyConfig.Log.format_syslog.format(app, msg))
    syslog.closelog()

def logger_file(app, lvl, code, msg):
    now = datetime.datetime.now()
    logfile = MightyConfig.Log.name_file.format(MightyConfig.Directory.logs, app, now.year, now.month, now.day)
    log = open(logfile, MightyConfig.Log.file_open_method)
    log.write(MightyConfig.Log.format_file.format(now.hour, now.minute, now.second, now.microsecond, lvl, app, msg))
    log.close()

def logger_console(app, lvl, code, msg):
    color = getattr(MightyConfig.Log, MightyConfig.Log.format_color.format(lvl))
    now = datetime.datetime.now()
    print(MightyConfig.Log.format_console.format(color, now.hour, now.minute, now.second, now.microsecond, lvl, app, msg, MightyConfig.Log.default_color))