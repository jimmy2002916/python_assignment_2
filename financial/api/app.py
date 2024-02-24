from datetime import datetime
import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db_path():
    current_file_path = os.path.abspath(__file__)
    api_dir = os.path.dirname(current_file_path)
    data_dir = os.path.join(api_dir, 'data')
    db_path = os.path.join(data_dir, 'financial_data.db')
    return db_path


def execute_sql_from_file(filename, connection):
    # The schema.sql file is located at the root of the project directory
    project_root = os.path.dirname(os.path.dirname(app.root_path))
    schema_path = os.path.join(project_root, filename)

    with open(schema_path, 'r') as sql_file:
        sql_script = sql_file.read()
    connection.executescript(sql_script)


def init_db():
    # Use the get_db_path function to connect to the SQLite database
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    # Execute the schema.sql file to create the tables
    execute_sql_from_file('schema.sql', conn)

    conn.commit()
    conn.close()


# Initialize the database
init_db()


def query_financial_data(start_date, end_date, symbol, limit, page):
    offset = (page - 1) * limit
    params = []
    query_parts = []

    if start_date:
        query_parts.append("date >= ?")
        params.append(start_date)
    if end_date:
        query_parts.append("date <= ?")
        params.append(end_date)
    if symbol:
        query_parts.append("symbol = ?")
        params.append(symbol)

    where_clause = " AND ".join(query_parts) if query_parts else "1 = 1"

    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get the total count of records
    count_query = f"SELECT COUNT(*) FROM financial_data WHERE {where_clause}"
    cur.execute(count_query, params)
    total_count = cur.fetchone()[0]
    total_pages = (total_count + limit - 1) // limit

    # Get the actual paginated records
    data_query = f"SELECT * FROM financial_data WHERE {where_clause} ORDER BY date LIMIT ? OFFSET ?"
    cur.execute(data_query, params + [limit, offset])
    records = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "data": records,
        "pagination": {
            "count": total_count,
            "page": page,
            "limit": limit,
            "pages": total_pages
        },
        "info": ""
    }


@app.route('/financial_data', methods=['GET'])
def financial_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    symbol = request.args.get('symbol')
    limit = request.args.get('limit', default=5, type=int)
    page = request.args.get('page', default=1, type=int)

    # Convert empty string to None to handle optional parameters
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None
    symbol = symbol.upper() if symbol else None  # Assuming symbol is case-insensitive

    # Validate date format if the date is provided
    for date_str in filter(None, [start_date, end_date]):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"data": [], "pagination": {}, "info": "Invalid date format. Use YYYY-MM-DD."}), 400

    result = query_financial_data(start_date, end_date, symbol, limit, page)
    return jsonify(result)


@app.route('/statistics', methods=['GET'])
def get_statistics():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    symbols = request.args.get('symbols').split(',')  # Assuming symbols are comma-separated

    # Validate required parameters
    if not start_date or not end_date or not symbols:
        return jsonify({"data": {}, "info": {"error": "start_date, end_date, and symbols are required"}}), 400

    try:
        # Convert and validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"data": {}, "info": {"error": "Invalid date format. Use YYYY-MM-DD."}}), 400

    db_path = get_db_path()  # Function to get the database path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Prepare response data
    response_data = {
        "start_date": start_date,
        "end_date": end_date,
        "symbols": symbols,
        "average_daily_open_price": {},
        "average_daily_close_price": {},
        "average_daily_volume": {}
    }

    for symbol in symbols:
        cur.execute('''
            SELECT
                AVG(CAST(open_price AS REAL)) AS avg_open_price,
                AVG(CAST(close_price AS REAL)) AS avg_close_price,
                AVG(CAST(volume AS REAL)) AS avg_volume
            FROM financial_data
            WHERE symbol = ? AND date BETWEEN ? AND ?
        ''', (symbol, start_date, end_date))

        row = cur.fetchone()
        response_data["average_daily_open_price"][symbol] = row["avg_open_price"] if row["avg_open_price"] is not None else 0
        response_data["average_daily_close_price"][symbol] = row["avg_close_price"] if row["avg_close_price"] is not None else 0
        response_data["average_daily_volume"][symbol] = row["avg_volume"] if row["avg_volume"] is not None else 0

    conn.close()

    return jsonify({"data": response_data, "info": {"error": ""}})


if __name__ == '__main__':
    app.run(debug=True)
