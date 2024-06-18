import folium
import json
import math
import random

# Load the coordinates from the JSON file
with open('new.json', 'r') as f:
    data = json.load(f)
    coordinates = data['coordinates']

# Create a dictionary of stations from the coordinates
stations = {}
for i, coord in enumerate(coordinates):
    station_name = f'Station_{i+1}'
    lat, lon, slope = coord['latitude'], coord['longitude'], coord['slope']
    stations[station_name] = (lat, lon, slope)

# Calculate the Haversine distance between two stations
def haversine_distance(station1, station2):
    lat1, lon1, _ = stations[station1]
    lat2, lon2, _ = stations[station2]

    r = 6371  # Earth's radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c

# Check if the slope between two stations is acceptable
def is_slope_acceptable(station1, station2):
    _, _, slope1 = stations[station1]
    _, _, slope2 = stations[station2]
    max_slope = 75
    return max(slope1, slope2) <= max_slope

# Initialize the pheromone trails
pheromones = {}
for station1 in stations:
    for station2 in stations:
        pheromones[(station1, station2)] = 1.0

# Define the ACO parameters
NUM_ANTS = 10
ALPHA = 1.0
BETA = 2.0
RHO = 0.5
MAX_ITERATIONS = 10

# Perform the ACO algorithm
best_path = None
best_distance = float('inf')

for iteration in range(MAX_ITERATIONS):
    print(f"Generation {iteration + 1}:")

    # Initialize the ants
    ants = []
    for _ in range(NUM_ANTS):
        start_station = random.choice(list(stations.keys()))
        path = [start_station]
        ants.append(path)

    # Let the ants find their paths
    for ant in ants:
        for _ in range(len(stations) - 1):
            current_station = ant[-1]
            unvisited_stations = [station for station in stations if station not in ant]
            probabilities = []
            total_pheromone = 0.0
            for station in unvisited_stations:
                if is_slope_acceptable(current_station, station):
                    pheromone = pheromones[(current_station, station)]
                    distance = haversine_distance(current_station, station)
                    distance_weight = 1.0 / (distance + 1e-10)  # Add a small constant to avoid division by zero
                    probability = pheromone ** ALPHA * distance_weight ** BETA
                    total_pheromone += probability
                    probabilities.append((station, probability))

            # Select the next station based on the probabilities
            next_station = None
            if total_pheromone > 0:
                cuml_prob = 0.0
                rand_prob = random.uniform(0, total_pheromone)
                for station, prob in probabilities:
                    cuml_prob += prob
                    if cuml_prob >= rand_prob:
                        next_station = station
                        break

            # If no station is selected, choose one randomly
            if not next_station:
                next_station = random.choice(unvisited_stations)

            ant.append(next_station)

    # Find the best path in the current iteration
    current_best_path = None
    current_best_distance = float('inf')
    for ant in ants:
        path_distance = sum(haversine_distance(ant[i], ant[i + 1]) for i in range(len(ant) - 1))
        if path_distance < current_best_distance:
            current_best_path = ant[:]
            current_best_distance = path_distance

    # Print the best path in the current iteration
    print(f"Best path in iteration {iteration + 1}: {' -> '.join(current_best_path)} (Distance: {current_best_distance:.2f} km)")

    # Update the overall best path if a better path is found
    if current_best_distance < best_distance:
        best_path = current_best_path[:]
        best_distance = current_best_distance
        print(f"New overall best path found: {' -> '.join(best_path)} (Distance: {best_distance:.2f} km)")


    # Update the pheromone trails
    for ant in ants:
        path_distance = sum(haversine_distance(ant[i], ant[i + 1]) for i in range(len(ant) - 1))
        if path_distance < best_distance:
            best_path = ant[:]
            best_distance = path_distance
            print(f"New best path found: {' -> '.join(best_path)} (Distance: {best_distance:.2f} km)")

        for i in range(len(ant) - 1):
            station1 = ant[i]
            station2 = ant[i + 1]
            pheromones[(station1, station2)] = (1 - RHO) * pheromones[(station1, station2)] + RHO / path_distance

# Visualize the solution on OpenStreetMap
map = folium.Map()

for station, coords in stations.items():
    lat, lon, _ = coords
    folium.Marker(
        location=[lat, lon],
        icon=folium.Icon(color='red'),
        tooltip=station
    ).add_to(map)

for i in range(len(best_path) - 1):
    station1 = best_path[i]
    station2 = best_path[i + 1]
    lat1, lon1, _ = stations[station1]
    lat2, lon2, _ = stations[station2]
    folium.PolyLine(
        locations=[(lat1, lon1), (lat2, lon2)],
        color='green',
        weight=2
    ).add_to(map)

for station, coords in stations.items():
    lat, lon, _ = coords
    folium.Marker(
        location=[lat, lon],
        icon=folium.Icon(color='green'),
        tooltip=station
    ).add_to(map)

map.save('railway_solution.html')

# Print the best path and its distance
print(f"Best path: {' -> '.join(best_path)}")
print(f"Best distance: {best_distance:.2f} km")