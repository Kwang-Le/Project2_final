import random
from Clustering.Clustering import clusteringDBSCAN
from Model.model import Location, Cluster, Vehicle
from Routing.routing import find_journey_car_travel_distance_constraint, find_journey_without_capacity
from Utils.utils import calculater_average_distance, create_distance_city, distance_callback
 
DISTANCE_CALLBACK = distance_callback

def find_journey_DBSCAN_car_travel_distance_constraint(pick_up_cluster, delivery_cluster, pickups_and_deliveries_cluster, depot_loc_list, vehicle_list):
    """
    Find route for VRP with DBSCAN with the constraint that a vehicle can only be allowed to travel less than 400km before it returns to depot
    
    Args:

    `pick_up_cluster` : A cluster containing only pick up locations

    `delivery_cluster` : A cluster containing only delivery locations

    `pickups_and_deliveries_cluster`: A cluster containing both pick up and delivery locations

    `depot_loc_list` : an array containing all the depot locations
    
    `vehicle_list` : A array of all vehicles 

    Returns:

    `paths_for_cars` : a combined path of each of the vehicle
    `total_distance` : total distance of all vehicles
    `total_no_load_distance_all` : total travel distance without load
    `total_has_load_distance_all` : total travel distance with load
    
    """
    average_distance = calculater_average_distance(pick_up_cluster, DISTANCE_CALLBACK)
    print("average_distance", average_distance)
    cluster_list = clusteringDBSCAN(pick_up_cluster,delivery_cluster, average_distance, depot_loc_list, 0.05)
    total_distance = 0
    paths_for_cars = []
    total_no_load_distance_all = 0
    total_has_load_distance_all = 0
    total_average_load_factor = 0


    for car_id, cluster in enumerate(cluster_list):
        pickup_and_deliveries_nodes = Cluster()

        

        # initialize the depot_loc index in the cluster, the default value is None
        depot_loc_index = None
        # find the index of the depot_loc
        for index, location in enumerate(cluster.location_list):
            for depot_loc in depot_loc_list:
                if depot_loc.id == location.id:
                    if depot_loc_index == None:
                        depot_loc_index = index
                    else:
                        cluster.location_list[index] = None # if there are more than one parking location in a cluster, choose the first one and remove the rest
                        break
        cluster.location_list = [ele for ele in cluster.location_list if ele != None]
        

        # if there is no depot_loc in cluster then automatically add the next depot_loc in the list, and then move that depot_loc to the end of the list
        if depot_loc_index == None:
            cluster.location_list.insert(0, depot_loc_list[0]) # add depot_loc location to each cluster
            depot_loc_list.append(depot_loc_list[0])
            #after adding the same depot_loc to the back then remove it at the front of the list
            depot_loc_list.pop(0)
            depot_loc_index = 0

        # if a cluster size is only one then skip
        if len(cluster.location_list) < 2:
            continue

        print(cluster.location_list)
        distance = create_distance_city(cluster, DISTANCE_CALLBACK)

        # add max capacities of vehicles in fleet
        vehicle_max_capacities = []
        for vehicle in vehicle_list:
            if vehicle.max_capacity not in vehicle_max_capacities:
                vehicle_max_capacities.append(vehicle.max_capacity)
        vehicle_max_capacities.sort()

        #find optimal route
        routes_list, total_distance_routes_list, max_capacity_routes_list, no_load_distance_routes_list, with_load_distance_routes_list, average_capacity_utilization_routes_list, number_of_dist_with_no_load_routes_list, number_of_dist_with_load_routes_list = find_journey_car_travel_distance_constraint(distance, depot_loc_index, depot_loc_index, cluster, vehicle_max_capacities)             
        
        for index, route in enumerate(routes_list):
            # construct path
            final_path = []
            for id in range(len(route)):
                final_path.append(cluster.location_list[route[id]])
            print(final_path)
            # construct order sequence list
            order_id_sequence = []
            for i in range(1, len(final_path) - 1):
                if final_path[i].pickup_delivery_value > 0: #is pickup point
                    order_id_sequence.append(final_path[i].id_pickup_delivery)
            

            # assign vehicle to route
            vehicle_id = None
            chosen_vehicle = None
            for vehicle in vehicle_list:
                # if vehicle max capacity is the same as the max capacity of route and the vehicle also has the same depot_loc in route then assign that vehicle to route
                if vehicle.max_capacity == max_capacity_routes_list[index] and vehicle.depot_loc_location == final_path[0].id:
                    vehicle_id = vehicle.id
                    vehicle.number_of_routes += 1
                    vehicle.total_distance_of_car += total_distance_routes_list[index]
                    vehicle.total_no_load_distance += no_load_distance_routes_list[index]
                    vehicle.total_has_load_distance += with_load_distance_routes_list[index]
                    vehicle.number_of_dist += len(route) - 1
                    vehicle.number_of_dist_with_no_load += number_of_dist_with_no_load_routes_list[index]
                    vehicle.number_of_dist_with_load += number_of_dist_with_load_routes_list[index]
                    vehicle.add_route_average_load_factor(average_capacity_utilization_routes_list[index])
                    vehicle.completed_order += order_id_sequence
                    
                    total_distance += total_distance_routes_list[index]
                    total_no_load_distance_all += no_load_distance_routes_list[index]
                    total_has_load_distance_all += with_load_distance_routes_list[index]
                    if vehicle.route_list != []:
                        popped_value = final_path.pop(0)
                        vehicle.route_list += final_path
                        
                        final_path.insert(0, popped_value)
                    else:
                        vehicle.route_list += final_path
                    chosen_vehicle = vehicle
                    vehicle_list.remove(vehicle)
                    # remove vehicle from the list then add again to then end of the list so that it has a kind of "cool down" effect
                    vehicle_list.append(chosen_vehicle)
                    break
            paths_for_cars.append(final_path)
            print("distance travel for this route:", total_distance_routes_list[index])
            print("average load factor for this route:", average_capacity_utilization_routes_list[index])

    # add vehicle to path
    for vehicle in vehicle_list:
        print("\nvehicle " + str(vehicle.id) + " - max capacity = " + str(vehicle.max_capacity) + ":", vehicle.route_list)
        print("total travel distance of car: ", vehicle.total_distance_of_car)
        print("total no load distance of car: ", vehicle.total_no_load_distance)
        print("total has load distance of car: ", vehicle.total_has_load_distance)
        print("Number of distances between two locations of car: ", vehicle.number_of_dist)
        print("Number of distances between two locations of car that have load : ", vehicle.number_of_dist_with_load)
        print("Number of distances between two locations of car that have  no load : ", vehicle.number_of_dist_with_no_load)
        print("Number of routes assigned: ", vehicle.number_of_routes)
        print("Number of orders completed: ", len(vehicle.completed_order))
        print("average load factor: ", vehicle.get_average_of_all_routes_average_load_factor())

    print("\nnumber of clusters: ", len(cluster_list))
    return paths_for_cars, total_distance, total_no_load_distance_all, total_has_load_distance_all
    
