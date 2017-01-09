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
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from opv_directorymanager.storage_service import StorageService
import multiprocessing as mp

HOST = socket.gethostbyname(socket.gethostname())

class FTP(StorageService):
    """
    FTP backed service storage
    """

    def __init__(
            self, path, host=HOST,
            host_listen=HOST, port=21, user=None, password=None,
            logfile="pyftpd.log"
    ):
        """
        Create and configure FTP server
        :param path: Path to share
        :param host: Host to listen to
        :param port: Port to listen to
        :param user: User to use for ftp server
        :param password: Password to use for ftp server
        :param logfile: Log file path
        """
        self.__host = host
        self.__host_listen = host_listen
        self.__port = port
        self.__user = user
        self.__password = password
        self.__logfile = logfile

        authorizer = DummyAuthorizer()

        # Make the URI
        if self.__user is not None and self.__password is not None:
            print(self.__user, self.__password)
            self.__uri = "ftp://%s:%s@%s:%s/" % (self.__user, self.__password, self.__host, self.__port)
            authorizer.add_user(self.__user, self.__password, path, perm='elradfmwM')
        else:
            self.__uri = "ftp://%s:%s/" % (self.__host, self.__port)
            authorizer.add_anonymous(path, perm='elradfmwM')

        handler = FTPHandler
        handler.authorizer = authorizer

        self.__server = FTPServer((self.__host_listen, self.__port), handler)
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
        self.__process = mp.Process(target=self.__start_server)
        self.__process.start()

    def __start_server(self):
        """
        Actually start the FTP server
        :return:
        """
        logging.basicConfig(filename=self.__logfile, level=logging.INFO)
        self.__server.serve_forever()
