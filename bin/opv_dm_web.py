#!/usr/bin/env python
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
# Description: This is the tests webinterface for the directory manager of Open Path View don't use this piece of sh*t
# for production!

import argparse
from opv_directorymanager import Webservice, default_config
from opv_directorymanager import DirectoryManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--configfile", dest="configfile", type=str, default=None,
        help="Specify configuration file for OPV Directory Manager"
    )
    parser.add_argument("-o", "--host", dest="host", type=str, default="0.0.0.0", help="Host to listen to")
    parser.add_argument("-p", "--port", dest="port", type=int, default=5000, help="Port to listen to")
    parser.add_argument(
        "-s", "--showConfigExample", action="store_true", dest="showMeExample",
        help="Show me a configuration file example"
    )
    args = parser.parse_args()

    if args.showMeExample:
        print(default_config)
        exit(0)

    dm = DirectoryManager()
    dm.read_config_file(config_file=args.configfile)
    web = Webservice(dm, args.host, args.port)
    web.start()

