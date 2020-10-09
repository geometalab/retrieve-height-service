"""
Created on 230315
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""

from flask import Flask
from .GetHeight import ELE
from .GetHighestElevationNearby import HIGH_ELE


app = Flask(__name__)
app.register_blueprint(ELE)
app.register_blueprint(HIGH_ELE)
