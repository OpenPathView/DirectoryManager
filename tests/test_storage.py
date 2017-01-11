# coding: utf-8

# Copyright (C) 2017 Open Path View
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.


from opv_directorymanager import Storage, LocalStorage, OPVDMException
import pytest
import uuid
import os

# Pas de slash dans le path
dir_test = "tests_dir_%s" % str(uuid.uuid1())


def test_storage():
    store = Storage()

    assert(store._cache == [])
    store._cache = ["Test", "Test1"]
    assert(store.exist("Test") is True)
    assert (store.exist("Test1") is True)
    assert (store.exist("Test0") is False)
    assert(store._cache == ["Test", "Test1"])

    store = Storage()
    with pytest.raises(NotImplementedError):
        store.ls()
    with pytest.raises(NotImplementedError):
        store.mkdir("tests_dir")


def test_local_storage():
    assert(dir_test.count("/") == 0)
    assert (os.path.isdir(dir_test) is False)
    store = LocalStorage(dir_test)
    assert (os.path.isdir(dir_test) is True)
    assert(store.path == os.path.realpath(os.path.expanduser(dir_test)))

    path = "%s/%s" % (dir_test, "TEMP")
    assert (os.path.isdir(path) is False)
    store.mkdir("TEMP")
    assert (os.path.isdir(path) is True)

    # Directory already exist
    with pytest.raises(OPVDMException):
        store.mkdir("TEMP")
    with pytest.raises(OPVDMException):
        store._mkdir("TEMP")

    # No slash in directory path
    with pytest.raises(OPVDMException):
        store.mkdir("TEMP////")

    assert(store.ls() == ["TEMP"])
    os.rmdir(path)
    os.rmdir(dir_test)
