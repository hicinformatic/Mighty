from django.conf import settings
from django.utils._os import safe_join
from django.utils.module_loading import import_string
Storage = import_string(settings.STORAGE)

import os

class CloudStorage(Storage):
    def _save_backup(self, name, content):
        content.seek(0)

        filename = "%s/%s" % (settings.MEDIA_ROOT, name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as bacfile:
            while True:
                buf=content.read(1024)
                if buf: 
                    for byte in buf:
                        pass    # process the bytes if this is what you want
                                # make sure your changes are in buf
                    n=bacfile.write(buf)
                else:
                    break

    def _save(self, name, content, headers=None):
        original_name = super(CloudStorage, self)._save(name, content, headers=None)
        self._save_backup(name, content)
        return original_name

    def remove_dir(self, name):
        dirname = os.path.dirname(name)
        while not os.listdir(dirname):
            os.rmdir(name)
            dirname = os.path.join(os.path.split(dirname)[:-1])


    def delete_backup(self, name):
        name = "%s/%s" % (settings.MEDIA_ROOT, name)
        assert name, "The name argument is not allowed to be empty."
        name = os.path.realpath(name)
        try:
            if os.path.isdir(name):
                os.rmdir(name)
            else:
                os.remove(name)
        except FileNotFoundError:
            pass

    def delete(self, name):
        super(CloudStorage, self).delete(name)
        self.delete_backup(name)
