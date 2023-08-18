import random
from Clustering.Clustering import clusteringDBSCAN
from Integrating.integrating import find_journey_DBSCAN_car_travel_distance_constraint
from Model.model import Cluster
from Routing.routing import find_journey_without_capacity
from Utils.utils import calculater_average_distance, create_distance_city, distance_callback


DISTANCE_CALLBACK = distance_callback


def find_journey_DBSCAN_without_capacity(pick_up_cluster, delivery_cluster, pickups_and_deliveries_cluster, park_loc_list, vehicle_list):
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
        cluster_list = clusteringDBSCAN(pick_up_cluster,delivery_cluster, average_distance, park_loc_list, 30)
        # return [], 0
        total_cost = 0
        paths_for_cars = []
        total_no_load_distance_all = 0

        for car_id, cluster in enumerate(cluster_list):
            # if len(cluster.location_list) > 15:
                # path, cost = Congalgorithm2(cluster, pickups_and_deliveries_cluster, math.ceil(len(cluster.location_list) / 10))
            # else:
            pickup_and_deliveries_nodes = Cluster()

            # initialize the park_loc index in the cluster, the default value is None
            park_loc_index = None
            # find the index of the park_loc
            for index, location in enumerate(cluster.location_list):
                for park_loc in park_loc_list:
                    if park_loc.id == location.id:
                        if park_loc_index == None:
                            park_loc_index = index
                        else:
                            cluster.location_list.pop(index) # if there are more than one parking location in a cluster, choose the first one and remove the rest

            # if there is no park_loc in cluster then automatically add a default park_loc, which is the first park_loc in list
            if park_loc_index == None:
                cluster.location_list.insert(0, park_loc_list[0]) # add park_loc location to each cluster
                park_loc_index = 0
            print(cluster.location_list)
            # for location in cluster.location_list:
            #     pickup_and_deliveries_nodes.append(pickups_and_deliveries_cluster.location_list[location.id])
            # print("\npick up and deliveries constraint of this cluster: ", pickup_and_deliveries_nodes.location_list)
            distance = create_distance_city(cluster, DISTANCE_CALLBACK)

            # add max capacities of vehicles in fleet
            vehicle_max_capacities = []
            for vehicle in vehicle_list:
                vehicle_max_capacities.append(vehicle.max_capacity)
            vehicle_max_capacities.sort()

            #find optimal route
            path, cost, no_load_distance = find_journey_without_capacity(distance, park_loc_index, park_loc_index, cluster)             
            
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
                total_cost += cost
            paths_for_cars.append(final_path)
            print("car for this cluster: ", vehicle_id, ":")
            print(final_path)
            print("distance travel for this route:", cost)
            print("no load travel distance: ", no_load_distance)
            # print("has load travel distance: ", has_load_distance)
            # print("Order sequence: ", order_id_sequence)

        # add vehicle to path
        for vehicle in vehicle_list:
            print("\nvehicle " + str(vehicle.id) + ":", vehicle.route_list)

        print("number of clusters: ", len(cluster_list))
        return paths_for_cars, total_cost, total_no_load_distance_all

