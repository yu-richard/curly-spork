import math
import csv 

# Load the airport dataset
def load_airport_data(file_path):
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

# Load the pricing data
def load_pricing_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

# Check if a point is inside a polygon
def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Get the region based on latitude and longitude
def get_region(lat, lon, polygons):
    point = (lat, lon)
    for region, polygon in polygons.items():
        if point_in_polygon(point, polygon):
            return region
    return None


# Get latitude and longitude based on airport code
def get_lat_lon(iata_code, airport_data):
    return airport_data.get(iata_code.upper(), (None, None))

# Calculate the distance between two coordinates using the haversine formula
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

# Define polygons for each region
polygons = {
    "North America": [
        (82.7870014, -59.3787003), (84.5580571, -81.2109375), (84.35484, -96.1241913), (82.2149613, -147.4523163), (72.357038, -167.8456879), (67.0429737, -168.0031872), (66.0599687, -168.0064058), (65.4692211, -168.7534761), (65.3182635, -169.6983004), (63.8474599, -171.8076754), (62.3218735, -171.4059448), (51.4715465, -179.4918823), (11.4645473, -166.8356323), (5.0589693, -95.1199722), (6.1842462, -78.5302734), (11.0059045, -76.3769531), (13.3254849, -71.015625), (11.4800246, -63.2373047), (11.1568453, -61.8530273), (10.7253813, -61.7651367), (9.9904908, -61.8530273), (9.7090571, -60.4248047), (12.7260843, -55.4150391), (47.4034616, -45.1318359), (74.6822527, -70.452919), (76.8399566, -74.671669), (78.0975167, -74.5837784), (80.4297022, -67.7283096), (81.2142764, -64.2126846), (81.9349958, -61.312294), (82.7870014, -59.3787003)
    ],
    "Atlantic": [
        (82.9186898, -56.4257813), (80.8728272, -66.4453125), (77.7302824, -73.828125), (58.0778763, -49.5703125), (19.2884613, -27.1142578), (-4.7646253, -15.6884766), (-38.5669585, 16.1279297), (-44.0130647, 41.4562225), (-27.4357746, 65.8898163), (-13.410994, 76.9921875), (-4.3902289, 82.3535156), (14.3069695, 88.9453125), (20.6327843, 91.4501953), (27.4887812, 96.9873047), (28.6134594, 97.2509766), (29.4587312, 95.3173828), (28.4203911, 92.9443359), (27.4887812, 88.9013672), (29.8025179, 82.0898438), (31.6561577, 79.2333984), (32.4383657, 78.6621094), (34.672041, 78.75), (36.917372, 75.1464844), (39.5175493, 73.8573074), (40.3933652, 74.9119949), (42.0459783, 80.0096512), (44.9771853, 80.6248856), (45.2872066, 82.4705887), (47.1119624, 83.4373856), (46.9921969, 85.4588699), (48.4116562, 85.6346512), (48.9917075, 87.3924637), (49.9624849, 86.6893387), (49.9624849, 85.0194168), (51.135201, 83.7010574), (51.0247691, 79.9217606), (54.0696637, 76.7576981), (53.3937708, 73.9451981), (55.5385395, 70.3416824), (54.0180574, 61.4647293), (56.4190289, 60.0807953), (59.6724216, 59.7292328), (62.9594376, 59.5534515), (65.1869205, 61.1354828), (66.3412251, 63.0690765), (67.6127514, 66.8483734), (69.2282846, 65.7057953), (71.4750154, 64.2631531), (75.1954423, 71.1000824), (77.3593367, 74.7914886), (81.7286224, 73.9125824), (82.6921109, 9.3974304), (82.9186898, -56.4257813)
    ],
    "Pacific": [
        (49.4587523, 87.6832581), (42.8975976, 80.3883362), (39.999742, 75.2906799), (34.8380407, 78.9820862), (28.7935375, 84.6949768), (28.089549, 87.2922134), (28.1964137, 90.0413704), (29.8043054, 95.993557), (28.2327173, 97.5573921), (19.3566599, 90.9633636), (10.7759758, 89.9684143), (-39.4139161, 94.4940948), (-60.0648405, 183.8671875), (-39.7156381, 188.9099121), (-25.1496356, 192.6280975), (-22.789476, 204.0339661), (15.2441086, 179.9529648), (31.2747363, 178.4601974), (47.754098, 181.40625), (62.8999099, 183.3089447), (66.2886792, 191.219101), (74.2506085, 161.1605072), (76.9129973, 76.4339447), (70.6014424, 64.8323822), (54.4504805, 60.2620697), (55.3599903, 69.2269135), (55.059102, 76.609726), (50.0425888, 87.156601), (49.4587523, 87.6832581)
    ],
    "South America": [
        (12.7260843, -55.4150391), (9.7090571, -60.4248047), (9.9904908, -61.8530273), (10.7253813, -61.7651367), (11.1568453, -61.8530273), (11.4800246, -63.2373047), (13.3254849, -71.015625), (11.0059045, -76.3769531), (6.1842462, -78.5302734), (3.2786581, -94.3965912), (-45.5813675, -89.6031189), (-51.3674937, -84.7265625), (-59.0596238, -75.7617188), (-58.3422988, -61.6992188), (-57.4549243, -35.2441406), (-52.4137285, -27.0703125), (-43.8795827, -32.6074219), (-16.1457623, -24.7896194), (0.5112008, -25.6685257), (12.6245927, -55.6392288)
    ],
}

