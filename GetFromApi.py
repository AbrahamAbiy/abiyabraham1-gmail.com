from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
requests_cache.install_cache('crime_api_cache', backend='sqlite', expire_after=36$
app = Flask(__name__)
street_url_template = 'https://data.police.uk/api/stops-street?lat={lat}&lng={lng$
@app.route('/stops-street', methods=['GET'])
def stopchart():
        my_latitude = request.args.get('lat','51.52369')
        my_longitude = request.args.get('lng','-0.0395857')
        my_date = request.args.get('date','2017-12')
        crime_url = street_url_template.format(lat = my_latitude, lng = my_longit$
        resp = requests.get(crime_url)
        if resp.ok:
                return jsonify(resp.json())
        else:
                print(resp.reason)
if __name__=="__main__":
        app.run(host='0.0.0.0', debug = True)
