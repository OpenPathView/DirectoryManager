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
# Description: Add support to ftp for storage service


import socket
import logging
import json
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from gevent.wsgi import WSGIServer
from opv_directorymanager.storage_service import StorageService
import multiprocessing as mp

HOST = socket.gethostbyname(socket.gethostname())


class HTTP(StorageService):
    """
    HTTP backend service storage
    """

    def __init__(self, path, host=HOST, listen_host=HOST, listen_port=5050, logfile="http.log"):
        """
        Create and configure FTP server
        :param path: Path to share
        :param host: Host to listen to
        :param port: Port to listen to
        :param user: User to use for ftp server
        :param password: Password to use for ftp server
        :param logfile: Log file path
        """
        self.__path = path
        self.__host = host
        self.__listen_host = listen_host
        self.__listen_port = listen_port
        self.__logfile = logfile
        self.__api = "/v1/files/"
        self.__uri = "http://%s:%s%s" % (self.__host, self.__listen_port, self.__api)
        app = Flask("OPV-TuilesServer")

        @app.route(os.path.join(self.__api, "<path:name>"))
        def send_file(name):
            """
            Will create a directory in directory manager
            :return: The UID of the directory
            """
            temp = []
            for i in name.split("/"):
                if i != "." and i != "..":
                    temp.append(i)
            p = os.path.join(self.__path, "/".join(temp))
            if os.path.isdir(p):
                return json.dumps(os.listdir(p))
            with open(p, "r") as fic:
                return fic.read()

        handler = RotatingFileHandler(self.__logfile, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        self.__app = app
        self.__process = None

    def uri(self):
        """
        Return URI of the FTP
        :return: string
        """
        return self.__uri

    def start(self):
        """
        Start the FTP server
        :return:
        """
        self.__process = mp.Process(target=self._start_server)
        self.__process.start()

    def _start_server(self):
        """
        Actually start the FTP server
        :return:
        """
        http_server = WSGIServer((self.__listen_host, self.__listen_port), self.__app)
        http_server.serve_forever()

if __name__ == "__main__":
    http = HTTP("directory_manager_storage")
    http._start_server()