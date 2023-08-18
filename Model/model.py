import numpy as np

class Location:
    """
        A class for a location
    """
    def __init__(self, x, y, id):
        """
        Get the number of location in this cluster
        
        Args:

        `x`: The value of X-axis

        `y`: The value of Y-axis

        `id`: Index of the location

        Returns:

        """
        self.x = x
        self.y = y
        self.id = id
        self.id_pickup_delivery = None
        self.pickup_delivery_value = None
    
    def __repr__(self):
        return "(" + str(self.id) + ")"

class Cluster:
    """
        A class for a cluster
    """
    def __init__(self, location_list = None):
        """
        Get the number of location in this cluster
        
        Args:

        `location_list`: The list containing cities in a cluster

        Returns:

        """
        self.location_list = []
        if (location_list != None):
            self.location_list = location_list
    
    def get_quantity(self):
        """
        Get the number of location in this cluster
        
        Args:
        
        Returns:

        The number of location
        """
        return len(self.location_list)

    def append(self, location):
        """
        Append a new location into this cluster
        
        Args:
        
        Returns:
        """
        self.location_list.append(location)

    def distance(self, cluster, distance_callback):
        """
        Calculate the distance between 2 clusters

        Args:

        `cluster`: Cluster you want to cal distance

        `distance_callback`: The function defining the distance between 2 location
        
        Returns:

        The distance between 2 cluster

        """
        min_distance = np.inf
        location_list = cluster.location_list
        connect_location = None
        
        for beg in self.location_list:
            for des in location_list:
                distance = distance_callback(beg, des)
                if min_distance > distance:
                    min_distance = distance
                    connect_location = beg.id
        
        return min_distance, connect_location
    
    def copy(self):
        new_cluster = Cluster()
        for location in self.location_list:
            new_cluster.append(location)
        
        return new_cluster

class Vehicle:
    """
        A class for a Vehicle
    """
    def __init__(self, id, max_capacity, depot_loc_location):
        """
        Get the number of location in this cluster
        
        Args:

        `id` : the id of the vehicle

        `max_capacity` : the max capacity that a vehicle can carry

        `depot_loc_location`: The depot location for this vehicle

        Returns:

        """
        self.id = id
        self.max_capacity = max_capacity
        self.route_list = []
        self.depot_loc_location  = depot_loc_location
        self.total_no_load_distance = 0
        self.total_has_load_distance = 0
        self.total_average_load_factor_of_routes = 0
        self.number_of_routes = 0
        self.total_distance_of_car = 0
        self.number_of_dist_with_no_load = 0
        self.number_of_dist_with_load = 0
        self.number_of_dist = 0
        self.completed_order = []

    def add_route_average_load_factor(self, average_load_factor):
        self.total_average_load_factor_of_routes += average_load_factor
    
    def get_average_of_all_routes_average_load_factor(self):
        if self.number_of_routes != 0 :
            return self.total_average_load_factor_of_routes / self.number_of_routes
        else:
            return 0
    def sortRoute():
        pass

class Order:
    """
        A class for a Order
    """
    def __init__(self, id, pickup_location, delivery_location, weight):
       self.order_id = id
       self.pickup_location = pickup_location
       self.delivery_location = delivery_location
       self.weight = weight
