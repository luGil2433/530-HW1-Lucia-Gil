"""
Module for calculating distances between geographic coordinates and finding closest matching points.

This module provides functionality to work with different coordinate formats (decimal and degrees),
calculate distances using the Haversine formula, and match closest points between two sets of coordinates.
"""

from math import radians, sin, cos, sqrt, atan2

EARTH_RADIUS_KM = 6371  # Earth's radius in kilometers


def clean_input(input_str):
    """Clean the input string by removing spaces and unexpected characters."""
    return input_str.replace(" ", "").replace("°", "").replace("'", "").replace('"', "")


def parse_degrees_to_decimal(degrees_str):
    """
    Convert a string in degrees format (ddmmss) to decimal degrees.
    
    Args:
        degrees_str: String in format 'dd°mm'ss"'
    
    Returns:
        float: Decimal degrees
    
    Raises:
        ValueError: If the input format is invalid
    """
    degrees_str = clean_input(degrees_str)
    try:
        degrees = int(degrees_str[:2])
        minutes = int(degrees_str[2:4])
        seconds = float(degrees_str[4:])
        decimal = degrees + minutes / 60 + seconds / 3600
        return decimal
    except (ValueError, IndexError) as exc:
        raise ValueError(
            "Invalid degrees format. Use 'dd°mm'ss\"' (e.g., 42°30'10\")"
        ) from exc


def validate_coordinates(latitude, longitude):
    """
    Validate that latitude and longitude are within valid Earth ranges.
    
    Args:
        latitude: Decimal degrees latitude
        longitude: Decimal degrees longitude
    
    Raises:
        ValueError: If coordinates are outside valid ranges
    """
    if not -90 <= latitude <= 90:
        raise ValueError(
            f"Invalid latitude {latitude}. Must be between -90 and 90 degrees."
        )
    if not -180 <= longitude <= 180:
        raise ValueError(
            f"Invalid longitude {longitude}. Must be between -180 and 180 degrees."
        )


def get_coordinates_from_user(prompt):
    """
    Get multiple coordinates from the user in either 'lat, lon' or 'degrees' format.
    
    Args:
        prompt: Input prompt string
    
    Returns:
        list: List of (latitude, longitude) tuples
    """
    coordinates = []
    input_format = input(
        "Choose input format ('1' for lat, lon or '2' for degrees): "
    ).strip()

    while True:
        if input_format == "1":
            print("Example: 42.3601,-71.0589; 40.7128,-74.0060")
            coord_input = input(prompt)
            try:
                for coord in coord_input.split(";"):
                    lat, lon = map(float, coord.split(","))
                    validate_coordinates(lat, lon)
                    coordinates.append((lat, lon))
            except ValueError as exc:
                print(f"Invalid input: {exc}")
                continue
        elif input_format == "2":
            print("Example: 423010N,0710253W; 404231N,0740059W")
            try:
                coord_input = input(
                    "Enter coordinates (e.g., 423010N,0710253W; 404231N,0740059W): "
                ).strip()
                for coord in coord_input.split(";"):
                    lat_str, lon_str = map(str.strip, coord.split(","))
                    lat = parse_degrees_to_decimal(lat_str[:-1])
                    lat *= -1 if lat_str[-1].upper() == 'S' else 1
                    lon = parse_degrees_to_decimal(lon_str[:-1])
                    lon *= -1 if lon_str[-1].upper() == 'W' else 1
                    validate_coordinates(lat, lon)
                    coordinates.append((lat, lon))
            except ValueError as exc:
                print(f"Invalid input: {exc}")
                continue
        else:
            print("Invalid option. Please choose '1' or '2'.")
            input_format = input(
                "Choose input format ('1' for lat, lon or '2' for degrees): "
            ).strip()
            continue

        add_more = input("Do you want to add more coordinates? (yes/no): ").strip().lower()
        if add_more != 'yes':
            break

    return coordinates


def calculate_haversine_distance(coord1_lat, coord1_lon, coord2_lat, coord2_lon):
    """
    Calculate the distance between two points using the Haversine formula.
    
    Args:
        coord1_lat: Latitude of first coordinate
        coord1_lon: Longitude of first coordinate
        coord2_lat: Latitude of second coordinate
        coord2_lon: Longitude of second coordinate
    
    Returns:
        float: Distance in kilometers
    """
    lat1, lon1, lat2, lon2 = map(
        radians, [coord1_lat, coord1_lon, coord2_lat, coord2_lon]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    temp = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    distance = 2 * atan2(sqrt(temp), sqrt(1 - temp))

    return EARTH_RADIUS_KM * distance


def find_closest_points(coords_set1, coords_set2):
    """
    Match the closest points between two sets of coordinates.
    
    Args:
        coords_set1: First set of coordinate pairs
        coords_set2: Second set of coordinate pairs
    
    Returns:
        list: List of tuples containing matching points and distances
    """
    closest_matches = []
    for coord1_lat, coord1_lon in coords_set1:
        closest_point = None
        shortest_distance = float('inf')
        for coord2_lat, coord2_lon in coords_set2:
            distance = calculate_haversine_distance(
                coord1_lat, coord1_lon, coord2_lat, coord2_lon
            )
            if distance < shortest_distance:
                shortest_distance = distance
                closest_point = (coord2_lat, coord2_lon)
        closest_matches.append(
            (coord1_lat, coord1_lon, closest_point, shortest_distance)
        )
    return closest_matches


def main():
    """Main function to run the coordinate matching program."""
    print("Enter coordinates for first set:")
    first_set = get_coordinates_from_user(
        "Enter lat, lon or degrees (multiple coordinates separated by ';'): "
    )

    print("Enter coordinates for second set:")
    second_set = get_coordinates_from_user(
        "Enter lat, lon or degrees (multiple coordinates separated by ';'): "
    )

    closest_matches = find_closest_points(first_set, second_set)

    for origin, match_data in zip(first_set, closest_matches):
        print(
            f"Point {origin} is closest to {match_data[2]} "
            f"with a distance of {match_data[3]:.2f} km."
        )


if __name__ == "__main__":
    main()
