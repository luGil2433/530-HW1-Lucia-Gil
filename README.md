# 530-HW1-Lucia-Gil

# Geolocation Matching Application

This Python application allows users to input two arrays of geolocation points (latitude and longitude or degrees), then calculates and matches each point in the first array to the closest point in the second array using the Haversine formula to measure distances on Earth's surface.

## Features

- **User Input Options**:
  - Users can choose between two input formats: `lat, lon` or degrees (`ddmmss` format).
  - Multiple coordinates can be entered at once, separated by semicolons.
- **Haversine Formula**: The application calculates the great-circle distance between two geographic points.
- **Closest Point Matching**: Each point in the first array is matched to its closest counterpart in the second array, with the distance provided.
- **Validation**:
  - Ensures latitude and longitude are within valid Earth ranges:
    - Latitude: −₉₀° to +90°
    - Longitude: −₁₈₀° to +180°
  - Handles unexpected characters, spaces, and incorrect formats with clear error messages.

## How It Works

1. The user is prompted to input points for two arrays (`array1` and `array2`) using their preferred input format:
   - **Option 1**: Latitude and longitude as `lat, lon` (e.g., `42.3601, -71.0589`).
   - **Option 2**: Degrees, minutes, and seconds in `ddmmss` format (e.g., `423010N, 0710253W`).
2. The application validates the input to ensure it falls within valid Earth ranges.
3. The Haversine formula computes the distance between each point in `array1` and all points in `array2`.
4. For each point in `array1`, the closest point in `array2` is identified along with the distance.
5. Results are displayed, showing the closest point and the computed distance in kilometers.

## Input Formats

### Option 1: Latitude and Longitude (`lat, lon`)
- Example: `42.3601, -71.0589; 34.0522, -118.2437`
- Separate multiple coordinates with semicolons.

### Option 2: Degrees (`ddmmss`)
- Example: `423010N, 0710253W; 340314N, 1181452W`
- North/South and East/West directions are indicated with `N`, `S`, `E`, or `W`.
- Separate multiple coordinates with semicolons.

## Example Run

### Input:

```
Enter coordinates for array1:
Choose input format ('1' for lat, lon or '2' for degrees): 1
Example: 42.3601,-71.0589; 40.7128,-74.0060
Enter lat, lon or degrees (multiple coordinates separated by ';'): 42.3601, -71.0589; 34.0522, -118.2437
Do you want to add more coordinates? (yes/no): no

Enter coordinates for array2:
Choose input format ('1' for lat, lon or '2' for degrees): 2
Example: 423010N,0710253W; 404231N,0740059W
Enter lat, lon or degrees (multiple coordinates separated by ';'): 404231N, 0740059W; 370458N, 1222520W
Do you want to add more coordinates? (yes/no): no
```

### Output:

```
Point (42.3601, -71.0589) is closest to (40.4231, -74.0059) with a distance of 212.94 km.
Point (34.0522, -118.2437) is closest to (37.0458, -122.2520) with a distance of 559.12 km.
```

## Fun Facts About Me

1. I was born in Spain.
2. I used to sail competitively.
3. I began coding in 9th grade.
4. I do the NYT Sudoku every day.
5. I'm very excited for Couture Fashion Week.

