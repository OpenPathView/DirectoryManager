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
# Desctipion:   Warning following text is writting in "croissant baquette"
#               Petit code pour nous permettre d'avancer dans OPV en fournissant une brique complete de stockage de données
#               dans un dossier local qui serat exposer dans un premier temps en FTP. C'est du temp, ca peut amener à bouger
#               Je ne pense pas qu'on est besoin d'une base de données a ce niveau mais pour pas faire trop de la merde je
#               vais faire un petit bouchon.

import os
import configparser
import socket
import json
from opv_directorymanager import LocalStorage
from opv_directorymanager import FTP
from opv_directorymanager import HTTP
from opv_directorymanager import LocalStorageService
from opv_directorymanager import BasicIDGenerator
from opv_directorymanager import StorageServiceManager


class DirectoryManager:
    """
    OPV FileManager
    """

    def __init__(self, ID=None, path=None, storage=None, uid_generator=None, storage_service_manager=None):
        """
        :param path: Path to the directory to server by backed storage
        """
        self.__id = ID
        self.__path = path
        self.__host = None
        self.__storage = storage
        self.__uid_generator = uid_generator
        self.__storage_service_manager = storage_service_manager

    def read_config_file(self, config_file=None):
        """
        Read configuration file and initialize object. If config file is None, it will use default value
        :param config_file: path to configuration file
        :return:
        """
        # Stop storage service
        self.stop_storage_service()

        config = configparser.ConfigParser()
        if config_file is not None:
            config.read(os.path.realpath(config_file))

        # Main configuration
        self.__id = config.get("OPV", "id", fallback="ID")
        self.__path = config.get("OPV", "path", fallback="directory_manager_storage")
        self.__path = os.path.realpath(os.path.expanduser(self.__path))
        self.__host = config.get("OPV", "host", fallback=socket.gethostbyname(socket.gethostname()))

        # FTP configuration
        ftp_host = config.get("FTP", "host", fallback="0.0.0.0")
        ftp_port = config.getint("FTP", "port", fallback=2121)
        ftp_logfile = config.get("FTP", "logfile", fallback="opv_directory_manager_ftp.log")

        # HTTP configuration
        http_host = config.get("HTTP", "host", fallback="0.0.0.0")
        http_port = config.getint("HTTP", "port", fallback=5050)
        http_logfile = config.get("HTTP", "logfile", fallback="opv_directory_manager_http.log")

        # Id
        self.__uid_generator = BasicIDGenerator(self.__id)

        # Storage
        self.__storage = LocalStorage(self.__path)

        # FTP
        ftp_storage_service = FTP(
            self.__path, host=self.__host, listen_host=ftp_host, listen_port=ftp_port, logfile=ftp_logfile
        )

        # HTTP
        http_storage_service = HTTP(
            self.__path, host=self.__host, listen_host=http_host, listen_port=http_port, logfile=http_logfile
        )

        # Local
        local_storage_service = LocalStorageService(self.__path)

        # Storage service
        self.__storage_service_manager = StorageServiceManager("ftp", ftp_storage_service)
        self.__storage_service_manager.addURI("file", local_storage_service)
        self.__storage_service_manager.addURI("http", http_storage_service)

    def __del__(self):
        # Stop all storage services
        self.stop_storage_service()

    def start_storage_service(self):
        """
        Start storage services
        :return:
        """
        if self.__storage_service_manager is not None:
            self.__storage_service_manager.start()

    def stop_storage_service(self):
        """
        Stop storage services
        :return:
        """
        if self.__storage_service_manager is not None:
            self.__storage_service_manager.stop()

    # Accessor & Mutator
    @property
    def ID(self):
        """
        Get the ID of the FileManager
        :return: FileManagerID
        """
        return self.__id

    @property
    def path(self):
        """
        return path serve by backend storage
        :return: Path
        """
        return self.__path

    def new_directory(self):
        """
        Get a new directory
        :return: UID
        """
        # Get the uid of the directory
        uid = self.__uid_generator.getUID()

        # Create the directory
        self.__storage.mkdir(uid)

        return uid

    def directory(self, directory, protocol=None):
        """
        Get or set a directory
        :param directory: The directory to get, if none will create a directory
        :param supported_uri_by_client: list of protocol supported by client
        :return: the uri to the directory
        :raise: Exception will directory don't exist
        """
        if directory is None or directory == "" or not self.__storage.exist(directory):
            return None
        else:
            return os.path.join(self.__storage_service_manager.getURI(protocol).uri, directory)

    def ls(self):
        """
        List all UID in directory manager
        :return: list of UID
        """
        return json.dumps(self.__storage.ls())

    def protocols(self):
        return json.dumps(self.__storage_service_manager.ls())

default_config = """
# Main configuration
[OPV]
# Id of the worker
id=First
# Path to directory
path=directory_manager_storage
# Host to give with the URI. MUST BE THE HOST OF THE CURRENT COMPUTER!!!!
# If none, will compute it.
#host=toto.fr

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