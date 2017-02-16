import pytest

import os
import sys

from jsub.loader import load_class
from jsub.loader import ModuleNotFoundError, ClassNotFoundError, NotAClassError

@pytest.fixture(scope='module', autouse=True)
def setup_python_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    load_path1 = os.path.join(current_path, 'test_loader', 'load1')
    load_path2 = os.path.join(current_path, 'test_loader', 'load2')
    sys.path.insert(0, load_path1)
    sys.path.insert(0, load_path2)
    print(sys.path)


def test_load_instances():
    i = load_class('jsub_ext1.repo.file_system', 'FileSystem')()
    assert i.desc == 'load1: jsub_ext1.repo.file_system.FileSystem'
    i = load_class('jsub_ext3.repo.sqlite', 'Sqlite')()
    assert i.desc == 'load2: jsub_ext3.repo.sqlite.Sqlite'
    i = load_class('jsub_ext2.backend.condor', 'Condor')()
    assert i.desc == 'load1: jsub_ext2.backend.condor.Condor'
    i = load_class('jsub_ext2.backend.pbs', 'Pbs')()
    assert i.desc == 'load1: jsub_ext2.backend.pbs.Pbs'
    i = load_class('jsub_ext3.backend.dirac', 'Dirac')()
    assert i.desc == 'load2: jsub_ext3.backend.dirac.Dirac'

def test_load_specific_class():
    i = load_class('jsub_ext2.backend.condor', 'ClassWithSpecificName')()
    assert i.desc == 'load1: jsub_ext2.backend.condor.ClassWithSpecificName'


def test_load_not_existed_module():
    with pytest.raises(ModuleNotFoundError):
        load_class('jsub_ext2.backend.unknown_module', 'UnknownClass')
    with pytest.raises(ModuleNotFoundError):
        load_class('jsub_ext3.backend.unknown_module', 'Condor')

def test_load_not_existed_class():
    with pytest.raises(ClassNotFoundError):
        load_class('jsub_ext2.backend.condor', 'UnknownClass')
    with pytest.raises(ClassNotFoundError):
        load_class('jsub_ext3.repo.empty', 'Empty')
    with pytest.raises(ClassNotFoundError):
        load_class('jsub_ext2.backend.condor', 'ClassWithAnotherName')

def test_load_not_a_class():
    with pytest.raises(NotAClassError):
        load_class('jsub_ext3.backend.dirac', 'i_am_a_function')
    with pytest.raises(NotAClassError):
        load_class('jsub_ext3.backend.dirac', 'i_am_a_variable')
