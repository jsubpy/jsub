import pytest

from jsub.dag import DAG

@pytest.fixture(scope='module')
def dag():
    dag = DAG
    return ext_mgr.load_ext_common('repo', config_repo)

def test_repo_file_system(repo_file_system):
    from jsub.exts.repo.file_system import FileSystem
    assert isinstance(repo_file_system, FileSystem)
