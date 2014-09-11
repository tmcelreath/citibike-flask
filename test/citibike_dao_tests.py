import os
import unittest
import logging
from app import create_app, get_mongo
from app import citibike_dao

class CitibikeDAOTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.dao = citibike_dao.CitiBikeDAO(get_mongo())
        self.station_id=79

    def tearDown(self):
        pass

    def test_get_stations(self):
        test_name='test_get_stations'
        stations = self.dao.find_all_stations()
        self.assertIsNotNone(stations)
        self.assertGreater(len(stations), 300)

    def test_find_station_by_id(self):
        test_name='test_find_station_by_id'
        msg_invalid_id='{}: Returned station ID "{}" is invalid.'
        msg_missing_field='{}: Required field "{}" does not exist.'
        station = self.dao.find_station_by_id(self.station_id)
        self.assertIsNotNone(station)
        self.assertIsNotNone(station['lat'], msg_missing_field.format(test_name, 'lat'))
        self.assertIsNotNone(station['lon'], msg_missing_field.format(test_name, 'lon'))
        self.assertIsNotNone(station['name'], msg_missing_field.format(test_name, 'name'))
        logging.debug('{}: Station={}'.format(test_name, station))
        self.assertEqual(station['id'], self.station_id, msg_invalid_id.format(test_name, station['id']))

    def test_find_stations_by_geo_location(self):
        test_name='test_find_stations_by_geo_location'
        lat = 40.748238
        lon = -73.978311
        radius = 1000
        limit = 3
        stations = self.dao.find_stations_by_geo_location(lon, lat, radius, limit)
        self.assertEqual(len(stations), limit)
        ''' Set limit to 1. Result should be 1. '''
        stations = self.dao.find_stations_by_geo_location(lon, lat, radius, 1)
        self.assertEqual(len(stations), 1)
        ''' Set lat/lon to 0. Result should be 0. '''
        stations = self.dao.find_stations_by_geo_location(0, 0, radius, limit)
        self.assertEqual(len(stations), 0)
        ''' Set radius to 1, limit to 3. Result should be 1. '''
        stations = self.dao.find_stations_by_geo_location(lon, lat, 1, limit)
        self.assertEqual(len(stations), 1)

    def test_get_station_averages(self):
        test_name='test_get_station_averages'
        stations = self.dao.get_station_averages([self.station_id], 12, [1])
        self.assertEqual(len(stations), 2)
        self.assertEqual(stations['result'][0]['_id'], self.station_id)
        self.assertIsNotNone(stations['result'][0]['avgBike'])
        self.assertIsNotNone(stations['result'][0]['avgDock'])
        stations = self.dao.get_station_averages([72, 79], 12, [1])
        self.assertIsNotNone(stations['result'][0]['avgBike'])
        self.assertIsNotNone(stations['result'][0]['avgDock'])
        self.assertIsNotNone(stations['result'][1]['avgBike'])
        self.assertIsNotNone(stations['result'][1]['avgDock'])

    def test_get_rides_by_bike_id(self):
        test_name='test_get_rides_by_bike_id'
        rides = self.dao.get_rides_by_bike_id('16848', '20140501', '20140502')
        #self.assertGreater(len(rides), 5)

if __name__ == '__main__':
    unittest.main()

