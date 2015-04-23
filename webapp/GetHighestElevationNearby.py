from flask import *
import jinja2, os
from app import GetData


highele = Blueprint("highele", __name__)

@highele.route('/dtm/v1/highestelevationnearby', methods=['GET'])
def highestelevationnearby():
    if request.args.get('lon'):
        x = request.args.get('lon')
    else:
        abort(400)
    if request.args.get('lat'):
        y = request.args.get('lat')
    else:
        abort(400)
    if request.args.get('radius'):
        r = request.args.get('radius')
    else:
        abort(400)
    data = GetData.retrieveHighPoint(float(x),float(y),int(r))

    if int(r)>2100:
        return 'r is too large of a radius'
    elif int(r)<120:
        return 'r is too small of a radius'
    else:
        return jsonify(type="Point", coordinates=data)

