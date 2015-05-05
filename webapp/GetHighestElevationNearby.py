"""
Created on 300315
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""
from flask import Blueprint, request, abort, jsonify
from app import GetData
HIGH_ELE = Blueprint("HIGH_ELE", __name__)

@HIGH_ELE.route('/dtm/v1/highestelevationnearby', methods=['GET'])
def highest_elevation_nearby():
    """
    This function will GET the url variable and assign
    it to the relevant variable before calling the GetData
    function retrieve_highest_point to get the height of
    the highest point within the radius of the area
    """
    if request.args.get('lon'):
        x_value = request.args.get('lon')
    else:
        abort(400)
    if request.args.get('lat'):
        y_value = request.args.get('lat')
    else:
        abort(400)
    if request.args.get('radius'):
        radius = request.args.get('radius')
    else:
        abort(400)
    if 120 < int(radius) < 2100:
        data = GetData.retrieve_highest_point(
            float(x_value), float(y_value), int(radius))
        return jsonify(type="Point", coordinates=data)
    else:
        return 'Radius must be in between 120 and 2100'