# Load datasets
airport_data = load_airport_data("GlobalAirportDatabase.txt")
pricing_data = load_pricing_data("AeroplanChart.csv")

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
        print(f"{airport_codes[i]}-{airport_codes[i + 1]} distance: {segment_distance:.0f} miles")
    else:
        print(f"Could not fetch coordinates for segment {airport_codes[i]}-{airport_codes[i + 1]}")

# Get latitudes and longitudes for the first and last airport
first_lat, first_lon = get_lat_lon(airport_codes[0], airport_data)
last_lat, last_lon = get_lat_lon(airport_codes[-1], airport_data)

# Get the regions for the first and last airport
start_region = None
end_region = None

if first_lat is not None and first_lon is not None:
    start_region = get_region(first_lat, first_lon, polygons)
if last_lat is not None and last_lon is not None:
    end_region = get_region(last_lat, last_lon, polygons)

# Output the regions
print(f"Region of first airport ({airport_codes[0]}): {start_region}")
print(f"Region of last airport ({airport_codes[-1]}): {end_region}")

def fetch_prices(pricing_data, start_region, end_region, distance):
    zone = f"{start_region},{end_region}" if start_region != end_region else f"{start_region},{start_region}"
    print(f"Searching for prices in zone: {zone} for distance: {distance:.0f} miles")
    
    for row in pricing_data:
        row_zone = f"{row['StartZone']},{row['EndZone']}"
        
        miles_start = float(row['DistanceBandMilesStart']) if row['DistanceBandMilesStart'].isdigit() else 0
        miles_end = float(row['DistanceBandMilesEnd']) if row['DistanceBandMilesEnd'].replace("+", "").isdigit() else float("inf")

        if row_zone == zone:
            if miles_start <= distance <= miles_end:
                return {
                    "Air Canada Y": row['ACEconomy'],
                    "Air Canada PY": row['ACPremiumEconomy'],
                    "Air Canada J": row['ACBusiness'],
                    "Air Canada F": row['ACFirst'],
                    "Partner Y": row['PartnerEconomy'],
                    "Partner PY": row['PartnerPremiumEconomy'],
                    "Partner J": row['PartnerBusiness'],
                    "Partner F": row['PartnerFirst'],
                }
            else:
                None
        else:
            None
    print("No matching zone or distance found in pricing data.")
    return None


# Read the pricing chart
pricing_data = load_pricing_data("AeroplanChart.csv")

# Calculate total distance and fetch pricing information
pricing_info = fetch_prices(pricing_data, start_region, end_region, total_distance)

# Output the prices if found
if pricing_info:
    print(f"Pricing information for flight from {airport_codes[0]} to {airport_codes[-1]}:")
    for fare_class, price in pricing_info.items():
        print(f"  {fare_class}: {price} points")
else:
    print(f"No pricing data found for flight from {airport_codes[0]} to {airport_codes[-1]}.")
