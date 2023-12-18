import requests
import xml.etree.ElementTree as ET
import pandas as pd
import mysql.connector
from mysql.connector import Error

def fetch_celestrak_omm_data(catnr):
    # Fetch OMM data from Celestrak using the specified catalog number
    base_url = "https://celestrak.org/NORAD/elements/gp.php"
    params = {'CATNR': catnr, 'FORMAT': 'XML'}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.text

def parse_omm_data(omm_data):
    # Parse OMM data and extract relevant information
    root = ET.fromstring(omm_data)
    satellite_data = root.find('.//metadata')

    satellite_info = {
        'object_name': satellite_data.find('OBJECT_NAME').text,
        'object_id': satellite_data.find('OBJECT_ID').text,
        'center_name': satellite_data.find('CENTER_NAME').text,
        'ref_frame': satellite_data.find('REF_FRAME').text,
        'time_system': satellite_data.find('TIME_SYSTEM').text,
        'mean_element_theory': satellite_data.find('MEAN_ELEMENT_THEORY').text
    }

    orbit_data = root.find('.//data/meanElements')

    orbit_info = {
        'epoch': pd.to_datetime(orbit_data.find('EPOCH').text),
        'mean_motion': float(orbit_data.find('MEAN_MOTION').text),
        'eccentricity': float(orbit_data.find('ECCENTRICITY').text),
        'inclination': float(orbit_data.find('INCLINATION').text),
        'ra_of_asc_node': float(orbit_data.find('RA_OF_ASC_NODE').text),
        'arg_of_pericenter': float(orbit_data.find('ARG_OF_PERICENTER').text),
        'mean_anomaly': float(orbit_data.find('MEAN_ANOMALY').text),
        'ephemeris_type': int(root.find('.//data/tleParameters/EPHEMERIS_TYPE').text),
        'classification_type': root.find('.//data/tleParameters/CLASSIFICATION_TYPE').text,
        'norad_cat_id': int(root.find('.//data/tleParameters/NORAD_CAT_ID').text),
        'element_set_no': int(root.find('.//data/tleParameters/ELEMENT_SET_NO').text),
        'rev_at_epoch': int(root.find('.//data/tleParameters/REV_AT_EPOCH').text),
        'bstar': float(root.find('.//data/tleParameters/BSTAR').text),
        'mean_motion_dot': float(root.find('.//data/tleParameters/MEAN_MOTION_DOT').text),
        'mean_motion_ddot': float(root.find('.//data/tleParameters/MEAN_MOTION_DDOT').text),
    }

    return satellite_info, orbit_info

def insert_into_mysql(satellite_info, orbit_info):
    # Insert data into MySQL database
    connection = None
    try:
        connection = mysql.connector.connect(
            user='root',
            database='satellitedata'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Insert data into SatelliteOMM table
            insert_satellite_query = """
                INSERT INTO SatelliteOMM (
                    object_name, object_id, center_name, ref_frame, time_system, mean_element_theory
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_satellite_query, tuple(satellite_info.values()))

            # Get the last inserted satellite_id
            satellite_id = cursor.lastrowid

            # Insert data into OrbitOMM table
            insert_orbit_query = """
                INSERT INTO OrbitOMM (
                    satellite_id, epoch, mean_motion, eccentricity, inclination, ra_of_asc_node,
                    arg_of_pericenter, mean_anomaly, ephemeris_type, classification_type,
                    norad_cat_id, element_set_no, rev_at_epoch, bstar, mean_motion_dot, mean_motion_ddot
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Convert the timestamp to a string in the required format
            epoch_str = orbit_info['epoch'].strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_orbit_query, (
                satellite_id,
                epoch_str,  # Use the string representation of the timestamp
                orbit_info['mean_motion'],
                orbit_info['eccentricity'],
                orbit_info['inclination'],
                orbit_info['ra_of_asc_node'],
                orbit_info['arg_of_pericenter'],
                orbit_info['mean_anomaly'],
                orbit_info['ephemeris_type'],
                orbit_info['classification_type'],
                orbit_info['norad_cat_id'],
                orbit_info['element_set_no'],
                orbit_info['rev_at_epoch'],
                orbit_info['bstar'],
                orbit_info['mean_motion_dot'],
                orbit_info['mean_motion_ddot']
            ))

            connection.commit()
            print("Data inserted into SatelliteOMM and OrbitOMM tables successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

# Example usage:
def fetch_and_insert_omm_data(catnr):
    # Fetch and insert OMM data for the specified catalog number
    omm_data = fetch_celestrak_omm_data(catnr)
    satellite_info, orbit_info = parse_omm_data(omm_data)
    insert_into_mysql(satellite_info, orbit_info)

# Specify the catalog number for the satellite
catalog_number = '25544'
fetch_and_insert_omm_data(catalog_number)
