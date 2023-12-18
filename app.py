from flask import Flask
import mysql.connector
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'user': 'root',           # Your MySQL username
    'database': 'satellitedata'  # Your MySQL database name
}

# API endpoint to retrieve satellite data
@app.route('/api/satellite_data')
def get_satellite_data():
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # SQL query to select all data from the SatelliteTLE table
    query = "SELECT * FROM SatelliteTLE"
    cursor.execute(query)

    # Fetch all the data from the query result
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the data to JSON format and return as a response
    return jsonify(data)

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
