from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS class

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app


@app.route('/')
def hello():
    return "hello"

@app.route('/geojson')
def get_geojson():
    # Replace this with your actual GeoJSON data or generate it dynamically.
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-74.17236328125, 40.64816265380517],
                            [-74.063720703125, 40.60016806609175],
                            [-73.99658203125, 40.69628791148941],
                            [-74.0869140625, 40.73349276195103],
                            [-74.17236328125, 40.64816265380517]
                        ]
                    ]
                },
                "properties": {
                    "name": "Sample Polygon"
                }
            }
        ]
    }
    return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051, debug=True)

