from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS class
from onemap_rain import OneMapRainAPI  # Import the OneMapRainAPI class
from tambon import Tambon
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta

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

# -----------------------------------------------------------------------------------------------------------

# Define a function to calculate the average sum of columns
def calculate_average_sum_of_columns():
    # Connect to your MongoDB instance
    client = MongoClient("mongodb://root:pass12345@113.53.253.56:27017/")
    db = client.water_balance_db

    # Specify the collection name
    collection_name = "precip_onemap_khs_43MB"

    # Fetch the data from the MongoDB collection
    cursor = db[collection_name].find({})

    # Convert the cursor to a list of dictionaries
    data = list(cursor)

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data)

    # Find the latest year in the dataset
    latest_year = df['YEAR'].max()

    # Calculate the date 6 months ago from today
    six_months_ago = datetime.now() - timedelta(days=30 * 6)

    # Use boolean indexing to select rows with the latest year and last 6 months
    selected_df = df[(df['YEAR'] == latest_year) & (df['MONTH'] >= six_months_ago.month)]

    # Select columns to sum (exclude 'YEAR', 'MONTH', 'DAY', and '_id')
    columns_to_sum = [col for col in selected_df.columns if col not in ['YEAR', 'MONTH', 'DAY', '_id']]

    # Calculate the sum for each column
    column_sums = selected_df[columns_to_sum].sum()

    # Calculate the average sum of columns
    average_sum_of_columns = column_sums.mean()

    return average_sum_of_columns

@app.route('/onemap_avg_rain_lasted_6_months', methods=['GET'])
def get_onemap_avg_rain_lasted_6_months():
    average_sum = calculate_average_sum_of_columns()
    return jsonify({'average_sum_of_columns': average_sum})

# -----------------------------------------------------------------------------------------------------------

@app.route('/api/tambon_rainfall_data', methods=['GET'])
def tambon_get_rainfall_data():
    api_instance = Tambon()
    geojson_data = api_instance.tambon_get_rainfall_data()
    return geojson_data

# -----------------------------------------------------------------------------------------------------------

@app.route('/api/rainfall_data', methods=['GET'])
def get_rainfall_data():
    # Connect to your MongoDB instance
    client = MongoClient("mongodb://root:pass12345@113.53.253.56:27017/")  # Replace with your MongoDB connection string
    db = client.water_balance_db  # Replace with your database name

    # Specify the collection name
    collection_name = "precip_onemap_khs_43MB"

    # Fetch the data from the MongoDB collection
    cursor = db[collection_name].find({})  # Retrieve all documents in the collection

    # Convert the cursor to a list of dictionaries
    data = list(cursor)

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data)

    # Find the latest year in the dataset
    latest_year = df['YEAR'].max()

    # Calculate the date 6 months ago from today
    six_months_ago = datetime.now() - timedelta(days=30 * 6)

    # Use boolean indexing to select rows with the latest year and last 6 months
    selected_df = df[(df['YEAR'] == latest_year) & (df['MONTH'] >= six_months_ago.month)]

    # Select columns to sum (exclude 'YEAR', 'MONTH', 'DAY', and '_id')
    columns_to_sum = [col for col in selected_df.columns if col not in ['YEAR', 'MONTH', 'DAY', '_id']]

    # Create a new column 'SUM_RAIN' containing the sum of selected columns for each row
    selected_df['SUM_RAIN'] = selected_df[columns_to_sum].sum(axis=1)

    # Group the data by month and calculate the sum of 'SUM_RAIN' for each month
    monthly_sum = selected_df.groupby(['YEAR', 'MONTH'])['SUM_RAIN'].sum().reset_index()

    # Create a new column 'x_axis' for plotting
    monthly_sum['x_axis'] = monthly_sum['YEAR'].astype(str) + '-' + monthly_sum['MONTH'].astype(str)

    # Prepare the JSON data for response
    data_for_chartjs = {
        'x_axis': monthly_sum['x_axis'].tolist(),
        'SUM_RAIN': monthly_sum['SUM_RAIN'].tolist()
    }

    return jsonify(data_for_chartjs)

# -----------------------------------------------------------------------------------------------------------

@app.route('/tambon_get_chart_data_table', methods=['GET'])
def tambon_get_chart_data_table():
    api_instance = Tambon()
    _data = api_instance.tambon_get_chart_data_table()
    return _data


# -----------------------------------------------------------------------------------------------------------

@app.route('/get_chart_data_table', methods=['GET'])
def get_chart_data_table():
    # Connect to your MongoDB instance
    client = MongoClient("mongodb://root:pass12345@113.53.253.56:27017/")
    db = client.water_balance_db  # Replace with your database name

    # Specify the collection name
    collection_name = "Metadata_Mooban_43Tambon"

    # Fetch the data from the MongoDB collection
    cursor = db[collection_name].find({})  # Retrieve all documents in the collection

    # Convert the cursor to a list of dictionaries
    data = list(cursor)

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data)

    # Rename the columns
    df = df.rename(columns={"หมู่บ้าน": "Mooban", "AREA (Sq": "AREA"})

    # Select the desired columns
    selected_columns = ["CODE_Mooban", "Mooban", "Tambon", "Amphoe", "Changwat", "AREA"]

    # Create a new DataFrame with only the selected columns
    selected_df = df[selected_columns]

    selected_df.loc[:, "AREA"] = selected_df["AREA"].apply(lambda x: float(x.get('m)')))

    # Convert the DataFrame to a JSON object and set the content type
    chart_data = selected_df.to_json(orient='records', force_ascii=False, default_handler=str)
    response = app.response_class(
        response=chart_data,
        status=200,
        mimetype='application/json; charset=utf-8'  # Set the charset to UTF-8
    )

    return response

# -----------------------------------------------------------------------------------------------------------

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
    


# Tambon ------------------------------------------
@app.route('/tambon_avg_rain', methods=['GET'])
def tambon_avg_rain():
    api_instance = Tambon()
    average_sum = api_instance.calculate_average_sum_of_columns()
    return jsonify({'average_sum_of_columns': average_sum})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)

