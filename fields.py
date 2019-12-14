base = ('id', 'date_create', 'date_update', 'update_by', )
modeluid = ('uid',)
image = ('image',)
display = ('display',)
tosearch = ('to_search',)
signhash = ('signhash',)
disable = ('is_disable',)
alert = ('alerts',)
error = ('errors',)
files = ('the_file', 'mimetype', 'file_name')
full = base + modeluid + display + tosearch + signhash + disable + alert + error

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