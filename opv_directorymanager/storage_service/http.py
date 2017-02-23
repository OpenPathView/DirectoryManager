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
from flask import Flask, send_file
from flask_cors import CORS
from gevent.wsgi import WSGIServer
from opv_directorymanager.storage_service import StorageService

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
        StorageService.__init__(self, self.__start_server)
        self.__path = path
        self.__host = host
        self.__listen_host = listen_host
        self.__listen_port = listen_port
        self.__logfile = logfile
        self.__api = "/v1/files/"
        self._uri = "http://%s:%s%s" % (self.__host, self.__listen_port, self.__api)
        app = Flask("OPV-TuilesServer")
        CORS(app)

        @app.route(os.path.join(self.__api, "<path:name>"))
        def file_send(name):
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
            return send_file(p)

        handler = RotatingFileHandler(self.__logfile, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        self.__app = app

    def __start_server(self):
        """
        Actually start the FTP server
        :return:
        """
        http_server = WSGIServer((self.__listen_host, self.__listen_port), self.__app)
        http_server.serve_forever()
