from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import sqlite3

geolocator = Nominatim(user_agent="QuickCare")

def get_user_coordinates(location_string):
    """Convert location string to coordinates."""
    try:
        location = geolocator.geocode(location_string)
        if location:
            return location.latitude, location.longitude
        raise ValueError("Location not found")
    except Exception as e:
        print(f"Geocoding failed (using default): {e}")
        return 40.7128, -74.0060  # Default to NYC as fallback

def calculate_distances(user_lat, user_lon, facilities):
    """Calculate distances and add wait times to facilities."""
    user_coords = (user_lat, user_lon)
    for facility in facilities:
        facility_coords = (facility['lat'], facility['lon'])
        distance = geodesic(user_coords, facility_coords).miles
        facility['distance'] = round(distance, 1)
        facility['wait_time'] = get_wait_time(facility['place_id'])
    return facilities

def get_wait_time(place_id):
    """Retrieve wait time from database."""
    try:
        conn = sqlite3.connect('quickcare.db')
        c = conn.cursor()
        c.execute("SELECT wait_time FROM wait_times WHERE place_id = ?", (place_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else 30  # Default to 30 min
    except Exception as e:
        print(f"Database error: {e}")
        return 30