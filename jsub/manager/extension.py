import os
import logging

from jsub.manager.error import ExtensionNotFoundError
from jsub.config        import ConfigFileNotFoundError

from jsub.loader import load_class, module_dir
from jsub.loader import LoadError

from jsub.config import find_and_load_config_file
from jsub.util   import snake_to_camel


class ExtensionManager(object):
    def __init__(self, exts):
        self.__exts = exts

        self.__logger = logging.getLogger('JSUB')

    def load_ext(self, category, ext_name, *args, **kwargs):
        class_name = snake_to_camel(ext_name)
        for ext in self.__exts:
            module_name = '.'.join([ext, category, ext_name])
            try:
                c = load_class(module_name, class_name)
                return c(*args, **kwargs)
            except LoadError:
                pass
        raise ExtensionNotFoundError('Extension "%s:%s" could not be found and loaded' % (category, ext_name))

    def load_ext_common(self, category, load_data):
        if 'type' not in load_data:
            raise ExtensionNotFoundError('Could not load extension without "type" specified')
        return self.load_ext(category, load_data['type'], load_data.get('param', {}))

    def ext_dir(self, category, ext_name):
        for ext in self.__exts:
            try:
                ext_root = module_dir(ext)
                ext_dir_temp = os.path.join(ext_root, category, ext_name)
                if os.path.isdir(ext_dir_temp):
                    return ext_dir_temp
            except LoadError:
                pass

        raise ExtensionNotFoundError('Extension directory "%s:%s" could not be found' % (category, ext_name))

    def ext_config(self, category, ext_name, config_name):
        try:
            return find_and_load_config_file(self.ext_dir(category, ext_name), config_name)
        except ConfigFileNotFoundError as e:
            self.__logger.debug('Extension config not found, use empty config')
            return {}
