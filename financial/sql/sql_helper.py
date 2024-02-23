def execute_sql_from_file(filename, connection):
    # Open and read the file as a single buffer
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()
    # Execute the SQL commands
    connection.executescript(sql_script)