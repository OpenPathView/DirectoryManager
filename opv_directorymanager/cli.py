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

# Contributors: Nouchet Christophe
# Email: christophe.nouchet@openpathview.fr

import configparser
from opv_directorymanager import LocalStorage
from opv_directorymanager import FTP
from opv_directorymanager import FileManager
from opv_directorymanager import BasicIDGenerator
from opv_directorymanager import StorageServiceManager

default_config = """
[OPV]
# This path must exist!!!!!!!!!!!
path=tests

[FTP]
host=0.0.0.0
port=1717

"""

config = configparser.ConfigParser()
config.read_string(default_config)


def cli(ID, path, host, port):

    storage = LocalStorage(path)

    storage_service = FTP(path, host=host, port=port)
    storage_service_manager = StorageServiceManager("ftp", storage_service)

    uid_generator = BasicIDGenerator(ID)

    # On démarre le serveur
    storage_service.start()

    fm = FileManager("ID", path, storage, uid_generator, storage_service_manager)

    while True:
        # On demande quelle URI otpenir
        a = input("$ ")
        if a == "list":
            [print(i) for i in storage.ls()]
        elif a == "mkdir":
            print(fm.new_directory())
        else:
            print(fm.directory(a))


if __name__ == "__main__":
    cli("ID", "/home/christophe/Documents/MDL/OPV/FileManager/test", "127.0.0.1", 2121)
