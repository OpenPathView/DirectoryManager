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


from opv_directorymanager import FTP, HTTP, LocalStorageService, StorageService, OPVDMException
import pytest
import uuid
import os

# For testing ftp

import ftplib
import io

# For testing http
import requests
import requests_ftp

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

CONTENT_TEST = """
TOTO
"""

FILE_TEST = "toto.txt"


@pytest.yield_fixture(autouse=True)
def directory():
    """
    Directory fixture
    Will create directory and temp file for testing storage services
    :return:
    """
    # Test directory
    dir_test = "tests_dir_%s" % str(uuid.uuid1())

    # Create the directory
    assert(os.path.isdir(dir_test) is False)
    os.makedirs(dir_test, mode=0o755)
    assert(os.path.isdir(dir_test) is True)

    # Create temp file
    temp_path = os.path.join(dir_test, FILE_TEST)
    with open(temp_path, "w") as fic:
        fic.write(CONTENT_TEST)
    assert(os.path.isfile(temp_path))

    # Function will be call with this argument
    yield (dir_test, get_open_port())

    # Remove temp directory
    assert(os.path.isdir(dir_test) is True)
    import shutil
    shutil.rmtree(dir_test)
    assert (os.path.isdir(dir_test) is False)


def test_storage_services(directory):
    path, port = directory
    storage_service = StorageService()
    assert(storage_service.is_running() is False)
    assert(storage_service.start() is False)
    assert(storage_service.stop() is False)
    assert(storage_service.is_running() is False)
    with pytest.raises(NotImplementedError):
        toto = storage_service.uri


def test_local_storage_services(directory):
    path, port = directory
    storage_service = LocalStorageService(path)
    assert(storage_service.start() is False)
    assert (storage_service.stop() is False)
    assert (storage_service.is_running() is False)
    assert(storage_service.uri == "file://%s" % path)


def test_ftp(directory):
    path, port = directory
    ftp = FTP(path, host="127.0.0.1", listen_host="127.0.0.1", listen_port=port)

    assert(ftp.uri == "ftp://%s:%s/" % ("127.0.0.1", port))

    # Test that service start
    ftp.start()

    with pytest.raises(OPVDMException):
        ftp.start()

    # Check service is running
    assert (ftp.is_running())

    # Connect to server

    requests_ftp.monkeypatch_session()
    s = requests.Session()

    r = s.retr("%s%s" % (ftp.uri, "toto.txt"))

    assert(r.status_code == 226)
    assert(r.text == CONTENT_TEST)

    # Stop http test service
    ftp.stop()

    assert(ftp.is_running() is False)


def test_http(directory):
    path, port = directory
    http = HTTP(path, host="127.0.0.1", listen_host="127.0.0.1", listen_port=port)

    addr = "http://%s:%s/v1/files/" % ("127.0.0.1", port)
    assert (http.uri == addr)

    # Test that service start
    http.start()

    # Check service is running
    assert(http.is_running())

    # Test if we can get the temp file
    r = requests.get(os.path.join(addr, "toto.txt"))

    assert(r.status_code == 200)
    assert(r.text == CONTENT_TEST)

    # Stop http test service
    http.stop()

    assert(http.is_running() is False)