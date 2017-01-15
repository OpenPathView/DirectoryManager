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
# Description: StorageService is an abstract class that must be override to implement storage service

from opv_directorymanager import OPVDMException
import multiprocessing as mp
import signal
import os


class StorageService:
    """
    StorageService is an abstract class for implement URI
    """

    def __init__(self, fct=None):
        self.__fct = fct
        self.__process = mp.Process(target=self.__fct)
        self._uri = None

    def __del__(self):
        self.stop()

    def start(self):
        """
        Start the service
        :return:
        """
        if self.__fct is None:
            return False
        if self.is_running():
            raise OPVDMException("Already running")
        self.__process.start()
        return self.is_running()

    def stop(self):
        """
        Stop the service
        :return:
        """

        while self.__process.is_alive():
            self.__process.terminate()
            self.__process.join(timeout=3)
            if self.__process.exitcode == -signal.SIGTERM:
                break

        return self.is_running()

    def is_running(self):
        """
        :return: boolean
        """
        return self.__process.is_alive()

    @property
    def uri(self):
        if self._uri is None:
            raise NotImplementedError
        return self._uri

