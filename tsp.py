import itertools
import requests

towns = ["Nairobi, Kenya", "Nakuru, Kenya", "Nyahururu, Kenya", "Nyeri, Kenya", "Meru, Kenya", "Nandi, Kenya"]


def get_coordinates(town):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': town,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(url, params=params).json()
    if response:
        return float(response[0]['lat']), float(response[0]['lon'])
    else:
        raise Exception(f"Could not get coordinates for {town}")

coordinates = [get_coordinates(town) for town in towns]

#OSRM API(to determine the distances between the towns)

def get_distance_matrix(coordinates):
    base_url = "http://router.project-osrm.org/table/v1/driving/"
    locs = ";".join([f"{lon},{lat}" for lat, lon in coordinates])
    url = f"{base_url}{locs}"
    params = {
        'annotations': 'distance'
    }
    
    response = requests.get(url, params=params).json()
    
    if 'distances' in response:
        return response['distances']
    else:
        raise Exception("Error fetching data from OSRM API")

distance_matrix = get_distance_matrix(coordinates) # A 2D array




def calculate_distance(path, distances):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distances[path[i]][path[i + 1]]
    return total_distance

def shortest_path(distances):
    num_towns = len(distances)
    shortest_distance = float('inf')
    shortest_path = None
    
    # Generate all permutations of towns
    all_paths = itertools.permutations(range(num_towns))
    
    # Iterate over all permutations and calculate distances
    for path in all_paths:
        current_distance = calculate_distance(path, distances)
        if current_distance < shortest_distance:
            shortest_distance = current_distance
            shortest_path = path
    
    return shortest_path, shortest_distance


    
shortest_path, shortest_distance = shortest_path(distance_matrix)
    
print(f"The shortest path is: {shortest_path}")
print(f"The shortest distance is: {shortest_distance}")