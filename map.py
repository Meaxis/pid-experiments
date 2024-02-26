# For the lost soul reading this: This implementation is limited in scope, you can only get the data the map is willing to give you
# Ideally implement GTFS in delay.py

import requests

pidata = requests.post("https://mapa.pid.cz/getData.php", json={
  "action":"getData", # Leave as getData
  "dimensions": [1027,694], # Screen dimensions
  "bounds": [14.006151689879978, 50.086263274683176, 14.711336626403419, 50.39104754934587], # Set of GPS coordinates to look at
  "filter_lin":"3869", # Connection number 
  "openedVehicleWindow": False
})

pidata = pidata.json()
pidata = pidata["trips"]
line_filter = None

most_delayed_connection = pidata["0"]

for connection_index in pidata:
    connection = pidata[connection_index]
    if not line_filter or connection["route"] not in line_filter:
        continue

    if connection["delay"] > most_delayed_connection["delay"]:
        most_delayed_connection = connection

print(f"The winner is connection {most_delayed_connection['route']} e.v. {most_delayed_connection['vehicle']} with delay {most_delayed_connection['delay']/60} minutes.")
