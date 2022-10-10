# weamyl-metcap

## To setup 

* clone this repository to your develepment machine
```
git clone ....
```

* install docker
```
sudo apt-get install docker.io
```

* install docker-compose
```
sudo apt-get install docker-compose
```

* add your user to the docker group in /etc/group

* cd to the metcap-api directory and run
```
docker-compose up
```

Your first run of docker-compose will take some time since images have to be downloaded, built and database populated.
