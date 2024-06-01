import random
import numpy as np

class AntColonyOptimization:
    def __init__(self, num_ants, num_stations, distance_matrix, pheromone_evaporation_rate, alpha, beta, max_iterations):
        self.num_ants = num_ants
        self.num_stations = num_stations
        self.distance_matrix = distance_matrix
        self.pheromone_evaporation_rate = pheromone_evaporation_rate
        self.alpha = alpha  # Pheromone importance factor
        self.beta = beta  # Heuristic importance factor
        self.max_iterations = max_iterations
        self.pheromone_matrix = np.ones((num_stations, num_stations))  # Initialize pheromone matrix

    def run(self):
        best_path = None
        best_distance = float('inf')

        for iteration in range(self.max_iterations):
            paths = self.construct_paths()
            distances = [self.calculate_path_distance(path) for path in paths]

            if min(distances) < best_distance:
                best_distance = min(distances)
                best_path = paths[distances.index(min(distances))]

            self.update_pheromone_matrix(paths, distances)

        return best_path, best_distance

    def construct_paths(self):
        paths = []
        for ant in range(self.num_ants):
            path = self.construct_path()
            paths.append(path)
        return paths

    def construct_path(self):
        path = [random.randint(0, self.num_stations - 1)]
        unvisited_stations = list(range(self.num_stations))
        unvisited_stations.remove(path[0])

        while unvisited_stations:
            current_station = path[-1]
            next_station = self.choose_next_station(current_station, unvisited_stations)
            path.append(next_station)
            unvisited_stations.remove(next_station)

        return path

    def choose_next_station(self, current_station, unvisited_stations):
        pheromone_values = [self.pheromone_matrix[current_station][station] ** self.alpha *
                             (1.0 / self.distance_matrix[current_station][station]) ** self.beta
                             for station in unvisited_stations]
        total_pheromone = sum(pheromone_values)
        probabilities = [value / total_pheromone for value in pheromone_values]
        next_station = np.random.choice(unvisited_stations, p=probabilities)
        return next_station

    def calculate_path_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += self.distance_matrix[path[i]][path[i + 1]]
        return distance

    def update_pheromone_matrix(self, paths, distances):
        self.pheromone_matrix *= (1 - self.pheromone_evaporation_rate)
        for path, distance in zip(paths, distances):
            pheromone_deposit = 1.0 / distance
            for i in range(len(path) - 1):
                self.pheromone_matrix[path[i]][path[i + 1]] += pheromone_deposit

# Example usage
num_ants = 10
num_stations = 5
distance_matrix = [[0, 10, 15, 20, 25],
                   [10, 0, 35, 25, 30],
                   [15, 35, 0, 30, 20],
                   [20, 25, 30, 0, 40],
                   [25, 30, 20, 40, 0]]
pheromone_evaporation_rate = 0.5
alpha = 1.0
beta = 2.0
max_iterations = 100

aco = AntColonyOptimization(num_ants, num_stations, distance_matrix, pheromone_evaporation_rate, alpha, beta, max_iterations)
best_path, best_distance = aco.run()

print("Best Path:", best_path)
print("Best Distance:", best_distance)