base = ('id', 'date_create','date_update','update_by',)
modeluid = ('uid',)
image = ('image',)
display = ('display',)
tosearch = ('to_search',)
signhash = ('signhash',)
disable = ('is_disable',)
alert = ('alerts',)
error = ('errors',)
full = base + modeluid + image + display + tosearch + signhash + disable + alert + error

readonly_fields =  base + modeluid + tosearch + signhash + disable + alert + error
list_display = display + disable
list_filter = disable
search_fields = display + tosearch

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