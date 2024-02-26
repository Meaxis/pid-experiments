from google.transit import gtfs_realtime_pb2
import requests

api_key = open("api_key.txt", "r").read()
url = "https://api.golemio.cz/v2/vehiclepositions/gtfsrt/trip_updates.pb"

response = requests.get(url, headers={"X-Access-Token": api_key})

latest_delay = 0
latest_delay_trip = None

# Parse the GTFS-RT feed
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

# Go over with the GTFS data
for entity in feed.entity:
    # Get trip_update field
    if entity.HasField('trip_update'):
        trip_update = entity.trip_update

        # Get delay from stop_time_update
        for stop_time_update in trip_update.stop_time_update:
            if stop_time_update.HasField('arrival'):
                delay = stop_time_update.arrival.delay
                if delay > latest_delay:
                    latest_delay = delay
                    latest_delay_trip = entity
                  

print(f"Most delayed trip: {latest_delay/60} min! Info:")
print(f"Route {latest_delay_trip.trip_update.trip.route_id} with vehicle {latest_delay_trip.trip_update.vehicle.id} from {latest_delay_trip.trip_update.stop_time_update[0].stop_id}")
