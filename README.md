# METNO METCAP API

## Local development and testing

Both the API and the database with sample data run as
Docker containers. All tests have been done on a standard
**Ubuntu 22.04 LTS** desktop installation.

To use the API in your local environment you must: 
* install [docker](https://docker.io) and [docker-compse](https://docs.docker.com/compose/install/compose-desktop/)
* clone this repository
* cd to the top directory (where *local-dev-docker-compose.yml* and  *local-dev-initialize-database.sh* reside)
* from the command line run:
```
docker-compose -f local-dev-docker-compose.yml  up -d
```
On first run this process will take several minutes as it
builds and starts the containers. It will also create the directory
$HOME/metcap.

Once done, you should have two running Docker containers. Check that is so by executing: 

```
docker ps
```

The result should resemble:

```
CONTAINER ID   IMAGE        COMMAND                  CREATED         STATUS         PORTS     NAMES
ccb239b3371a   metcap-db    "tini -- /docker-ent…"   8 minutes ago   Up 8 minutes             metcap-db
3573ad1d00f8   metcap-api   "./run.sh"               8 minutes ago   Up 8 minutes             metcap-api

```

* Sample data can be found in the data/metcap directory

```
data
└──metcap/
    └── data_sources
        ├── norway
        │   ├── lrmap
        │   ├── map
        │   └── warnings
        └── romania
            ├── lrmap
            ├── map
            └── warnings

```

To make the sample data available from within the running containers you
must copy the entire contents of the data/metcap dirctory to $HOME/metcap. The 
tree structure must be preserved. You can do this with the following command:

```
sudo cp -r data/metcap $HOME/.
```

* Initialize the running database container with search routines and sample data:
```
./local-dev-initialize-database.sh
```

This script may take several minutes to complete after which
you will have a CouchDB container running with routines and sample 
data installed. The data is now persistent and stored under $HOME/metcap.
Subsequent sessions will use this data store. Note also that the CouchDB 
caches internal queries so the first call to an end point in the API may 
take on the order of several seconds, but subsequent calls will return 
much more quickly.

You may add more data under in the appropriate directory under $HOME/metcap 
at any time, but to upload the data to the database container you must run 
```
./local-dev-initialize-database.sh
```
again.

* You can point your browser to http://localhost:7532/api/docs#/
and you should see

![METCAP API docs](./images/00.png?raw=true "METCAP API docs")


* View the database using your web browser
```
http://localhost:5984/_utils/#
```
The user name is "admin" and the password is "password". You should see

![METCAP API database](./images/01.png?raw=true "METCAP API database")

* Stopping and restarting
The docker containers are stopped with

```
docker stop <CONTAINER ID>
```
and they can be restarted with
```
docker-compose -f local-dev-docker-compose.yml  up -d
```


* Uninstalling METCAP completely

To completely remove the METCAP installation, 
the docker containers must be stopped and all Docker resources
must be deleted. 

Data pesistance across sessions is achieved by
storing CouchDB under $HOME/metcap on first installation. This 
directory and its subdirectories must also be deleted for a 
complete removal of METCAP API.

### CAUTION: These commands will remove ALL Docker resources including containers not related to METCAP

The following commands are provided as examples only. Use them with caution.

```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a --force --volumes
sudo rm -rf $HOME/metcap
```

