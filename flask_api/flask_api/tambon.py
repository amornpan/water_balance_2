import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta

class Tambon:
    def __init__(self):
        pass
     
     # Define a function to calculate the average sum of columns
    def calculate_average_sum_of_columns(self):
        # Connect to your MongoDB instance
        client = MongoClient("mongodb://root:pass12345@113.53.253.56:27017/")
        db = client.water_balance_db

        # Specify the collection name
        collection_name = "precip_onemap_khs_59TB"

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
    
    def tambon_get_chart_data_table(self):
        # Connect to your MongoDB instance
        client = MongoClient("mongodb://root:pass12345@113.53.253.56:27017/")
        db = client.water_balance_db  # Replace with your database name

        # Specify the collection name
        collection_name = "Metadata_59Tambon"

        # Fetch the data from the MongoDB collection
        cursor = db[collection_name].find({})  # Retrieve all documents in the collection

        # Convert the cursor to a list of dictionaries
        data = list(cursor)

        # Create a pandas DataFrame from the data
        df = pd.DataFrame(data)

        # Rename the columns
        df = df.rename(columns={"Sum of AREA (Sq": "AREA"})

        # Select the desired columns
        selected_columns = ["Code_Tambon", "TB_NAME", "AMP_NAME", "PRV_NAME", "AREA"]

        # Create a new DataFrame with only the selected columns
        selected_df = df[selected_columns]

        selected_df.loc[:, "AREA"] = selected_df["AREA"].apply(lambda x: float(x.get('m)')))

        # Convert the DataFrame to a JSON object and set the content type
        chart_data = selected_df.to_json(orient='records', force_ascii=False, default_handler=str)

        # Encode the JSON data with UTF-8 encoding
        chart_data_utf8 = chart_data.encode('utf-8')

        return chart_data_utf8
    

    
    def tambon_get_rainfall_data(self):
        # Connect to your MongoDB instance
        client = MongoClient("mongodb://root:pass12345@113.53.253.56:27017/")  # Replace with your MongoDB connection string
        db = client.water_balance_db  # Replace with your database name

        # Specify the collection name
        collection_name = "precip_onemap_khs_59TB"

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

        return data_for_chartjs

