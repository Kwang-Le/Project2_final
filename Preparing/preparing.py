import math

import numpy as np
from Model.model import Cluster, Location, Order, Vehicle
import csv


def write_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header (if any)
        header = ['Column1', 'Column2', 'Column3']  # Replace with your desired header names
        writer.writerow(header)
        
        # Write the data rows
        for row in data:
            writer.writerow(row)
            
    print(f"Data successfully written to {file_path}")

def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # Skip the header (if any)
        header = next(reader, None)
        
        # Read the data rows
        data = []
        for row in reader:
            num_arr = []
            for data_str in row:
                num_arr.append(int(data_str))
            data.append(num_arr)
            
    return data

def initiate_vehicle(data, vehicles_data):
    vehicle_list = []
    park_loc_list = []
    for index, row in enumerate(vehicles_data):
        new_vehicle = Vehicle(id=index, max_capacity=row[0], depot_loc_location=row[1])
        vehicle_list.append(new_vehicle)
        newLocation = Location(x=data[row[1]][0], y=data[row[1]][1], id = row[1]) # add park_loc location attribute to vehicle
        is_element_existed = False
        for location in park_loc_list:
            if location.id == row[1]:
                is_element_existed = True
        if is_element_existed == False:
            park_loc_list.append(newLocation)
    print(park_loc_list)
    return park_loc_list, vehicle_list

def get_pick_up_and_delivery_constraint(data, pickup_and_deliveries_data):
    pickups_and_deliveries_constraint = [None for _ in range(len(data) - 1)]
    for order_id, order in enumerate(pickup_and_deliveries_data):
        pickup_and_delivery_order = Order(order_id, order[0], order[1], order[2])
        pickups_and_deliveries_constraint[pickup_and_delivery_order.pickup_location] = [order_id, pickup_and_delivery_order.weight]
        pickups_and_deliveries_constraint[pickup_and_delivery_order.delivery_location] = [order_id, 0 - pickup_and_delivery_order.weight]
    return pickups_and_deliveries_constraint

def get_pick_up_and_delivery_constraint_without_weight(data, pickup_and_deliveries_data):
    pickups_and_deliveries_constraint = [None for _ in range(len(data) - 1)]
    for order_id, order in enumerate(pickup_and_deliveries_data):
        pickup_node_id = order[0]
        deliver_node_id = order[1]
        order_weight = order[2]
        pickups_and_deliveries_constraint[pickup_node_id] = [order_id, 100]
        pickups_and_deliveries_constraint[deliver_node_id] = [order_id, 0 - 100]
    return pickups_and_deliveries_constraint

def generate_data(park_loc_list, number_of_orders):
    pickups = []
    deliveries = []
    # number_of_orders = int((len(data) - (len(park_loc_list) + 1)) / 2)
    for id in range(number_of_orders):
        pickups.append([id, 100])
        deliveries.append([id, -100])
    pickups_and_deliveries_constraint = pickups + deliveries
    # randomize the pickups and deliveries
    np.random.shuffle(pickups_and_deliveries_constraint)
    return pickups_and_deliveries_constraint

def create_pick_up_and_delivery_cluster(data, park_loc_list,pickups_and_deliveries_constraint):
    counter = 0 
    pickups_and_deliveries_cluster = Cluster()
    for i in range(0,len(data) - 1):
        is_park_loc_location = False
        for park_loc in park_loc_list:
            if park_loc.id == i:
                is_park_loc_location = True
        if is_park_loc_location == False:
            newLocation = Location(x=data[i][0], y=data[i][1], id = i)
            while pickups_and_deliveries_constraint[counter] == None: # if parking location then continue until found a valid location
                print(counter)
                counter += 1 
            newLocation.id_pickup_delivery = pickups_and_deliveries_constraint[counter][0]
            newLocation.pickup_delivery_value = pickups_and_deliveries_constraint[counter][1]
            counter += 1 # increase counter only when the location is not a parking location
            pickups_and_deliveries_cluster.append(newLocation)
    return pickups_and_deliveries_cluster


# # define distance_callback
# def distance_callback(cityA, cityB):
#     xDis = (cityA.x - cityB.x)*(cityA.x - cityB.x)
#     yDis = (cityA.y - cityB.y)*(cityA.y - cityB.y)
#     distance = math.ceil(math.sqrt(xDis + yDis) * 100000)

#     return distance

# create distance for all nodes without clustering
def create_distance_no_cluster(bigCluster, distance_callback):
    n = bigCluster.get_quantity()
    distance = [[0] * n for i in range(n)]

    for id in range(n):
        for id_ in range(n):
            distance[id][id_] = distance_callback(bigCluster.location_list[id], bigCluster.location_list[id_])

    return distance