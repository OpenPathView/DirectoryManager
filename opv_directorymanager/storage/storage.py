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
# Description: You must implement a least one Storage for creating directory

import threading


class Storage:
    """
    Abstarct storage
    """

    def __init__(self):
        self.__lock = threading.Lock()
        self.__cache = []

    @property
    def _cache(self):
        with self.__lock:
            return self.__cache

    @_cache.setter
    def _cache(self, cache):
        with self.__lock:
            self.__cache = cache

    def mkdir(self, directory, options=None):
        """
        Create a directory in storage
        :param directory: Name of the directory
        :param options:
        :return:
        :raise: Exception if it's impossible to make directory
        """
        if self.exist(directory):
           raise Exception("Directory already exist")

        # Create the directory
        self._mkdir(directory, options)

        # Add directory to cache
        self._cache.append(directory)

    def _mkdir(self, directory, options=None):
        raise NotImplementedError

    def ls(self, options=None):
        """
        List all element in directory
        :param options:
        :return: list
        """
        raise NotImplementedError

    def exist(self, uid):
        """
        Check if an uid exist
        :param uid: UID to check
        :return: boolean
        """
        return uid in self._cache
