from datetime import datetime, timedelta
import requests
import os
import sqlite3
import json


def execute_sql_from_file(filename, connection):
    # Open and read the file as a single buffer
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()
    connection.executescript(sql_script)


def get_stock_data(symbols):
    API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
    base_url = "https://www.alphavantage.co/query"

    # Calculate date range for the last two weeks
    end_date = datetime.today()
    start_date = end_date - timedelta(weeks=2)

    data_dir = 'financial/data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    conn = sqlite3.connect(f'{data_dir}/financial_data.db')

    execute_sql_from_file('schema.sql', conn)

    for symbol in symbols:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": API_KEY
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            raw_data = response.json()

            time_series_data = raw_data.get("Time Series (Daily)", {})

            processed_data = []
            for date_str, daily_values in time_series_data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if start_date <= date <= end_date:
                    processed_data.append({
                        "symbol": symbol,
                        "date": date_str,
                        "open_price": str(daily_values["1. open"]),
                        "close_price": str(daily_values["4. close"]),
                        "volume": str(daily_values["5. volume"])
                    })

            for data in processed_data:
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

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else: {err}")

    conn.commit()
    conn.close()


symbols = ['IBM', 'AAPL']
get_stock_data(symbols)