def find_journey_DBSCAN_without_capacity(pick_up_cluster, delivery_cluster, pickups_and_deliveries_cluster, depot_loc_list, vehicle_list):
    """
    Find route for VRP with DBSCAN without the capacitated constraint
    
    Args:

    `pick_up_cluster` : A cluster containing only pick up locations

    `delivery_cluster` : A cluster containing only delivery locations

    `pickups_and_deliveries_cluster`: A cluster containing both pick up and delivery locations

    `depot_loc_list` : an array containing all the depot locations

    `vehicle_list` : A array of all vehicles 

    Returns:

    `paths_for_cars` : a combined path of each of the vehicle
    `total_cost` : total distance of all vehicles
    `total_no_load_distance_all` : total travel distance without load

    """
    average_distance = calculater_average_distance(pick_up_cluster, DISTANCE_CALLBACK)
    # print("average_distance", avperage_distance)
    cluster_list = clusteringDBSCAN(pick_up_cluster,delivery_cluster, average_distance, depot_loc_list, 30)
    # return [], 0
    total_distance = 0
    paths_for_cars = []
    total_no_load_distance_all = 0

    for car_id, cluster in enumerate(cluster_list):
        pickup_and_deliveries_nodes = Cluster()

        # initialize the depot_loc index in the cluster, the default value is None
        depot_loc_index = None
        # find the index of the depot_loc
        for index, location in enumerate(cluster.location_list):
            for depot_loc in depot_loc_list:
                if depot_loc.id == location.id:
                    if depot_loc_index == None:
                        depot_loc_index = index
                    else:
                        cluster.location_list.pop(index) # if there are more than one parking location in a cluster, choose the first one and remove the rest

        # if there is no depot_loc in cluster then automatically add a default depot_loc, which is the first depot_loc in list
        if depot_loc_index == None:
            cluster.location_list.insert(0, depot_loc_list[0]) # add depot_loc location to each cluster
            depot_loc_index = 0
        print(cluster.location_list)
        distance = create_distance_city(cluster, DISTANCE_CALLBACK)

        # add max capacities of vehicles in fleet
        vehicle_max_capacities = []
        for vehicle in vehicle_list:
            vehicle_max_capacities.append(vehicle.max_capacity)
        vehicle_max_capacities.sort()

        #find optimal route
        path, distance, no_load_distance = find_journey_without_capacity(distance, depot_loc_index, depot_loc_index, cluster)             
        
        # construct path
        final_path = []
        for id in range(len(path)):
            final_path.append(cluster.location_list[path[id]])
        
        # construct order sequence list
        order_id_sequence = []
        for i in range(1, len(final_path) - 1):
            if final_path[i].pickup_delivery_value > 0: #is pickup point
                order_id_sequence.append(final_path[i].id_pickup_delivery)
        
        # add no_load_distance of route to total
        total_no_load_distance_all += no_load_distance

        # assign vehicle to route
        vehicle_id = None
        chosen_vehicle = random.choice(vehicle_list)                
        vehicle_id = chosen_vehicle.id
        chosen_vehicle.number_of_routes += 1
        if chosen_vehicle.route_list != []:
            popped_value = final_path.pop(0)
            chosen_vehicle.route_list += final_path
            final_path.insert(0, popped_value)
        else:
            chosen_vehicle.route_list += final_path
        if vehicle_id != None: # only calculate if a vehicle is assigned to route
            total_distance += distance
        paths_for_cars.append(final_path)
        print("car for this cluster: ", vehicle_id, ":")
        print(final_path)
        print("distance travel for this route:", distance)
        print("no load travel distance: ", no_load_distance)

    # add vehicle to path
    for vehicle in vehicle_list:
        print("\nvehicle " + str(vehicle.id) + ":", vehicle.route_list)

    print("number of clusters: ", len(cluster_list))
    return paths_for_cars, total_distance, total_no_load_distance_all

