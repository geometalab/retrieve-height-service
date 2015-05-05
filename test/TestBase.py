"""
Created on 280415
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""
from flask_testing import TestCase
from webapp import app
import unittest


class BaseTestCase(TestCase):
    TESTING = True

    def create_app(self):
        return app

