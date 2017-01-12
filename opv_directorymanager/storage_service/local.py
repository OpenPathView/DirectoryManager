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
# Description: Add support for local storage service

from opv_directorymanager.storage_service import StorageService


class LocalStorageService(StorageService):
    """
    StorageService is an abstract class for implement URI
    """

    def __init__(self, path):
        """
        :param path: Path to give for the URI
        """
        StorageService.__init__(self)
        self.__path = path
        self._uri = "file://%s" % self.__path
