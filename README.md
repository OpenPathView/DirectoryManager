# OPV Directory Manager

** WARNING: This piece of software is not finished at all, so it (can be) is buggy **

** To make this project work smoothly you must have a resolvable hostname. "hostname -i" must not return 127.0.0.1! or modify configuration file **

For example

```
$ hostname -i
192.168.0.100
```

## Description

This project will be use to make a link between unique ID and directory. Long story short, we have to setup a storage service between local independent worker and a centralized one. So we need a component that can serve access to a directory and referencing it in a database. But we can't referencing the path to the directory in the database, because it's local to the worker. We need a component that can make a link between an unique id and where the data is store. This little piece of software was made for that purpose ^^.

The name is maybe too long, I'm not very good for naming thing, sorry...

## Architecture

This software is compose by:

* Storage facilities: Where the directories referenced by UID are store (by default in local)
* Storage service: Give access to the directory to other host (by default, will use FTP, but we will need http)
* UID generator: It's use to generate uniq id to reference directory in database
* Web interface: A very simple one and not production ready (flask). This web interface is use a restful API to make directory and get URI for a UID

## I want to play with it

You should consider install this beauty in a virtualenv ^^.

### I want to install this beauty

```
python setup.py install
```

### I want correct all bugs that you leave in your code... / extend functionalities

```
pip3 install -r requirements.txt
```

## How to run it

For help
```
$ opv_directorymanager-web.py -h
usage: opv_directorymanager-web.py [-h] [-c CONFIGFILE] [-o HOST] [-p PORT]
                                   [-s]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIGFILE, --config CONFIGFILE
                        Specify configuration file for OPV Directory Manager
  -o HOST, --host HOST  Host to listen to
  -p PORT, --port PORT  Port to listen to
  -s, --showConfigExample
                        Show me a configuration file example
```

For basic usage, I create a default configuration that can be override in configuration file:
```
$ opv_directorymanager-web.py -s

# This configuration file is temporary, so don't suppose that the syntax will be write in stone, I will change it!

# Configuration for the Directory Manager
[OPV]
# Path to the directory that is going to be use has parent of all our directory referencing by UID
path=tests

# The id of the worker
id=MonZolieID

# The storage service configuration (default one is FTP)
[FTP]
# Host return for URI, if not definied will try to compute it with the hostname
#host=127.0.0.1
# Host to listen for the ftp server
hostlisten=127.0.0.1
# Same as above but fot the port
port=2121
```

Example: The following command will create a web interface listening on 127.0.0.1:5000 and a ftp server listening on 127.0.0.1:21

```
opv_directorymanager-web.py -o 127.0.0.1 -p 5000
```

## API Documenation

### Create a new directory and get his UID

```
$ curl -X POST http://127.0.0.1:5000/directory
MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365
```

### Get the directory URI by is UID

```
curl -X GET http://127.0.0.1:5000/directory/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365
ftp://127.0.1.1:2121/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365
```
Or if you want to specify another protocol (accecpted protocl [ftp, file])
```
curl -X GET http://127.0.0.1:5000/directory/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365/file
file:///home/christophe/Documents/MDL/OPV/FileManager/tests/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365
```

## Todo

* FINISHED IT
* Add Test (si ca peut nous éviter de perdre un dimanche après midi sur un script d'extraction d'image dans des SD non testé. Je dit ca je dit rien :))
* Add a central class that handle all initialisation stuff (like instantiated storage, storage_service and UID)
* Add configuration file
* Add log
* Make this thing beautiful

## License

Copyright (C) 2017 Open Path View <br />
This program is free software; you can redistribute it and/or modify  <br />
it under the terms of the GNU General Public License as published by  <br />
the Free Software Foundation; either version 3 of the License, or  <br />
(at your option) any later version.  <br />
This program is distributed in the hope that it will be useful,  <br />
but WITHOUT ANY WARRANTY; without even the implied warranty of  <br />
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  <br />
GNU General Public License for more details.  <br />
You should have received a copy of the GNU General Public License along  <br />
with this program. If not, see <http://www.gnu.org/licenses/>.  <br />


