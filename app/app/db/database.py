
import yaml
import requests
import logging
from http import HTTPStatus
import os


class Database():
    """
    Handles basic connection and CRUD for CouchDB
    """
    # TODO The etc directory and config files must be placed under /opt/weamyl and environment set to show where they are
    # The config is not distributed. File must be kept safe. 
    configFileDefault = "/opt/metcap/etc/config.yml"
    configFile = os.environ.get('METCAP_CONFIG_FILE', configFileDefault)
    # def __init__(self, configFile="/opt/metcap/etc/config.yml"):
    def __init__(self, configFile=configFile):
        self.configFile = configFile
        with open(configFile) as file:
            try:
                self.mycnf = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)
        self.mapDb = self.mycnf['couchDb']['mapDb']
        self.capDb = self.mycnf['couchDb']['capDb']
        self.lrmapDb = self.mycnf['couchDb']['lrmapDb']
        self.customMapDb = self.mycnf['couchDb']['customMapDb']

    def check_database(self):
        """
        Check if database is accessible
        """
        try:
            self.initialized = True
            self.status_code = 200
            self.couchDb_url = '{}://{}:{}@{}:{}'.format(
                                            self.mycnf['couchDb']['protocol'],
                                            self.mycnf['couchDb']['username'],
                                            self.mycnf['couchDb']['password'],
                                            self.mycnf['couchDb']['FQDN'],
                                            self.mycnf['couchDb']['port']
                                            )
            request_response = requests.head(self.couchDb_url, timeout=3.0)
            request_response.raise_for_status()
        # TODO assign correct exception for missing config key/value
        except Exception as e:
            logging.warning("""Configuration file does not contain
                            the sections or keywords requested""")
            self.status_code = 204
            self.initialized = False
        except requests.exceptions.Timeout as e:
            print("Timeout error")
            logging.error("""Http request to database timed out
                          with error message: {}""".format(e))
            self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.initialized = False
        except requests.exceptions.ConnectionError as e:
            print("connection error")
            logging.error("""Failed to connect to database
                          with error message: {}""".format(e))
            self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.initialized = False
        except requests.exceptions.HTTPError as e:
            logging.error("""Http request to database failed
                          with error message: {}""".format(e))
            self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.initialized = False
        except Exception as e:
            logging.error("""Exception occured during request
                          to database with error message: {}""".format(e))
            self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.initialized = False

    def get(self, query):
        """
        Function that handles http requests
        with method "GET" to couchDb

        Arguments:
        ----------
        query: string
            end of url for requests to couchDb

        Returns:
        ---------
        content: response
            response for the http get request
        status code: int
            status code for the http get request
            to couchDb
        """
        self.check_database()
        if not self.initialized:
            return("", self.status_code)
        url = self.couchDb_url + query
        try:
            content = requests.get(url)
            status = content.status_code
            return(content, status)
        except Exception as err:
            logging.warn(f'Exception in get {str(err)}')
            return(str(err), HTTPStatus.INTERNAL_SERVER_ERROR.value)

    def put(self, query, data, content_type="application/json"):
        """
        Function the handles http requests
        with method "PUT" to couchDb

        Arguments:
        ----------
        query: string
            end of url for requests to couchDb
        data: json
            content to be uploaded to database
        content_type: string
            content type for data to be uploaded

        """
        self.check_database()
        if not self.initialized:
            return("", self.status_code)
        headers = {"Content-type": content_type}
        try:
            url = self.couchDb_url + query
            if content_type == "text/xml":
                r = requests.put(url, data=data, headers=headers)
            else:
                r = requests.put(url, json=data, headers=headers)
        except Exception as err:
            logging.warn(f'Exception in put {str(err)}')
            return(str(err), HTTPStatus.INTERNAL_SERVER_ERROR.value)
        return(r.status_code)

    def post(self, query, data):
        """
        Function handles http requests
        with method "POST" to couchDb

        Arguments:
        ----------
        query: string
            end of url for requests to couchDb
        data: json
            content to be uploaded to database
        content_type: string
            content type for data to be uploaded

        Returns:
        --------
        status: int
            Status code of http request to database
        """

        self.check_database()
        if not self.initialized:
            return(self.status_code)
        headers = {'Content-type': 'application/json'}
        try:
            url = self.couchDb_url + query
            r = requests.post(url, json=data, headers=headers)
        except Exception as err:
            logging.warn(f'Exception in post {str(err)}')
            return(HTTPStatus.INTERNAL_SERVER_ERROR.value)
        return(r.status_code)

    def delete(self, query):
        """
        Function handles http requests
        with method "DELETE" to couchDb

        Arguments:
        -----------
        query: string
            end of url for requests to couchDb

        Returns:
        --------
        status: int
            Status code of http request to database
        """
        self.check_database()
        if not self.initialized:
            return(self.status_code)
        try:
            url = self.couchDb_url + query
            r = requests.delete(url)
        except Exception as err:
            logging.warn(f'Exception in delete {str(err)}')
            return HTTPStatus.INTERNAL_SERVER_ERROR.value
        return(r.status_code)

    def createDb(self, query):
        self.check_database()
        if not self.initialized:
            return(self.status_code)
        try:
            url = self.couchDb_url + query
            r = requests.put(url)
        except Exception as e:
            logging.warn(f'Exception in pub {str(e)}')
            return HTTPStatus.INTERNAL_SERVER_ERROR.value
        return(r.status_code)

    def save(self, db, id, data):
        self.db = db
        self.id = id
        self.data = data
        self.check_database()
        if not self.initialized:
            return(self.status_code)
        try:
            r = requests.put(f'{self.couchDb_url}/{self.db}/{self.id} / put', data={self.data})
        except Exception as e:
            logging.warn(f'Exception in pub {str(e)}')
            return HTTPStatus.INTERNAL_SERVER_ERROR.value
        return(r.status_code)

couch = Database()
