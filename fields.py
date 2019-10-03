notsignhash = (
    'id',
    'uid',
    'logentry',
    'display',
    'is_disable',
    'to_search',
    'date_create',
    'date_update',
    'update_by',
    'signhash',
    'initials',
    'alerts',
    'errors',
)

notsignhash = (
    'id',
    'uid',
    'to_search',
    'is_disable',
    'date_create',
    'date_update',
    'update_by',
    'signhash',
    'alerts',
    'errors',
    'related_data',
)

readonly_fields = (
    'id',
    'uid',
    'to_search',
    'is_disable',
    'date_create',
    'date_update',
    'update_by',
    'signhash',
    'alerts',
    'errors',
)

list_display = ('__str__', 'is_disable')
list_filter = ('is_disable',)
search_fields = ('display', 'signhash',)