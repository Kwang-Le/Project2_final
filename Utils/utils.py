import math
from Model.model import Cluster, Location

def distance_callback(locationA, locationB):
    """
    function defining how distance is calculated between 2 locations
    
    Args:
    
    `locationA`: the first location
        
    `locationB`: the second location
    
    Returns:

    distance between 2 locations 
    """
    xDis = (locationA.x - locationB.x)*(locationA.x - locationB.x)
    yDis = (locationA.y - locationB.y)*(locationA.y - locationB.y)
    distance = math.ceil(math.sqrt(xDis + yDis) * 100000)

    return distance


def create_distance(cluster_list, distance_callback):
    """
    Create distance matrix between each 2 clusters in a cluster list
    
    Args:
    
    `cluster_list`: The list of clusters
        
    `distance_callback`: Function to define the distance between 2 cities.
    
    Returns:

    An 2-D array 
    """
    n = len(cluster_list)
    distance = [[0] * n for i in range(n)]

    for id in range(n):
        for id_ in range(n):
            distance[id][id_], _ = cluster_list[id].distance(cluster_list[id_], distance_callback)

    return distance

def calculater_average_distance(cluster: Cluster, distance_callback):
    distance = create_distance_city(cluster, distance_callback)
    sum = 0
    counter = 0
    for row in distance:
        for value in row:
            sum += value
            counter += 1
    average = sum / counter
    return average


def create_distance_city(cluster, distance_callback):
    """
    Create distance matrix between each 2 clusters in a cluster list
    
    Args:
    
    `cluster_list`: The list of clusters
        
    `distance_callback`: Function to define the distance between 2 cities.
    
    Returns:

    An 2-D array 
    """
    n = cluster.get_quantity()
    distance = [[0] * n for i in range(n)]

    for id in range(n):
        for id_ in range(n):
            distance[id][id_] = distance_callback(cluster.location_list[id], cluster.location_list[id_])

    return distance