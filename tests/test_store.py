import grocer
import pytest
import pathlib


@pytest.fixture()
def ini_pathlib_dir(request):
    cwd = pathlib.Path.cwd()
    a_dir = pathlib.Path.joinpath(cwd, "tests", "a_dir")
    a_dir.mkdir()

    def rmdir():
        a_dir.rmdir()

    request.addfinalizer(rmdir)

    return a_dir


@pytest.fixture()
def ini_pathlib_file(request):
    cwd = pathlib.Path.cwd()
    a_file = pathlib.Path.joinpath(cwd, "tests", "a_file")
    a_file.touch()

    def unlink():
        a_file.unlink()

    request.addfinalizer(unlink)

    return a_file


@pytest.fixture()
def ini_aisle():
    cwd = pathlib.Path.cwd()
    store_path = pathlib.Path.joinpath(cwd, "tests", "store")
    store = grocer.Store(store_path)
    aisle = store["produce"]
    return aisle


@pytest.fixture()
def ini_apple_path(request):
    cwd = pathlib.Path.cwd()
    apple_path = pathlib.Path.joinpath(cwd, "tests", "store", "produce", "apple.json")

    def rm():
        apple_path.unlink()

    request.addfinalizer(rm)

    return apple_path


def test_store_init_works_when_given_dir_doesnt():
    cwd = pathlib.Path.cwd()
    a_dir = pathlib.Path.joinpath(cwd, "tests", "a_dir")
    a = grocer.Store(a_dir)
    assert a._store_path.exists()
    a_dir.rmdir()


def test_store_init_works_when_given_dir_exists(ini_pathlib_dir):
    a = grocer.Store(ini_pathlib_dir)
    assert a._store_path.exists()


def test_store_init_raises_when_given_file(ini_pathlib_file):
    with pytest.raises(NotADirectoryError):
        grocer.Store(ini_pathlib_file)


def test_store_access_key_exists(ini_aisle):
    d = ini_aisle["eggplant"]
    assert "price" in d.keys()


def test_store_access_key_doesnt(ini_aisle):
    with pytest.raises(KeyError):
        ini_aisle["apple"]


def test_store_create_sku(ini_aisle, ini_apple_path):
    d = {"price": "2.0"}
    ini_aisle["apple"] = d
    assert d == ini_aisle["apple"]
