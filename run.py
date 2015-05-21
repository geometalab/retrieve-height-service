"""
Created on 230315
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""
from webapp import app
import unittest
import flask_testing

if __name__ == '__main__':
    app.run('0.0.0.0', port=55555)
    app.run('0.0.0.0', debug=True)
    app.config['TESTING'] = True
    unittest.main()
