# ACO Railway Path Optimization

This project implements an Ant Colony Optimization (ACO) algorithm to find an optimal path between railway stations, considering distance and slope constraints. The solution is visualized on an interactive map using Folium.

## Features

- Loads station data from a JSON file
- Implements the ACO algorithm for path optimization
- Considers both distance and slope in path selection
- Visualizes the best path on an interactive map
- Outputs detailed information about the best path found

## Dependencies

- folium
- json
- math
- random

## Usage

1. Ensure all required dependencies are installed.
2. Prepare your station data in a JSON file named `updated_new.json` with the following structure:
   ```json
   {
     "coordinates": [
       {"latitude": 51.5074, "longitude": -0.1278, "slope": 2.5},
       ...
     ]
   }
   ```
3. Adjust the ACO parameters in the script as needed:
   - `NUM_ANTS`
   - `ALPHA`
   - `BETA`
   - `RHO`
   - `MAX_ITERATIONS`
4. Run the script:
   ```
   python main.py
   ```
5. The script will generate an HTML file `best_path_map.html` showing the best path on an interactive map.

## How It Works

1. The script loads station data from the JSON file.
2. It initializes the ACO algorithm with the specified parameters.
3. For each iteration:
   - Ants construct paths between stations.
   - The best path in the current iteration is identified.
   - Pheromone trails are updated based on the quality of the paths.
4. The overall best path is tracked across all iterations.
5. Finally, the best path is visualized on an interactive map using Folium.

## Customization

You can customize the project by:
- Modifying the ACO parameters to fine-tune the algorithm's performance
- Adjusting the `max_slope` value to change the slope constraint
- Altering the map visualization style or adding additional features to the map

## Output

The script provides detailed output, including:
- The best path found in each iteration
- The overall best path and its total distance
- A list of stations in the best path
- An interactive HTML map showing the optimal route

## Note

This project is designed for educational and research purposes. The effectiveness of the generated paths should be validated by domain experts before any real-world application in railway planning.
