# Flag to use mock data
USE_MOCK_DATA = True

def fetch_facility_data(user_lat, user_lon):
    """Return mock healthcare facilities in Charlotte and Concord, NC."""
    if USE_MOCK_DATA:
        facilities = [
            # Charlotte, NC
            {'place_id': '1', 'name': 'AFC Urgent Care Ballantyne', 'lat': 35.068676, 'lon': -80.832378, 'type': 'Urgent Care'},
            {'place_id': '2', 'name': 'Atrium Health Carolinas Medical Center', 'lat': 35.222728, 'lon': -80.841721, 'type': 'Hospital'},
            # Concord, NC
            {'place_id': '3', 'name': 'CVS MinuteClinic', 'lat': 35.401282, 'lon': -80.615776, 'type': 'Clinic'}
        ]
        return facilities
    else:
        # Placeholder for real API (not implemented here)
        print("Real API not implemented in this prototype.")
        return []