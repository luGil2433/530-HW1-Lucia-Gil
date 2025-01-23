import math


    #User Input
def get_coordinates_from_user(prompt):
    coordinates = []
    while True:
        user_input = input(prompt)
        try:
            lat, lon = map(float, user_input.split(','))
            coordinates.append((lat, lon))
        except ValueError:
            print("Invalid input. Please enter coordinates in the format 'lat, lon'.")
            continue
        add_more = input("Do you want to add another input to this array? (yes/no): ").strip().lower()
        if add_more != 'yes':
            break
    return coordinates


    # Haversine formula
    # Calculate the distance between two points on the Earth
def haversine(lat1, lon1, lat2, lon2):
   
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

    #Find the closest point
def match_closest_points(array1, array2):
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
print("Enter coordinates for array1 :")
array1 = get_coordinates_from_user("Enter lat, lon: ")

print("Enter coordinates for array2 :")
array2 = get_coordinates_from_user("Enter lat, lon: ")

# Find matches
matches = match_closest_points(array1, array2)

# Display results
for origin, match in zip(array1, matches):
    lat1, lon1 = origin
    closest_lat, closest_lon = match[2]
    min_distance = match[3]
    print(f"Point {origin} is closest to {match[2]} with a distance of {min_distance:.2f} km.")
