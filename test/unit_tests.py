import urllib2
from flask import Flask
import unittest
from flask.ext.testing import TestCase

class MyTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_api_get_station(self):
        response = urllib2.urlopen(self.get_station_api_url())
        self.assertEqual(response.code, 200)

    def test_api_get_station_id(self):
        response = urllib2.urlopen(self.get_station_id_api_url(79))
        self.assertEqual(response.code, 200)

    def get_server_url(self):
        return 'http://localhost:5000/'

    def get_station_api_url(self):
        return self.get_server_url, 'api/station/'

    def get_station_id_api_url(self, station_id):
        return self.get_station_api_url(), station_id

if __name__ == '__main__':
    unittest.main()