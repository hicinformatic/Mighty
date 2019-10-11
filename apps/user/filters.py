from mighty.filters import Filter
from mighty.models.user import User

def UserFilter(view, request):
    UserFilter = Filter(request, User)
    UserFilter.add("search", "to_search")
    UserFilter.add("search", "username")
    UserFilter.add("search", "email")
    UserFilter.add("search", "last_name")
    UserFilter.add("search", "first_name")
    return UserFilter.get()

#def UserExtendFilter(request):
#    UserExtendFilter = Filter(request, models.UserExtend)
#    UserExtendFilter.add("search", "value")
#    UserExtendFilter.add("search", "to_search")
#    UserExtendFilter.add("search", "field__name")
#    UserExtendFilter.add("search", "parent__to_search")
#    UserExtendFilter.add("search", "parent__username")
#    UserExtendFilter.add("search", "parent__email")
#    UserExtendFilter.add("search", "parent__last_name")
#    UserExtendFilter.add("search", "parent__first_name")
#    return UserExtendFilter.get()
#
#def UserHistoryFilter(request):
#    UserHistoryFilter = Filter(request, models.UserHistory)
#    UserHistoryFilter.add("search", "value")
#    UserHistoryFilter.add("search", "to_search")
#    UserHistoryFilter.add("search", "field__name")
#    UserHistoryFilter.add("search", "parent__to_search")
#    UserHistoryFilter.add("search", "parent__username")
#    UserHistoryFilter.add("search", "parent__email")
#    UserHistoryFilter.add("search", "parent__last_name")
#    UserHistoryFilter.add("search", "parent__first_name")
#    return UserHistoryFilter.get()