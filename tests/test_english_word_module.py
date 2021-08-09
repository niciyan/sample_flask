import unittest

from app import create_app, db
from app.models import User


class EnglishWordBasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        User.generate_test_user()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.post('/auth/login', data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/english-word/', data={
            'word': 'word',
            'meaning': 'aaa'
        }, follow_redirects=True)
        self.assertTrue(response.status_code, 200)

        response = self.client.get('/english-word/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('aaa' in response.get_data(as_text=True))
