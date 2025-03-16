import sqlite3
from geolocation import get_user_coordinates, calculate_distances
from data_fetcher import fetch_facility_data


# Initialize databases
def init_db():
    """Initialize SQLite databases for wait times and users."""
    # Wait times database
    conn = sqlite3.connect('quickcare.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wait_times
                 (place_id TEXT PRIMARY KEY, wait_time INTEGER, last_updated TIMESTAMP)''')
    conn.commit()
    conn.close()

    # Users database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, gender TEXT, age INTEGER)''')
    conn.commit()
    conn.close()


def login():
    """Handle user login or registration."""
    print("Welcome to QuickCare Prototype!")
    while True:
        email = input("Enter your email to log in/register (or 'quit' to exit): ").strip().lower()
        if email == 'quit':
            return None

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT gender, age FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        if user:  # Existing user
            print(f"Logged in as {email} (Gender: {user[0]}, Age: {user[1]})")
            conn.close()
            return email
        else:  # New user
            print("New user detected. Please provide some details.")
            gender = input("Gender (e.g., M/F/Other): ").strip()
            age = input("Age (e.g., 25): ").strip()
            if age.isdigit() and 0 < int(age) < 150:
                c.execute("INSERT INTO users (email, gender, age) VALUES (?, ?, ?)",
                          (email, gender, int(age)))
                conn.commit()
                print(f"Registered and logged in as {email}")
                conn.close()
                return email
            else:
                print("Invalid age. Try again.")
        conn.close()


def main():
    """Main prototype loop for QuickCare."""
    init_db()
    user_email = login()
    if not user_email:
        print("Exiting QuickCare.")
        return

    print(f"\nHello, {user_email}! Enter a location (e.g., 'Charlotte, NC') or 'quit' to exit.")

    while True:
        user_input = input("Location: ").strip()
        if user_input.lower() == 'quit':
            print("Exiting QuickCare.")
            break

        # Get user coordinates
        try:
            lat, lon = get_user_coordinates(user_input)
            print(f"Resolved location to coordinates: ({lat}, {lon})")
        except Exception as e:
            print(f"Error with location: {e}")
            continue

        # Fetch facilities
        facilities = fetch_facility_data(lat, lon)
        if not facilities:
            print("No facilities found.")
            continue

        # Calculate distances and get wait times
        facilities = calculate_distances(lat, lon, facilities)
        facilities = sorted(facilities, key=lambda x: x['distance'])[:5]  # Top 5 closest

        # Display results
        print("\nNearby Healthcare Facilities:")
        for i, facility in enumerate(facilities, 1):
            print(f"{i}. {facility['name']} ({facility['type']})")
            print(f"   Distance: {facility['distance']} miles")
            print(f"   Wait Time: {facility['wait_time']} minutes")

        # Allow wait time reporting
        report = input("\nReport a wait time? (Enter number 1-5 or 'no'): ").strip()
        if report.isdigit() and 1 <= int(report) <= len(facilities):
            facility = facilities[int(report) - 1]
            wait_time = input(f"Enter wait time for {facility['name']} (minutes): ").strip()
            if wait_time.isdigit():
                save_wait_time(facility['place_id'], int(wait_time))
                print("Wait time saved!")
            else:
                print("Invalid wait time.")
        elif report.lower() != 'no':
            print("Invalid input, skipping.")


def save_wait_time(place_id, wait_time):
    """Save user-reported wait time to database."""
    try:
        conn = sqlite3.connect('quickcare.db')
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO wait_times (place_id, wait_time, last_updated) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (place_id, wait_time))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving wait time: {e}")


if __name__ == '__main__':
    main()