from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

# Database connection details
server = 'your_server_name'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'
driver = 'ODBC Driver 17 for SQL Server'

# Establishing a connection to the database
conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")

@app.route('/query', methods=['POST'])
def query_database():
    try:
        data = request.get_json()
        sql_query = data['query']

        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        # Constructing the response
        response = []
        for row in results:
            row_dict = {}
            for i in range(len(columns)):
                row_dict[columns[i]] = row[i]
            response.append(row_dict)

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
