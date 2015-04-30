'''
Created on 28 March 2015
Created by Eugene Phua
'''

from flask import *
import jinja2, os
from app import GetData

ele = Blueprint("ele", __name__)

@ele.route('/dtm/v1/elevation', methods=['GET'])
def elevation():
    if request.args.get('lon'):
        x = request.args.get('lon')
    else:
        abort(400)
    if request.args.get('lat'):
        y = request.args.get('lat')
    else:
        abort(400)
    if request.args.get('format'):
        f = request.args.get('format')
    else:
        f='geojson'
    elevation= GetData.retrieveband(float(x),float(y))
    data = [float(x), float(y), int(elevation)]
    if f.lower()=='json':
        return jsonify(coordinates=data)
    elif f.lower()=='raw':
        return str(data)
    else:
        return jsonify(type="Point",coordinates=data)



