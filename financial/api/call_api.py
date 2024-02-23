import requests
import os
import sqlite3
import json

from financial.sql.sql_helper import execute_sql_from_file

def get_stock_data(symbol):
    API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')  # Ensure the API key is set in your environment variables
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        raw_data = response.json()

        # Extract the daily time series data
        time_series_data = raw_data.get("Time Series (Daily)", {})

        # Prepare the data for JSON file and SQLite insertion
        processed_data = []
        for date, daily_values in time_series_data.items():
            processed_data.append({
                "symbol": symbol,
                "date": date,
                "open_price": str(daily_values["1. open"]),
                "close_price": str(daily_values["4. close"]),
                "volume": str(daily_values["5. volume"])
            })

        # Write the processed data to a JSON file
        output_file = f"{symbol}_data.json"
        with open(output_file, 'w') as file:
            json.dump(processed_data, file, indent=4)
        print(f"Data for {symbol} saved to {output_file}")

        # Connect to SQLite database
        conn = sqlite3.connect('financial_data.db')

        # Execute SQL from schema.sql to create the financial_data table
        execute_sql_from_file('schema.sql', conn)

        # Insert the processed data into the SQLite database
        for data in processed_data:
            # Insert or ignore to avoid duplicates
            conn.execute('''
            INSERT OR IGNORE INTO financial_data (symbol, date, open_price, close_price, volume)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                data["symbol"],
                data["date"],
                data["open_price"],
                data["close_price"],
                data["volume"]
            ))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()
        print(f"Data for {symbol} saved to the SQLite database.")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")

