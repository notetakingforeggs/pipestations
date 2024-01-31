#API from GCC is for live rentals :https://gcc.portal.azure-api.net/docs/services/mobility/operations/get-getrentals?
#API from nextbike has place data and more :https://mrin9.github.io/OpenAPI-Viewer/#/load/https%3A%2F%2Fraw.githubusercontent.com%2Fnextbike%2Fapi-doc%2Fmaster%2Fmaps%2Fnextbike-maps.openapi.yaml

import requests
import sqlite3
from datetime import datetime


#TODO also insert a column and data for time of request

# function to create table
def create_table():
  current_time = datetime.datetime.now().strftime("Y%m%d_%H%M%S")
  table_name = f"nextbike_map_data_{current_time}"
  conn = sqlite3.connect("nextbike_data.db")
  cursor = conn.cursor()
  cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                station_id INTEGER,
                name TEXT,
                latitude REAL,
                Longitude REAL,
                bikes_available INTEGER
                time_of_request TEXT
                )       
                ''')
  conn.commit()
  conn.close()
  print(f"table {table_name} created")
# insert station data function
  
def insert_station_data(city, station_data):
    conn = sqlite3.connect("nextbike_data.db")
    cursor = conn.cursor()
    request_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("connected to table in insert function")
    for place in station_data:
         cursor.execute('''
                         INSERT INTO nextbike_map_data (city, station_id, name, latitude, longitude, bikes_available)
                         VALUES (?, ?, ?, ?, ?, ?)
                         ''', (
                              city,
                              place.get('number'),
                              place.get('name'),
                              place.get('lat'),
                              place.get('lng'),
                              place.get('bikes_available_to_rent')
                              request_datetime
                         ))
    conn.commit()
    print("insert function completed")
    conn.close()

# make API request
base_url = "https://maps.nextbike.net/"
endpoint_path = "maps/nextbike-live.json"
params = {
    "city": "237",
    "scope": "official",
    "format": "json",
}


response = requests.get(base_url + endpoint_path, params = params)

if response.status_code == 200:
      data = response.json()
      countries_data = data.get("countries", [])
      if countries_data:
          cities_data = countries_data[0].get("cities", [])
          if cities_data:
              # Assuming "places" is the correct key for stations
              station_data = cities_data[0].get("places", [])
              print(station_data)
              
          else:
              print("No cities data")
      else:
          print("No countries data")
      
      print(station_data, "this was station")
      print("initiate create table")
      create_table() 
      print("create table complete initiate insert function")
      insert_station_data(params["city"], station_data)
      print("insert function complete")
else:
     print("some error")