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

