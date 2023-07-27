import math

# Load the dataset
def load_dataset(file_path):
    try:
        with open(file_path, 'r') as file:
            airport_data = {}
            for line in file:
                fields = line.strip().split(":")
                iata_code = fields[1]
                try:
                    latitude = float(fields[-2])
                    longitude = float(fields[-1])
                except ValueError:
                    continue
                if iata_code != "N/A":
                    airport_data[iata_code.upper()] = (latitude, longitude)
            return airport_data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}

# Fetch latitude and longitude from the dataset
def get_lat_lon(iata_code, airport_data):
    return airport_data.get(iata_code.upper(), (None, None))

# Define the haversine formula to calculate great circle distance
def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in miles
    R = 3958.8

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Compute differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate distance
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

# Load the dataset
airport_data = load_dataset("GlobalAirportDatabase.txt")

# Ensure that the dataset was loaded
if not airport_data:
    print("Unable to proceed without the dataset.")
    exit()

# Get user input and convert to uppercase
user_input = input("Enter airport IATA codes separated by hyphens (e.g. YYZ-YHZ-LAX): ").upper()

# Split the input into individual airport codes
airport_codes = user_input.split("-")

# Initialize total distance
total_distance = 0.0

# Calculate distances for segments
for i in range(len(airport_codes) - 1):
    # Get latitudes and longitudes of the two airports
    lat1, lon1 = get_lat_lon(airport_codes[i], airport_data)
    lat2, lon2 = get_lat_lon(airport_codes[i + 1], airport_data)
    
    # Calculate and accumulate the distance
    if lat1 is not None and lat2 is not None:
        segment_distance = haversine(lat1, lon1, lat2, lon2)
        total_distance += segment_distance
        print(f"{airport_codes[i]}-{airport_codes[i + 1]} distance: {segment_distance:.2f} miles")
    else:
        print(f"Could not fetch coordinates for segment {airport_codes[i]}-{airport_codes[i + 1]}")

# Print total distance
print(f"Total distance: {total_distance:.2f} miles")
