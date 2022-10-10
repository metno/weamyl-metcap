# from the command line in this dirctory run:
#
# docker build -t dev-couchdb .
# docker run -d -p 5984:5984 dev-couchdb
FROM couchdb

COPY config/local.ini /opt/couchdb/etc/
COPY config/config.yml /opt/couchdb/etc/
