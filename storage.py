from django.conf import settings
from django.utils._os import safe_join
from django.utils.module_loading import import_string
import os

Storage = import_string(settings.STORAGE)

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
                        pass
                    n=bacfile.write(buf)
                else:
                    break

    def _save(self, name, content, headers=None):
        original_name = super(CloudStorage, self)._save(name, content, headers=None)
        self._save_backup(name, content)
        return original_name

    def remove_dir(self, name):
        dirname = os.path.dirname(name)
        level = 1
        if os.path.isdir(dirname):
            while not os.listdir(dirname):
                if level <= 5:
                    os.rmdir(dirname)
                    dirname = os.path.dirname(dirname)
                    level += 1
                else:
                    break

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
        self.remove_dir(name)

    def delete(self, name):
        super(CloudStorage, self).delete(name)
        self.delete_backup(name)