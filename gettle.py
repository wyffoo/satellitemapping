import mysql.connector
import re
import requests

# Replace these values with your MySQL server information
db_config = {
    'user': 'root',
    'database': 'satellitedata'
}

def get_tle_data(catalog_number):
    # Fetch TLE data from Celestrak using the specified catalog number
    base_url = "https://celestrak.org/NORAD/elements/gp.php"
    query_params = {
        "CATNR": catalog_number,
        "FORMAT": "TLE"
    }

    response = requests.get(base_url, params=query_params)
    
    if response.status_code == 200:
        tle_data = response.text
        return tle_data
    else:
        print(f"Error: Unable to fetch TLE data. Status Code: {response.status_code}")
        return None

def parse_tle(tle_data):
    # Parse TLE data and extract relevant information
    lines = tle_data.strip().split('\n')
    
    satellite_name = lines[0].strip()

    # Find the line containing NORAD catalog number
    norad_line = next((line for line in lines if line.startswith('1 ')), None)
    if norad_line is None:
        print("Error: NORAD line not found.")
        return None
    
    norad_catalog_number = int(norad_line[2:7])  # Extract the NORAD catalog number part
    
    # Get the third line of the TLE; return an error if not found
    tle_line = next((line for line in lines if line.startswith('2 ')), None)
    if tle_line is None:
        print("Error: TLE line not found.")
        return None

    values = tle_line[2:].split()
    
    # Validate if there are enough values in the TLE line
    if len(values) < 7:
        print("Error: Not enough values in TLE line.")
        print("Line content:", tle_line)
        print("Split values:", values)
        return None

    # Extract values from the TLE line
    epoch_date, bstar_drag, inclination, right_ascension, eccentricity, \
    perigee_argument, mean_anomaly = map(float, values[:7])  # Extract the first 7 values

    # Add the following debug statements in the parse_tle function
    print("Satellite Name:", satellite_name)
    print("TLE Line:", tle_line)
    print("Split values:", values)
    print("Type of epoch_date:", type(epoch_date))
    print("Type of bstar_drag:", type(bstar_drag))
    print("Type of inclination:", type(inclination))
    print("Type of right_ascension:", type(right_ascension))
    print("Type of eccentricity:", type(eccentricity))
    print("Type of perigee_argument:", type(perigee_argument))
    print("Type of mean_anomaly:", type(mean_anomaly))
    

    return {
        'SatelliteName': satellite_name,
        'NoradCatalogNumber': norad_catalog_number,
        'EpochDate': epoch_date,
        'BStarDrag': bstar_drag,
        'Inclination': inclination,
        'RightAscensionOfAscendingNode': right_ascension,
        'Eccentricity': eccentricity,
        'ArgumentOfPerigee': perigee_argument,
        'MeanAnomaly': mean_anomaly
    }

# Get TLE data for the International Space Station (ISS) with catalog number 25544
iss_tle = get_tle_data(25544)

if iss_tle is not None:
    tle_data = parse_tle(iss_tle)

    # Connect to the MySQL server
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert data into the SatelliteTLE table
    insert_query = """
        INSERT INTO SatelliteTLE (
            SatelliteName, NoradCatalogNumber,
            EpochDate, BStarDrag, Inclination,
            RightAscensionOfAscendingNode, Eccentricity, ArgumentOfPerigee,
            MeanAnomaly
        ) VALUES (
            %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s
        )
    """

    cursor.execute(insert_query, (
        tle_data['SatelliteName'],
        tle_data['NoradCatalogNumber'],
        tle_data['EpochDate'],
        tle_data['BStarDrag'],
        tle_data['Inclination'],
        tle_data['RightAscensionOfAscendingNode'],
        tle_data['Eccentricity'],
        tle_data['ArgumentOfPerigee'],
        tle_data['MeanAnomaly']
    ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
