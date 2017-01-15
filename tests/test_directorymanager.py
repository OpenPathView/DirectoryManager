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


from opv_directorymanager import DirectoryManager, FTP, StorageServiceManager, LocalStorageService, LocalStorage
import pytest
import uuid
import os
MYCONF = """
# Main configuration
[OPV]
# Id of the worker
id=First
# Path to directory
path=/tmp/directory_manager_storage
# Host to give with the URI. MUST BE THE HOST OF THE CURRENT COMPUTER!!!!
# If none, will compute it.
host=toto.fr

# Storage Service
[FTP]
host=0.0.0.0
port=2121
logfile=opv_directory_manager_ftp.log

[HTTP]
host=0.0.0.0
port=5050
logfile=opv_directory_manager_http.log
"""


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
def conf_file():
    conf_test = "conf_test_%s" % str(uuid.uuid1())

    with open(conf_test, "w") as fic:
        fic.write(MYCONF)

    yield conf_test

    os.remove(conf_test)


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


def test_directory_manager(conf_file, directory):
    path, port = directory
    ftp = FTP(path, host="127.0.0.1", listen_host="127.0.0.1", listen_port=port)
    local = LocalStorageService(path)
    assert (ftp.uri == "ftp://%s:%s/" % ("127.0.0.1", port))

    storage_m = StorageServiceManager("ftp", ftp)
    storage_m.addURI("file", local)
    directory_manager = DirectoryManager(storage_service_manager=storage_m, storage=LocalStorage(path))

    # Launch service and check that it start
    directory_manager.start_storage_service()
    assert (ftp.is_running() is True)

    assert(directory_manager.directory("Must return None") is None)
    ftp_temp = "ftp://%s:%s/%s" % ("127.0.0.1", port, "toto.txt")
    assert(directory_manager.directory("toto.txt") == ftp_temp)
    assert(directory_manager.directory("toto.txt", protocol="ftp") == ftp_temp)
    assert(directory_manager.directory("toto.txt", protocol="MustReturnFtp") == ftp_temp)
    assert(directory_manager.directory("toto.txt", protocol="file") == "file://%s" % os.path.join(path, "toto.txt"))
    # Read Configuration File
    directory_manager.read_config_file(conf_file)

    assert(directory_manager.ID == "First")
    assert(directory_manager.path == "/tmp/directory_manager_storage")

    temp = directory_manager.new_directory()
    assert(temp in directory_manager.ls())

    temp = directory_manager.protocols()
    assert("file" in temp)
    assert("ftp" in temp)
    assert("http" in temp)




