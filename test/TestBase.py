from flask_testing import TestCase
from webapp import app
import unittest


class BaseTestCase(TestCase):
    TESTING = True
    def create_app(self):
        return app

