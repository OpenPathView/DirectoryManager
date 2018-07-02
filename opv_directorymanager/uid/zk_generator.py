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
# Description: Just a little code for generating uniq id for directory using zookeeper to increment uid

import os
from opv_directorymanager.uid import BasicIDGenerator


class ZkIDGenerator(BasicIDGenerator):

    def __init__(self, zk, path="/DirectoryManager/increment", *args, **kwargs):
        """
        :param zk: KazooClient
        :param path: The path on zookeeper for the UID
        """
        BasicIDGenerator.__init__(self, *args, **kwargs)

        self.__zk = zk
        self.__path = path

    @property
    def zk(self):
        """Get the KazooClient"""
        return self.__zk

    @zk.setter
    def zk(self, zk):
        """Set the KazooClient"""
        self.__zk = zk

    @property
    def path(self):
        """Get the path on zookeeper"""
        return self.__path

    @path.setter
    def path(self, path):
        """Set the path on zookeeper"""
        self.__path = path

    def increment(self):
        """
        Increment the UID
        :return : Return the value incremented
        """
        self.zk.ensure_path(self.path)
        counter = self.zk.Counter(os.path.join(self.path, "int"), default=0)
        counter += 1
        return counter.value

