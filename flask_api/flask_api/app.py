from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS class
from onemap_rain import OneMapRainAPI  # Import the OneMapRainAPI class

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

@app.route('/get_rain_data', methods=['GET'])
def get_rain_data():
    start_year = request.args.get('start_year')
    start_month = request.args.get('start_month')
    start_day = request.args.get('start_day')
    end_year = request.args.get('end_year')
    end_month = request.args.get('end_month')
    end_day = request.args.get('end_day')

    start_date = {
        "YEAR": int(start_year),
        "MONTH": int(start_month),
        "DAY": int(start_day)
    }

    end_date = {
        "YEAR": int(end_year),
        "MONTH": int(end_month),
        "DAY": int(end_day)
    }

    api_instance = OneMapRainAPI()
    geojson_data = api_instance.process_rain_data(start_date, end_date)
    return geojson_data
    #return jsonify(geojson_data)

@app.route('/get_geojson_data', methods=['GET'])
def get_geojson_data():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)

        # Access the specified database and collection
        db = client[database_name]
        collection = db[collection_name]

        # Query for GeoJSON data (modify the query as needed)
        query = {}
        geojson_cursor = collection.find(query)

        # Convert the GeoJSON cursor to a list of dictionaries
        geojson_list = list(geojson_cursor)

        # Create an empty list to store features
        features = []

        # Iterate through the features in the GeoJSON list
        for feature in geojson_list[0]['features']:  # Access the 'features' list within the first element
            properties = feature['properties']

            # Check if "geometry" field exists and is not None
            if 'geometry' in feature and feature['geometry']:
                coordinates = feature['geometry']['coordinates']  # Extract coordinates array

                # Create a feature dictionary
                feature_dict = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": coordinates
                    },
                    "properties": properties
                }

                # Extract the TB_CODE
                tb_code = properties.get("TB_CODE")

                # Query for rain data within the custom date range and for the given TB_CODE
                rain_query = {
                    "YEAR": {"$gte": start_date["YEAR"], "$lte": end_date["YEAR"]},
                    "MONTH": {"$gte": start_date["MONTH"], "$lte": end_date["MONTH"]},
                    "DAY": {"$gte": start_date["DAY"], "$lte": end_date["DAY"]},
                }

                # Find all documents matching the date range
                rain_values = collection.find(rain_query)

                # Initialize total rain for the current polygon
                total_rain = 0

                # Iterate through rain values for the current polygon
                for rain_data in rain_values:
                    total_rain += rain_data[tb_code]

                # Add the accumulated rain value as a property
                feature_dict["properties"]["Accumulated_Rain"] = total_rain

                features.append(feature_dict)

        # Create a GeoJSON structure
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }

        return jsonify(geojson_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)

