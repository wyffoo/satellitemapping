1.Setup Database:

Execute the SQL scripts in the sql directory to create the necessary database and tables.
Modify the database configuration in app.py and getommtle.py according to your MySQL server setup.
2.Run the Application:

Run app.py to start the Flask web application.
Access the application at http://127.0.0.1:5000/ in your web browser.
Fetch Satellite Data:

Run getommtle.py to fetch TLE data for a specific satellite catalog number and insert it into the database.
View Satellite Tracking:

3.Open mapping.html in a web browser to view the rotating globe with orbiting lights.
The application will display latitude and longitude information on click and show real-time satellite data fetched from the local API.