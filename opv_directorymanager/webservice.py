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

import json
from flask import Flask
from flasgger import Swagger
from flask import request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer


class Webservice:

    def __init__(self, directory_manager, host, port):
        self.__host = host
        self.__port = port
        self.__directory_manager = directory_manager

    def start(self):
        app = Flask("OPV-DirectoryManager")
        swagger = Swagger(app)
        CORS(app)

        @app.route("/v1/directory", methods=["POST"])
        def create_directory():
            """Will create a directory in directory manager
            This is using docstrings for specifications.
            ---
            responses:
              200:
                description: The UID of the new directory
                examples:
                  NewId: ID-1-2f969174-5e22-11e9-8798-38d5471381ce
              500:
                description: If the DirectoryManager can't create the directory
            """
            try:
                return json.dumps(self.__directory_manager.new_directory())
            except Exception as e:
                return str(e), 500

        @app.route("/v1/directory/<string:uid>")
        @app.route("/v1/directory/<string:uid>/<string:protocol>")
        def directory(uid, protocol=None):
            """Get the URI of an UID
            TEST
            ---
            parameters:
              - name: uid
                in: path
                type: string
                required: true
              - name: protocol
                in: path
                enum: ["http", "ftp", "file"]
                type: string
                required: false
                default: ftp
              - name: no-host
                in: header
                type: int
                required: false
                enum: [0, 1]
                default: 0
            responses:
              200:
                description: The URI of the UID
                examples:
                  URI: ftp://127.0.0.1:2121/ID-1-2f969174-5e22-11e9-8798-38d5471381ce
              500:
                description: The directory didn't exist
            """
            # """
            # Get the URI to a directory by is UID
            # :param uid: The UID of the directory
            # :param protocol: The proctol that you want to use
            # :return: the URI to the directory
            # """
            try:
                no_host = bool(int(request.headers["No-Host"])) if "No-Host" in request.headers else False
                return json.dumps(self.__directory_manager.directory(uid, protocol, no_host))
            except Exception as e:
                return str(e), 500

        @app.route("/v1/ls")
        def ls():
            """List all UID store in the DirectoryManager
            TEST
            ---
            responses:
              200:
                description: The UID of the new directory
                examples:
                  list: ["ID-1-2f969174-5e22-11e9-8798-38d5471381ce"]
            """
            try:
                return json.dumps(self.__directory_manager.ls())
            except Exception as e:
                return str(e), 500

        @app.route("/v1/protocols")
        def protocols():
            """List of protocols supported by the DirectoryManager
            TEST
            ---
            responses:
              200:
                description: The UID of the new directory
                examples:
                  list: ["ftp", "file", "http"]
            """
            try:
                return json.dumps(self.__directory_manager.protocols())
            except Exception as e:
                return str(e), 500

        http_server = WSGIServer((self.__host, self.__port), app)
        http_server.serve_forever()
