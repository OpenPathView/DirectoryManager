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
import magic
from PIL import Image
import io
from flask import Flask, send_file, request
from flask_cors import CORS
from flask_caching import Cache
from gevent.pywsgi import WSGIServer
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
        app = Flask("OPV-TuilesServer")
        CORS(app)
        cache = Cache(app, config={'CACHE_TYPE': 'simple'})

        def make_key():
          """Make a key that includes GET parameters."""
          return request.full_path

        @app.route(os.path.join(self.__api, "<path:name>"))
        @cache.cached(timeout=50, key_prefix=make_key)
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

            if magic.from_file(p, mime=True).split("/")[0] == "image" and (request.args.get('scale') is not None or request.args.get('width') is not None or request.args.get('height') is not None):
                img = Image.open(p)
                size = [0, 0]
                if request.args.get('scale', type=int) is not None:
                    scale = request.args.get('scale', type=int)
                    size = [img.size[0]/scale, img.size[1]/scale]
                elif request.args.get('width', type=int) is not None:
                    size = [request.args.get('width', type=int), img.size[1]]
                elif request.args.get('height', type=int) is not None:
                    size = [img.size[0], request.args.get('height', type=int)]
                img.thumbnail(size)  # Automatically compute the image max size that can be contained into "size" preserving ratio
                p = io.BytesIO()
                img.save(p, "JPEG")
                p.seek(0)
                return send_file(p, mimetype='image/jpeg')

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

    def uri(self, no_host=False):
        """
        :param ho_host:
        :return:
        """
        return "http://%s:%s%s" % (
            self.__host if no_host is False else "{host}",
            self.__listen_port,
            self.__api
        )