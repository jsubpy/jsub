import pytest

from jsub.loader import Loader
from jsub.task import Task, TaskPool

@pytest.fixture(scope='module')
def repo_file_system(tmpdir_factory):
    loader = Loader(['jsub.exts'])
    repo_dir = str(tmpdir_factory.mktemp('repo_file_system'))
    return loader.load_class('repo', 'FileSystem')(repo_dir)


def test_repo_file_system(repo_file_system):
    from jsub.exts.repo.file_system import FileSystem
    assert isinstance(repo_file_system, FileSystem) 

def test_save_load(repo_file_system):
    task_pool = TaskPool(repo_file_system)
    task_id_1 = task_pool.create({'a':3, 'b':'ok'}).data['task_id']
    task_id_2 = task_pool.create({'c':9, 'd':'no'}).data['task_id']
    assert len(task_pool.all()) == 2

    task_1 = task_pool.find(task_id_1)
    task_2 = task_pool.find(task_id_2)
    assert task_1.props['a'] == 3
    assert task_1.props['b'] == 'ok'
    assert task_2.props['c'] == 9
    assert task_2.props['d'] == 'no'
