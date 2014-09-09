import unittest
import json
from app import create_app

class APITestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.client = app.test_client()

        self.test_station = '367'
        self.test_bike = ''
        self.test_lat = '40.748238'
        self.test_lon = '-73.978311'
        self.test_radius = '1000'
        self.test_limit = '2'

        self.api_urls = {
            'station': '/api/station/',
            'station_geo': '/api/station/geosearch/?lat={}&lon={}&radius={}&limit={}'.format(self.test_lat, self.test_lon, self.test_radius, self.test_limit),
            'station_rides': '/api/station/{}/rides?start_date=20140501&end_date=20140502'.format(self.test_station),
            'station_id': '/api/station/{}/'.format(self.test_station),
            'station_avg': '/api/station/{}/avg?hour=12&day=1'.format(self.test_station),

            }
        self.api_headers =  [('Content-Type', 'application/json')]

    def tearDown(self):
        pass

    def test_api_urls_ping(self):
        for key, value in self.api_urls.items():
            response = self.client.get(value, self.api_headers)
            self.assertEqual(response.status_code, 200)

    def test_404(self):
        response = self.client.get(
            '/api/station/XXX',
            headers=self.get_api_headers())
        self.assertTrue(response.status_code == 404)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'not found')


    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

if __name__ == '__main__':
    unittest.main()