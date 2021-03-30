import pytest

from jsub.manager.extension import ExtensionManager
from jsub.task import Task, TaskPool

@pytest.fixture(scope='module')
def repo_file_system(tmpdir_factory):
    ext_mgr = ExtensionManager(['jsub.exts'])
    config_repo = {}
    config_repo['type'] = 'file_system'
    config_repo['param'] = {'dir': str(tmpdir_factory.mktemp('repo_file_system'))}
    return ext_mgr.load_ext_common('repo', config_repo)


def test_repo_file_system(repo_file_system):
    from jsub.exts.repo.file_system import FileSystem
    assert isinstance(repo_file_system, FileSystem)

def test_save_load(repo_file_system):
    task_pool = TaskPool(repo_file_system)
    task_id_1 = task_pool.create({'a':3, 'b':'ok'}).data['id']
    task_id_2 = task_pool.create({'c':9, 'd':'no'}).data['id']
    assert len(task_pool.all()) == 2

    task_1 = task_pool.find(task_id_1)
    task_2 = task_pool.find(task_id_2)
    assert task_1.data['a'] == 3
    assert task_1.data['b'] == 'ok'
    assert task_2.data['c'] == 9
    assert task_2.data['d'] == 'no'
