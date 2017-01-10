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

import threading


class StorageServiceManager:
    """
    Manage all Storage service
    """

    def __init__(self, protocol, service_manager):
        """
        :param protocol: Default protocol to use
        :param service_manager: Default service manager to use for default protocol
        """
        self.__uris = {}
        self.__default_protocol = protocol
        self.__lock = threading.Lock()
        # Add default URI
        self.addURI(protocol, service_manager)


    def addURI(self, protocol, service_manager):
        """
        Add storage service
        :param uri: Protocl to use
        :param service_manager: Service manager to use
        :return:
        """
        if protocol in self.__uris:
            raise Exception("%s already in manager" % protocol)
        with self.__lock:
            self.__uris[protocol] = service_manager

    def getURI(self, protocol=None):
        """
        Get the URI for a protocol
        :param protocol: protocol associate with URI, if none return the default one
        :return: string, URI
        """
        with self.__lock:
            if protocol is None or protocol not in self.__uris:
                return self.__uris[self.__default_protocol]
            else:
                return self.__uris[protocol]
