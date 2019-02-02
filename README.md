# OPV Directory Manager


**To make this project work smoothly (rechable by other host) you must have a resolvable hostname. "hostname -i" must not return 127.0.0.1! or modify configuration file**

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
* Storage service: Give access to the directory to other host (by default, will use FTP)
    * file : Return local path to directories
    * ftp : Give ftp uri to acces to the directories by ftp
    * http : Give http uri to acces to the files by http
* UID generator: It's use to generate uniq id to reference directory in database
* Web interface: This web interface is use as a restful API to make directory and get URI for a UID

## I want to play with it


### Docker

```bash
docker build -t directorymanager -f Dockerfile .
```

You should consider using volume and map it as /mnt/dm

```bash
docker volume create dm
```

Launch the image

```bash
docker run -it -p 2121:2121 -p 5000:5000 -p 5050:5050 -v dm:/mnt/dm --rm directorymanager
```

You should consider to install it in a virtualenv.

### I want to install it

```
apt-get install libffi-dev libssl-dev
pip3 install -r requirements.txt
python setup.py install
```

## How to run it

For help
```
$ opv_dm_web.py -h
usage: opv_dm_web.py [-h] [-c CONFIGFILE] [-o HOST] [-p PORT] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIGFILE, --configfile CONFIGFILE
                        Specify configuration file for OPV Directory Manager
  -o HOST, --host HOST  Host to listen to
  -p PORT, --port PORT  Port to listen to
  -s, --showConfigExample
                        Show me a configuration file example
```

For basic usage, I create a default configuration that can be override in configuration file:

```
# Show you an example of configuration file
$ opv_dm_web.py -s

# Main configuration
[OPV]
# Id of the worker
id=First
# Path to directory
path=directory_manager_storage
# Host to give with the URI. MUST BE THE HOST OF THE CURRENT COMPUTER!!!!
# If none, will compute it.
#host=toto.fr
# To chosse the backend for the uid
# Values can be [basic, zookeeper, zk]
uid_type=basic

# Storage Service
[FTP]
host=0.0.0.0
port=2121
logfile=opv_directory_manager_ftp.log

[HTTP]
host=0.0.0.0
port=5050
logfile=opv_directory_manager_http.log

# If you choose uid_type=zk or uid_type=zookeeper
[ZOOKEEPER]
# Hosts to zookeeper cluster
hosts=127.0.0.1:2181

# Path to use on zookeeper
path=/DirectoryManager/increment
```

Example: The following command will create a web interface listening on 127.0.0.1:5000 and a ftp server listening on 0.0.0.0:2121

```
opv_dm_web.py -o 127.0.0.1 -p 5000
```

## Launch tests

You can launch unit and functionnal tests with this command:

```
./launch_test.sh
```

Code coverage is avaible under directory 'htmlcov', open index.html to see the report.


## API Documenation

### Create a new directory and get his UID

```
$ curl -X POST http://127.0.0.1:5000/v1/directory
"MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365"
```

### Get the directory URI by is UID

```
curl -X GET http://127.0.0.1:5000/v1/directory/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365
"ftp://127.0.1.1:2121/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365"
```
Or if you want to specify another protocol (accecpted protocl [ftp, file, http])
```
curl -X GET http://127.0.0.1:5000/v1/directory/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365/file
"file:///home/christophe/Documents/MDL/OPV/FileManager/tests/MonZolieID-1-021e88ee-d6bd-11e6-8aa9-f46d0424e365"
```

### List available protocol

```
curl -X GET  http://127.0.0.1:5000/v1/protocols
["file", "http", "ftp"]
```

### List uid

```
curl -X GET  http://127.0.0.1:5000/v1/ls
["ID-1-6f26e348-d77e-11e6-a52d-f46d0424e365"]
```

### Generate a thumbnail
The http access allow you to generate thumbnail using some http parameter.
* scale : set a scale factor, ex if scale is equal to 2, the image will be reduce by 2
* width : set image width, height will be computed
* height : set image height, width will be computed

```
curl -X GET  'http://opv_master:5000/v1/files/uuid/panorama.jpg?scale=6'
# Return cropped image
```

This parameters work on all image available thought the directory manager.

## Todo

* Add log
* Test the api
* Write a good documentation

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
