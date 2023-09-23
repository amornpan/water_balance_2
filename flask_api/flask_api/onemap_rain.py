from datetime import datetime
import pymongo
import geopandas as gpd
import pandas as pd
import json

class OneMapRainAPI:
    def __init__(self):
        now = datetime.now()
        self.start_date = {
            "YEAR": now.year,
            "MONTH": now.month,
            "DAY": now.day
        }
        self.end_date = {
            "YEAR": now.year,
            "MONTH": now.month,
            "DAY": now.day
        }
        
        # Replace with your MongoDB server URL and credentials
        mongo_uri = "mongodb://root:pass12345@113.53.253.56:27017/"
        database_name = "water_balance_db"
        collection_name = "boundary_tb_hks0_adjusted"
        collection_onemap = "precip_onemap_khs_59TB"  # New collection name

        # Connect to MongoDB
        self.client = pymongo.MongoClient(mongo_uri)

        # Access the specified database and collection
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.collection_one = self.db[collection_onemap]  # Access the new collection

    def process_rain_data(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = self.start_date
        if end_date is None:
            end_date = self.end_date

        data_list = []

        # Query for GeoJSON data (modify the query as needed)
        query = {}
        geojson_cursor = self.collection.find(query)

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

                # Query for rain data within the custom date range and for the given TB_CODE in the new collection
                rain_query = {
                    "YEAR": {"$gte": start_date["YEAR"], "$lte": end_date["YEAR"]},
                    "MONTH": {"$gte": start_date["MONTH"], "$lte": end_date["MONTH"]},
                    "DAY": {"$gte": start_date["DAY"], "$lte": end_date["DAY"]},
                }

                # Find all documents matching the date range in the new collection
                rain_values = self.collection_one.find(rain_query)

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

        return json.dumps(geojson_data)  # Return the GeoJSON data as a JSON string

