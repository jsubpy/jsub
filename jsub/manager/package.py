import logging

from jsub.error import JsubError

from jsub.loader import package_dir
from jsub.loader import LoadError

from jsub.config import find_and_load_config_file
from jsub.config import ConfigFileNotFoundError

from jsub.util import ensure_list
from jsub.util import unique_list


class PackageNotFoundError(JsubError):
    pass


PACKAGE_CONFIG_NAME = 'config'

def _package_config(package):
    try:
        pkg_dir = package_dir(package)
        return find_and_load_config_file(pkg_dir, PACKAGE_CONFIG_NAME)
    except LoadError as e:
        raise PackageNotFoundError('Package "%s" not found: %s' % (package, e))
    except ConfigFileNotFoundError as e:
        return {}


class PackageManager(object):
    def __init__(self, schema_mgr, initial_packages):
        self.__schema_mgr = schema_mgr
        self.packages_config = {}

        self.__logger = logging.getLogger('JSUB')

        self.__resolve_packages(initial_packages)

    def __package_deps(self, packages):
        pkgs = []
        for pkg in packages:
            pkgs.append(pkg)
            pkg_config = _package_config(pkg)
            pkg_config = self.__schema_mgr.validate_package_config(pkg_config)
            if 'package' in pkg_config:
                sub_pkgs = ensure_list(pkg_config['package'])
                pkgs.append(self.__package_deps(sub_pkgs))
            self.packages_config[pkg] = pkg_config
        return unique_list(pkgs)

    def __resolve_packages(self, initial_packages):
        self.packages = self.__package_deps(initial_packages)



