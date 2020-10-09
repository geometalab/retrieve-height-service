"""
Created on 230315
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""
import os
from webapp import app
import unittest
import flask_testing
from raven.contrib.flask import Sentry

sentry = Sentry()  # automatically reads 'SENTRY_DSN' if set

if __name__ == '__main__':
    sentry.init_app(app)
    app.run('0.0.0.0', port=5000, debug=bool(os.environ.get('DEBUG')))
    app.config['TESTING'] = True
    unittest.main()
