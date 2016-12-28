import os

from jsub.error import JsubError

from jsub.loader import load_class, module_dir
from jsub.loader import LoadError

from jsub.util import snake_to_camel


class ExtensionNotFoundError(JsubError):
    pass


class ExtensionManager(object):
    def __init__(self, exts):
        self.__exts = exts

    def load_ext(self, category, ext_name, *args, **kwargs):
        class_name = snake_to_camel(ext_name)
        for ext in self.__exts:
            module_name = '.'.join([ext, category, ext_name])
            try:
                c = load_class(module_name, class_name)
                return c(*args, **kwargs)
            except LoadError as e:
                pass
        raise ExtensionNotFoundError('Extension "%s:%s" could not be found and loaded' % (category, ext_name))

    def load_ext_common(self, category, load_data):
        if 'type' not in load_data:
            raise Exte
        return self.load_ext(category, load_data['type'], load_data.get('param', {}))

    def ext_dir(self, category, ext_name):
        for ext in self.__exts:
            try:
                ext_root = module_dir(ext)
                ext_dir_temp = os.path.join(ext_root, category, ext_name)
                if os.path.isdir(ext_dir_temp):
                    return ext_dir_temp
            except LoadError as e:
                pass

        raise ExtensionNotFoundError('Extension directory "%s:%s" could not be found' % (category, ext_name))