def find_journey_DBSCAN(pick_up_cluster, delivery_cluster, pickups_and_deliveries_cluster, park_loc_list, vehicle_list):
    """
    Find route for VRP with DBSCAN
    
    Args:

    `pick_up_cluster` : A cluster containing only pick up locations

    `delivery_cluster` : A cluster containing only delivery locations

    `pickups_and_deliveries_cluster`: A cluster containing both pick up and delivery locations
        
    `vehicle_list` : A array of all vehicles 

    Returns:

    none
    """
    average_distance = calculater_average_distance(pick_up_cluster, DISTANCE_CALLBACK)
    print("average_distance", average_distance)
    cluster_list = clusteringDBSCAN(pick_up_cluster,delivery_cluster, average_distance, park_loc_list, 0.05)
    total_cost = 0
    paths_for_cars = []
    total_no_load_distance_all = 0
    total_has_load_distance_all = 0
    total_average_load_factor = 0


    for car_id, cluster in enumerate(cluster_list):
        pickup_and_deliveries_nodes = Cluster()

        # if a cluster size is only one then skip
        if len(cluster.location_list) < 2:
            continue

        # initialize the park_loc index in the cluster, the default value is None
        park_loc_index = None
        # find the index of the park_loc
        for index, location in enumerate(cluster.location_list):
            for park_loc in park_loc_list:
                if park_loc.id == location.id:
                    if park_loc_index == None:
                        park_loc_index = index
                    else:
                        cluster.location_list.pop(index) # if there are more than one parking location in a cluster, choose the first one and remove the rest

        # if there is no park_loc in cluster then automatically add the next park_loc in the list, and then move that park_loc to the end of the list
        if park_loc_index == None:
            cluster.location_list.insert(0, park_loc_list[0]) # add park_loc location to each cluster
            park_loc_list.append(park_loc_list[0])
            #after adding the same park_loc to the back then remove it at the front of the list
            park_loc_list.pop(0)
            park_loc_index = 0
        print(cluster.location_list)
        distance = create_distance_city(cluster, DISTANCE_CALLBACK)

        # add max capacities of vehicles in fleet
        vehicle_max_capacities = []
        for vehicle in vehicle_list:
            if vehicle.max_capacity not in vehicle_max_capacities:
                vehicle_max_capacities.append(vehicle.max_capacity)
        vehicle_max_capacities.sort()

        #find optimal route
        path, cost, max_capacity, no_load_distance, has_load_distance, average_load_factor, number_of_dist_with_no_load, number_of_dist_with_load = find_optimal_path2(distance, park_loc_index, park_loc_index, cluster, vehicle_max_capacities)             
        
        # construct path
        final_path = []
        for id in range(len(path)):
            final_path.append(cluster.location_list[path[id]])
        
        # construct order sequence list
        order_id_sequence = []
        for i in range(1, len(final_path) - 1):
            if final_path[i].pickup_delivery_value > 0: #is pickup point
                order_id_sequence.append(final_path[i].id_pickup_delivery)
        

        # assign vehicle to route
        vehicle_id = None
        chosen_vehicle = None
        for vehicle in vehicle_list:
            # if vehicle max capacity is the same as the max capacity of route and the vehicle also has the same park_loc in route then assign that vehicle to route
            if vehicle.max_capacity == max_capacity and vehicle.park_loc_location == final_path[0].id:
                vehicle_id = vehicle.id
                vehicle.number_of_routes += 1
                vehicle.total_distance_of_car += cost
                vehicle.total_no_load_distance += no_load_distance
                vehicle.total_has_load_distance += has_load_distance
                vehicle.number_of_dist += len(path) - 1
                vehicle.number_of_dist_with_no_load += number_of_dist_with_no_load
                vehicle.number_of_dist_with_load += number_of_dist_with_load
                vehicle.add_route_average_load_factor(average_load_factor)
                vehicle.completed_order += order_id_sequence
                
                total_cost += cost
                total_no_load_distance_all += no_load_distance
                total_has_load_distance_all += has_load_distance
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
        print("distance travel for this route:", cost)

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
    return paths_for_cars, total_cost, total_no_load_distance_all, total_has_load_distance_all


def start_algorithm_experimentation(cluster, delivery_cluster, pickups_and_deliveries_cluster, park_loc_list, vehicle_list):
            """
            Create route for VRP
            
            Args:

            `cluster` : A cluster containing cities

            `start`: Index of start location

            `end` : Index of end location

            `n_clusters`: Number of cluster to cluster in each cluster
            
            Returns:

            The list of cities presenting the path with pickup and delivery
            """
            is_with_capacity = True
            if is_with_capacity == True:
                pickup_cluster = cluster.copy()
                final_path, total_cost, total_no_load_distance_all, total_has_load_distance_all  = find_journey_DBSCAN_car_travel_distance_constraint(pickup_cluster, delivery_cluster, pickups_and_deliveries_cluster, park_loc_list, vehicle_list)
                print("\ntotal cost of all cars: ", total_cost)
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
            else:
                pickup_cluster = cluster.copy()
                print(pickup_cluster.location_list)
                final_path, total_cost, total_no_load_distance_all = find_journey_DBSCAN_without_capacity(pickup_cluster, delivery_cluster, pickups_and_deliveries_cluster, park_loc_list, vehicle_list)
                number_of_utilized_cars = 0
                for vehicle in vehicle_list:
                    if vehicle.number_of_routes > 0:
                        number_of_utilized_cars += 1
                print("\ntotal cost of all cars: ", total_cost)
                print("total no load distance of all cars: ", total_no_load_distance_all)
                print("number of utilized cars: ", number_of_utilized_cars)
                return final_path