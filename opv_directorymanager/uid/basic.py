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

import uuid
import threading
from opv_directorymanager.uid import UIDGenerator


class BasicIDGenerator(UIDGenerator):
    """
    Very simple uid generator with suffix that represent the luggage id
    """
    def __init__(self, prefix=""):
        self.__prefix = prefix
        self.__lock = threading.Lock()
        self.__inc = 0

    @property
    def prefix(self):
        return self.__prefix

    def increment(self):
        """
        Increment the UID
        :return : Return the value incremented
        """
        self.__inc += 1
        return self.__inc

    def safe_increment(self):
        """
        Increment the UID with lock
        :return : Return the value incremented
        """
        with self.__lock:
            return self.increment()

    def getUID(self):
        """Get the new UID"""
        return "%s%s-%s" % ("%s-" % self.prefix if self.prefix else "", self.safe_increment(), str(uuid.uuid1()))
