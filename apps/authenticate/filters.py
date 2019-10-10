from mighty.filters import Filter
from mighty.apps.authenticate import models

def SmsFilter(request):
    SmsFilter = Filter(request, models.SMS)
    SmsFilter.add("search", "user__to_search")
    SmsFilter.add("search", "user__username")
    SmsFilter.add("search", "user__email")
    SmsFilter.add("search", "user__last_name")
    SmsFilter.add("search", "user__first_name")
    SmsFilter.add("search", "user__codes")
    SmsFilter.add("search", "html")
    SmsFilter.add("search", "txt")
    return SmsFilter.get()

def EmailFilter(request):
    EmailFilter = Filter(request, models.SMS)
    EmailFilter.add("search", "user__to_search")
    EmailFilter.add("search", "user__username")
    EmailFilter.add("search", "user__email")
    EmailFilter.add("search", "user__last_name")
    EmailFilter.add("search", "user__first_name")
    EmailFilter.add("search", "user__codes")
    EmailFilter.add("search", "html")
    EmailFilter.add("search", "txt")
    return EmailFilter.get()