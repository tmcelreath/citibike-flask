import unittest
from app import create_app, get_mongo
from app import citibike_dao

class CitibikeDAOTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.dao = citibike_dao.CitiBikeDAO(get_mongo())

    def tearDown(self):
        pass

    def test_get_stations(self):
        dao = self.dao
        self.assertIsNotNone(dao)
        stations = dao.find_all_stations()
        self.assertIsNotNone(stations)


if __name__ == '__main__':
    unittest.main()