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


from opv_directorymanager import DirectoryManager
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


@pytest.yield_fixture(autouse=True)
def conf_file():
    conf_test = "conf_test_%s" % str(uuid.uuid1())

    with open(conf_test, "w") as fic:
        fic.write(MYCONF)

    yield conf_test

    os.remove(conf_test)


def test_directory_manager(conf_file):
    directory_manager = DirectoryManager()

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
