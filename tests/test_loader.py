import pytest

import os
import sys

from jsub.loader import Loader
from jsub.loader import ModuleNotFoundError, ClassNotFoundError, NotAClassError

class TestLoader:
    @pytest.fixture(scope='class', autouse=True)
    def files(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        load_path1 = os.path.join(current_path, 'test_loader', 'load1')
        load_path2 = os.path.join(current_path, 'test_loader', 'load2')
        sys.path.insert(0, load_path1)
        sys.path.insert(0, load_path2)

    @pytest.fixture(scope='class')
    def loader(self):
        return Loader(['jsub_ext1', 'jsub_ext2', 'jsub_ext3'])


    def test_load_instances(self, loader):
        i = loader.load_instance('repo', 'FileSystem')
        assert i.desc == 'load1: jsub_ext1.repo.file_system.FileSystem'
        i = loader.load_instance('repo', 'Sqlite')
        assert i.desc == 'load2: jsub_ext3.repo.sqlite.Sqlite'
        i = loader.load_instance('backend', 'Condor')
        assert i.desc == 'load1: jsub_ext2.backend.condor.Condor'
        i = loader.load_instance('backend', 'Pbs')
        assert i.desc == 'load1: jsub_ext2.backend.pbs.Pbs'
        i = loader.load_instance('backend', 'Dirac')
        assert i.desc == 'load2: jsub_ext3.backend.dirac.Dirac'

    def test_load_specific_class(self, loader):
        i = loader.load_instance('backend', 'ClassWithSpecificName', 'condor')
        assert i.desc == 'load1: jsub_ext2.backend.condor.ClassWithSpecificName'


    def test_load_not_existed_module(self, loader):
        with pytest.raises(ModuleNotFoundError):
            loader.load_instance('backend', 'UnknownClass')
        with pytest.raises(ModuleNotFoundError):
            loader.load_instance('backend', 'Condor', 'unknown_module')

    def test_load_not_existed_class(self, loader):
        with pytest.raises(ClassNotFoundError):
            loader.load_instance('backend', 'UnknownClass', 'condor')
        with pytest.raises(ClassNotFoundError):
            loader.load_instance('repo', 'Empty')
        with pytest.raises(ClassNotFoundError):
            loader.load_instance('backend', 'ClassWithAnotherName', 'condor')

    def test_load_not_a_class(self, loader):
        with pytest.raises(NotAClassError):
            loader.load_instance('backend', 'i_am_a_function', 'dirac')
        with pytest.raises(NotAClassError):
            loader.load_instance('backend', 'i_am_a_variable', 'dirac')
