import math


def clean_input(input_str):
    """
    Cleans the input string by removing spaces and unexpected characters.
    """
    return input_str.replace(" ", "").replace("°", "").replace("'", "").replace('"', "")


def parse_degrees_to_decimal(degrees_str):
    """
    Converts a string in degrees format (ddmmss) to decimal degrees.
    """
    degrees_str = clean_input(degrees_str)
    try:
        degrees, minutes, seconds = int(degrees_str[:2]), int(degrees_str[2:4]), float(degrees_str[4:])
        decimal = degrees + minutes / 60 + seconds / 3600
        return decimal
    except (ValueError, IndexError):
        raise ValueError("Invalid degrees format. Use 'dd°mm'ss\"' (e.g., 42°30'10\").")


def get_coordinates_from_user(prompt):
    """
    Gets multiple coordinates from the user in either 'lat, lon' or 'degrees' format.
    """
    coordinates = []
    input_format = input("Choose input format ('1' for lat, lon or '2' for degrees): ").strip()

    while True:
        if input_format == "1":
            print("Example: 42.3601,-71.0589; 40.7128,-74.0060")
            user_input = input(prompt)
            try:
                # Split multiple inputs by semicolon and process each
                for coord in user_input.split(";"):
                    lat, lon = map(float, coord.split(","))
                    coordinates.append((lat, lon))
            except ValueError:
                print("Invalid input. Please enter coordinates in the format 'lat, lon' separated by semicolons.")
                continue
        elif input_format == "2":
            print("Example: 423010N,0710253W; 404231N,0740059W")
            try:
                user_input = input("Enter coordinates (e.g., 423010N,0710253W; 404231N,0740059W): ").strip()
                for coord in user_input.split(";"):
                    lat_str, lon_str = map(str.strip, coord.split(","))
                    lat = parse_degrees_to_decimal(lat_str[:-1]) * (-1 if lat_str[-1].upper() == 'S' else 1)
                    lon = parse_degrees_to_decimal(lon_str[:-1]) * (-1 if lon_str[-1].upper() == 'W' else 1)
                    coordinates.append((lat, lon))
            except ValueError as e:
                print(f"Invalid input: {e}")
                continue
        else:
            print("Invalid option. Please choose '1' or '2'.")
            input_format = input("Choose input format ('1' for lat, lon or '2' for degrees): ").strip()
            continue

        add_more = input("Do you want to add more coordinates? (yes/no): ").strip().lower()
        if add_more != 'yes':
            break

    return coordinates


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points on the Earth using the Haversine formula.
    """
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # Earth's radius in km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def match_closest_points(array1, array2):
    """
    Matches the closest points between two arrays of geolocations.
    """
    matches = []
    for lat1, lon1 in array1:
        closest_point = None
        min_distance = float('inf')
        for lat2, lon2 in array2:
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance < min_distance:
                min_distance = distance
                closest_point = (lat2, lon2)
        matches.append((lat1, lon1, closest_point, min_distance))
    return matches


# Main
# Get user input for arrays of geolocations
print("Enter coordinates for array1:")
array1 = get_coordinates_from_user("Enter lat, lon or degrees (multiple coordinates separated by ';'): ")

print("Enter coordinates for array2:")
array2 = get_coordinates_from_user("Enter lat, lon or degrees (multiple coordinates separated by ';'): ")

# Find matches
matches = match_closest_points(array1, array2)

# Display results
for origin, match in zip(array1, matches):
    lat1, lon1 = origin
    closest_lat, closest_lon = match[2]
    min_distance = match[3]
    print(f"Point {origin} is closest to {match[2]} with a distance of {min_distance:.2f} km.")
