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
# Description: This class will create the directory locally

import os
from opv_directorymanager.storage import Storage


class LocalStorage(Storage):
    """
    Local storage
    """
    def __init__(self, path):
        """
        :param path: Path to directory
        """
        Storage.__init__(self)
        self.__path = os.path.realpath(os.path.expanduser(path))
        # Check if path exist otherwise make it
        if not os.path.isdir(path):
            os.mkdir(path, mode=0o755)
        self._cache = self.ls()

    @property
    def path(self):
        """
        Return path
        :return: string
        """
        return self.__path

    def _mkdir(self, directory, options=None):
        """
        Create a directory in storage
        :param directory: Name of the directory
        :param options:
        :return:
        """
        if directory.find("/") >= 0:
            raise Exception("I don't accept directory name with '/' in name")
        if os.path.isdir(directory):
            raise Exception("Directory already exist")

        # Create the directory
        os.mkdir(os.path.join(self.path, directory))

    def ls(self, options=None):
        """
        List all element in directory
        :param options:
        :return: list
        """
        return os.listdir(self.path)