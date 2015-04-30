'''
Created on 30 April 2015
Created by Eugene Phua
'''
from flask import *

from GetHeight import ele
from GetHighestElevationNearby import highele


app = Flask(__name__)
app.register_blueprint(ele)
app.register_blueprint(highele)