def start_algorithm(cluster, delivery_cluster, pickups_and_deliveries_cluster, depot_loc_list, vehicle_list):
        """
        Start the main algorithm to solve the VRP problem
        
        Args:

        `cluster` : A cluster containing only delivery locations

        `delivery_cluster`: Index of start location

        `pickups_and_deliveries_cluster` : A cluster containing both pick up and delivery locations

        `depot_loc_list` : an array containing all the depot locations

        `n_clusters`: Number of cluster to cluster in each cluster
        
        Returns:

        The list of cities presenting the path with pickup and delivery
        """
        pickup_cluster = cluster.copy()
        final_path, total_distance, total_no_load_distance_all, total_has_load_distance_all  = find_journey_DBSCAN_car_travel_distance_constraint(pickup_cluster, delivery_cluster, pickups_and_deliveries_cluster, depot_loc_list, vehicle_list)
        print("\ntotal distance of all cars: ", total_distance)
        print("total no load distance of all cars: ", total_no_load_distance_all)
        print("total has load distance of all cars: ", total_has_load_distance_all)
        average_load_factor_of_all_cars = 0
        number_of_utilized_cars = 0
        for vehicle in vehicle_list:
            if vehicle.get_average_of_all_routes_average_load_factor() > 0:
                number_of_utilized_cars += 1
            average_load_factor_of_all_cars += vehicle.get_average_of_all_routes_average_load_factor()
        average_load_factor_of_all_cars = average_load_factor_of_all_cars / number_of_utilized_cars
        print("average load factor of all cars: ", average_load_factor_of_all_cars)
        print("number of utilized cars: ", number_of_utilized_cars)
        return final_path            