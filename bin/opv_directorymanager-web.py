#!/usr/bin/env python
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
# Description: This is the test webinterface for the directory manager of Open Path View don't use this piece of sh*t
# for production!

import os
import socket
import configparser
from flask import Flask
import argparse
from opv_directorymanager import LocalStorage
from opv_directorymanager import FTP
from opv_directorymanager import LocalStorageService
from opv_directorymanager import FileManager
from opv_directorymanager import BasicIDGenerator
from opv_directorymanager import StorageServiceManager

default_config = """
# This configuration file is temporary, so don't suppose that the syntax will be write in stone, I will change it!

# Configuration for the Directory Manager
[OPV]
# Path to the directory that is going to be use has parent of all our directory referencing by UID
path=tests

# The id of the worker
id=MonZolieID

# The storage service configuration (default one is FTP)
[FTP]
# Host return for URI, if not definied will try to compute it with the hostname
#host=127.0.0.1
# Host to listen for the ftp server
hostlisten=127.0.0.1
# Same as above but fot the port
port=2121

"""

config = configparser.ConfigParser()
config.read_string(default_config)


def web(config, host, port):
    ID = config["OPV"]["id"]
    path = config["OPV"]["path"]
    path = os.path.realpath(os.path.expanduser(path))
    ftp_host = config.get("FTP", "host", fallback=None)
    ftp_host_listen = config["FTP"]["hostlisten"]
    ftp_port = config["FTP"]["port"]
    storage = LocalStorage(path)
    temp = {}
    if ftp_host is not None:
        temp["host"] = ftp_host
    if ftp_port is not None:
        temp["port"] = ftp_port
    storage_service = FTP(
        path, host=ftp_host if ftp_host is not None else socket.gethostbyname(socket.gethostname()),
        host_listen=ftp_host_listen, port=ftp_port
    )
    storage_service_manager = StorageServiceManager("ftp", storage_service)

    local_storage_service = LocalStorageService(path)
    storage_service_manager.addURI("file", local_storage_service)

    uid_generator = BasicIDGenerator(ID)

    # On démarre le serveur FTP
    storage_service.start()

    fm = FileManager(ID, path, storage, uid_generator, storage_service_manager)

    app = Flask(__name__)

    @app.route("/directory", methods=["POST"])
    def create_directory():
        """
        Will create a directory in directory manager
        :return: The UID of the directory
        """
        try:
            return fm.new_directory()
        except Exception as e:
            return str(e), 500

    @app.route("/directory/<string:uid>")
    @app.route("/directory/<string:uid>/<string:protocol>")
    def directory(uid, protocol=None):
        """
        Get the URI to a directory by is UID
        :param uid: The UID of the directory
        :param protocol: The proctol that you want to use
        :return: the URI to the directory
        """
        try:
            return fm.directory(uid, protocol)
        except Exception as e:
            return str(e), 500

    app.run(host=host, port=port, threaded=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-c", "--config", dest="configfile", type=str, default=None, help="Specify configuration file for OPV Directory Manager"
    )
    parser.add_argument("-o", "--host", dest="host", type=str, default="0.0.0.0", help="Host to listen to")
    parser.add_argument("-p", "--port", dest="port", type=int, default=2121, help="Port to listen to")
    parser.add_argument(
        "-s", "--showConfigExample", action="store_true", dest="showMeExample",
        help="Show me a configuration file example"
    )
    args = parser.parse_args()

    if args.showMeExample:
        print(default_config)
        exit(0)
    if args.configfile is not None:
        config.read(args.configfile)

    web(config, args.host, args.port)
