import re
import importlib
import inspect

def camel_to_lower(name):
    return name.lower()

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class ModuleNotFoundError(Exception):
    pass

class ClassNotFoundError(Exception):
    pass

class NotAClassError(Exception):
    pass


class Loader:
    def __init__(self, extensions):
        self.__extensions = extensions

    def load_module(self, category, module_name):
        m = None
        for ext in self.__extensions:
            name = '.'.join([ext, category, module_name])
            try:
                m = importlib.import_module(name)
                break
            except ImportError as e:
                print(':::::::::::::: %s' % e)
                continue

        if m is None:
            raise ModuleNotFoundError('Module "%s" of category "%s" could not be found' % (module_name, category))
        return m

    def load_class(self, category, class_name, module_name = ''):
        m_name = module_name
        if not m_name:
            m_name = camel_to_snake(class_name)
        m = self.load_module(category, m_name)

        try:
            c = getattr(m, class_name)
        except:
            raise ClassNotFoundError('Class "%s" of category "%s" not found in module "%s"' % (class_name, category, module_name))

        if not inspect.isclass(c):
            raise NotAClassError('"%s" in module "%s" is not a class' % (class_name, module_name))

        return c

    def load_instance(self, category, class_name, module_name = ''):
        return self.load_class(category, class_name, module_name)()
