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


class StorageService:
    """
    StorageService is an abstract class for implement URI
    """

    def start(self):
        """
        Start the service
        :return:
        """
        raise NotImplementedError

    def uri(self):
        """
        Get the URI of the service
        :return:
        """
        raise NotImplementedError
