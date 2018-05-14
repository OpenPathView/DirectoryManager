#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from setuptools import setup, find_packages
import pip

# Merci Sam & Max : http://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/

setup(
    name='opv_directorymanager',
    version="0.1.1",
    packages=find_packages(),
    author="Christophe NOUCHET",
    author_email="christophe.nouchet@openpathview.fr",
    description="Open Path View Directory Manager",
    long_description=open('README.md').read(),
    install_requires=[
        "Flask>=1.0.2",
        "pyftpdlib",
        "gevent",
        "Flask-Cors"
    ],
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=False,
    url='https://github.com/OpenPathView/DirectoryManager',

    scripts=[
        "bin/opv_dm_web.py"
    ],

    license="GPL3",
)
