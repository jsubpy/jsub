import pytest

import os
import sys

from jsub.manager.extension import ExtensionManager
from jsub.manager.error     import ExtensionNotFoundError

@pytest.fixture(scope='module', autouse=True)
def setup_python_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    loader_path = os.path.join(current_path, 'fixtures', 'packages', 'loader')
    load_path1 = os.path.join(loader_path, 'load1')
    load_path2 = os.path.join(loader_path, 'load2')
    sys.path.insert(0, load_path1)
    sys.path.insert(0, load_path2)
    yield
    sys.path.remove(load_path2)
    sys.path.remove(load_path1)

@pytest.fixture(scope='module')
def ext_mgr():
    return ExtensionManager(['jsub_ext1', 'jsub_ext2', 'jsub_ext3'])


def test_load_instances(ext_mgr):
    i = ext_mgr.load_ext('repo', 'file_system')
    assert i.desc == 'load1: jsub_ext1.repo.file_system.FileSystem'
    i = ext_mgr.load_ext('repo', 'sqlite')
    assert i.desc == 'load2: jsub_ext3.repo.sqlite.Sqlite'
    i = ext_mgr.load_ext('backend', 'condor')
    assert i.desc == 'load1: jsub_ext2.backend.condor.Condor'
    i = ext_mgr.load_ext('backend', 'pbs')
    assert i.desc == 'load1: jsub_ext2.backend.pbs.Pbs'
    i = ext_mgr.load_ext('backend', 'dirac')
    assert i.desc == 'load2: jsub_ext3.backend.dirac.Dirac'


def test_load_not_existed_module(ext_mgr):
    with pytest.raises(ExtensionNotFoundError):
        ext_mgr.load_ext('backend', 'UnknownClass')
    with pytest.raises(ExtensionNotFoundError):
        ext_mgr.load_ext('backend', 'Condor', 'unknown_module')

def test_load_not_existed_class(ext_mgr):
    with pytest.raises(ExtensionNotFoundError):
        ext_mgr.load_ext('backend', 'UnknownClass', 'condor')
    with pytest.raises(ExtensionNotFoundError):
        ext_mgr.load_ext('repo', 'Empty')
    with pytest.raises(ExtensionNotFoundError):
        ext_mgr.load_ext('backend', 'ClassWithAnotherName', 'condor')

def test_load_not_a_class(ext_mgr):
    with pytest.raises(ExtensionNotFoundError):
        ext_mgr.load_ext('backend', 'i_am_a_function', 'dirac')
    with pytest.raises(ExtensionNotFoundError):
        ext_mgr.load_ext('backend', 'i_am_a_variable', 'dirac')
