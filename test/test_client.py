import unittest
from app import create_app

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_add('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_home_page(self):
        response = client.get(url_for('main.index'))
