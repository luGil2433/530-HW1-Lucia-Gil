# 530-HW1-Lucia-Gil

# Geolocation Matching Application

This Python application allows users to input two arrays of geolocation points (latitude and longitude), then calculates and matches each point in the first array to the closest point in the second array using the Haversine formula to measure distances on Earth's surface.

## Features

- **User Input**: Users can input arrays of geolocation points interactively.
- **Haversine Formula**: The application calculates the great-circle distance between two geographic points.
- **Closest Point Matching**: Each point in the first array is matched to its closest counterpart in the second array, with the distance provided.

## How It Works

1. The user is prompted to input points for two arrays (`array1` and `array2`) in the format `lat, lon`.
   Follow the prompts:
   - Enter coordinates for the first array when prompted.
   - Enter coordinates for the second array when prompted.
   - For each array, you can add multiple points.
3. The Haversine formula computes the distance between each point in `array1` and all points in `array2`.
4. For each point in `array1`, the closest point in `array2` is identified along with the distance.
5. Results are displayed, showing the closest point and the computed distance in kilometers.

## Input Format

- Enter coordinates as `lat, lon` (e.g., `42.3601, -71.0589`).
- After each input, specify if you want to add more points (`yes` or `no`).

## Example Run

#### Input:

```
Enter coordinates for array1:
Enter lat, lon: 42.3601, -71.0589
Do you want to add another input to this array? (yes/no): yes
Enter lat, lon: 34.0522, -118.2437
Do you want to add another input to this array? (yes/no): no

Enter coordinates for array2:
Enter lat, lon: 37.7749, -122.4194
Do you want to add another input to this array? (yes/no): yes
Enter lat, lon: 47.6062, -122.3321
Do you want to add another input to this array? (yes/no): no
```

#### Output:

```
Point (42.3601, -71.0589) is closest to (37.7749, -122.4194) with a distance of 4306.36 km.
Point (34.0522, -118.2437) is closest to (37.7749, -122.4194) with a distance of 559.12 km.
```
