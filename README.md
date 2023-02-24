# METNO METCAP API

## Local development and testing

Both the API and the database with sample data run as
Docker containers. All test have been done on a standard
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
builds the containers.

Once done, you should have two running Docker containers. Check that is so by executing: 

```
docker ps
```

The result should resemble:

```
CONTAINER ID   IMAGE        COMMAND                  CREATED        STATUS         PORTS     NAMES
fb81206ec2cf   metcap-api   "./run.sh"               20 hours ago   Up 6 minutes             metcap-api
9179a30737b3   database     "tini -- /docker-ent…"   20 hours ago   Up 6 minutes             database
```

* To add search routines and data to your running database container execute
```
./local-dev-initialize-database.sh
```

This script is run **only once** to initialize your database.
It too will take several minutes to complete at the end of which 
you will have a CouchDB container running with routines and sample 
data installed. The data is now persistent and stored under $HOME/couchdb.
Subsequent sessions will use this data store. Note also that the CouchDB 
caches internal queries so the first call to an end point in the API may 
take on the order of several seconds, but subsequent calls will return 
much more quickly.

* You can point your browser to http://localhost:7532/api/docs#/
and you should see

![METCAP API docs](./images/00.png?raw=true "METCAP API docs")


* View the database using your web browser
```
http://localhost:5984/_utils/#
```
The user name is "admin" and the password is "password". You should see

![METCAP API database](./images/01.png?raw=true "METCAP API database")

* Other examples of API use are found in the [./local-dev/demo](local-dev/demo/README.md) directory. 

* Removing the software

To completely remove the software, 
the docker containers must be stopped and all Docker resources
must be deleted. 

Data pesistance across sessions is achieved by
storing CouchDB under $HOME/couchdb on first installation. This 
directory and its subdirectories must also be deleted for a 
complete removal of METCAP API.

### CAUTION: These command will remove ALL Docker resources

The following commands are provided as examples only. Use them with caution.

```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a --force --volumes
rm -rf $HOME/couchdb
```

