"""
Created on 230315
Created by Phua Joon Kai Eugene
Last Modification on 050515
"""
from flask import Blueprint, request, abort, jsonify
from app import GetData
ELE = Blueprint("ELE", __name__)


@ELE.route('/dtm/v1/elevation', methods=['GET'])
def elevation():
    """
    This function will GET the url variable and assign
    it to the relevant variable before calling the GetData
    function retrieve_band to get the height of the data
    """
    if request.args.get('lon'):
        x_value = request.args.get('lon')
    else:
        abort(400)
    if request.args.get('lat'):
        y_value = request.args.get('lat')
    else:
        abort(400)
    if request.args.get('format'):
        output_type = request.args.get('format')
    else:
        output_type = 'geojson'
    height = GetData.retrieve_band(float(x_value), float(y_value))
    data = [float(x_value), float(y_value), int(height)]
    if output_type.lower() == 'json':
        return jsonify(coordinates=data)
    elif output_type.lower() == 'raw':
        return str(data)
    else:
        return jsonify(type="Point", coordinates=data)




