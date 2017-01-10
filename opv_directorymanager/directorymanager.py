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
# Desctipion:   Warning following text is writting in "croissant baquette"
#               Petit code pour nous permettre d'avancer dans OPV en fournissant une brique complete de stockage de données
#               dans un dossier local qui serat exposer dans un premier temps en FTP. C'est du temp, ca peut amener à bouger
#               Je ne pense pas qu'on est besoin d'une base de données a ce niveau mais pour pas faire trop de la merde je
#               vais faire un petit bouchon.

import os


class DirectoryManager:
    """
    OPV FileManager
    """

    def __init__(self, ID, path, storage, uid_generator, storage_service_manager):
        """
        :param path: Path to the directory to server by backed storage
        """
        self.__ID = ID
        self.__path = path
        self.__storage = storage
        self.__uid_generator = uid_generator
        self.__storage_service_manager = storage_service_manager

    # Accessor & Mutator
    @property
    def ID(self):
        """
        Get the ID of the FileManager
        :return: FileManagerID
        """
        return self.__ID

    @property
    def path(self):
        """
        return path serve by backend storage
        :return: Path
        """
        return self.__path

    @property
    def uid_generator(self):
        return self.__uid_generator

    def new_directory(self):
        """
        Get a new directory
        :return: UID
        """
        # Get the uid of the directory
        uid = self.__uid_generator.getUID()

        # Create the directory
        self.__storage.mkdir(uid)

        return uid

    def directory(self, directory, protocol=None):
        """
        Get or set a directory
        :param directory: The directory to get, if none will create a directory
        :param supported_uri_by_client: list of protocol supported by client
        :return: the uri to the directory
        :raise: Exception will directory don't exist
        """
        if directory is None or directory == "" or not self.__storage.exist(directory):
            return None
        else:
            return os.path.join(self.__storage_service_manager.getURI(protocol).uri(), directory)
