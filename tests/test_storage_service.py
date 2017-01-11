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


from opv_directorymanager import FTP, HTTP, LocalStorageService, StorageService
import pytest
import uuid
import os

def get_open_port():
    """
    http://stackoverflow.com/questions/2838244/get-open-tcp-port-in-python/2838309#2838309
    :return: free port
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.yield_fixture(autouse=True)
def directory():
    # Pas de slash dans le path
    dir_test = "tests_dir_%s" % str(uuid.uuid1())

    # Create the directory
    assert(os.path.isdir(dir_test) is False)
    os.makedirs(dir_test, mode=0o755)
    yield (dir_test, get_open_port())
    assert(os.path.isdir(dir_test) is True)
    import shutil
    shutil.rmtree(dir_test)
    assert (os.path.isdir(dir_test) is False)


def test_storage_service():
    storage_service = StorageService()
    with pytest.raises(NotImplementedError):
        storage_service.start()
    with pytest.raises(NotImplementedError):
        storage_service.uri()


def test_local_storage_services(directory):
    path, port = directory
    storage_service = LocalStorageService(path)
    assert(storage_service.start() == True)
    assert(storage_service.uri() == "file://%s" % path)


def test_ftp(directory):
    path, port = directory
    ftp = FTP(path, host="127.0.0.1", listen_host="127.0.0.1", listen_port=port)

    assert(ftp.uri() == "ftp://%s:%s/" % ("127.0.0.1", port))

    # Test that service start


def test_http(directory):
    path, port = directory
    http = HTTP(path, host="127.0.0.1", listen_host="127.0.0.1", listen_port=port)

    assert (http.uri() == "http://%s:%s/v1/files/" % ("127.0.0.1", port))

    # Test that service start
