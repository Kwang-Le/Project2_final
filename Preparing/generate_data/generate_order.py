from CongVRP import CongVRP
from CongVRP.model import Cluster, City, Vehicle
from CongVRP.utils import find_optimal_path2
import numpy as np
from numpy import genfromtxt
from time import time
import random
import math
import csv
# Read coor

OFFSET = 495

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

def initiate_vehicle(vehicles_data):
    vehicle_list = []
    park_loc_list = []
    for index, row in enumerate(vehicles_data):
        new_vehicle = Vehicle(id=index, max_capacity=row[0], park_loc_location=row[1])
        vehicle_list.append(new_vehicle)
        newCity = City(x=data[row[1]][0], y=data[row[1]][1], id = row[1]) # add park_loc location attribute to vehicle
        is_element_existed = False
        for location in park_loc_list:
            if location.id == row[1]:
                is_element_existed = True
        if is_element_existed == False:
            park_loc_list.append(newCity)
    print(park_loc_list)
    return park_loc_list, vehicle_list

def get_pick_up_and_delivery_constraint(pickup_and_deliveries_data):
    pickups_and_deliveries_constraint = [None for _ in range(len(data) - 1)]
    for order_id, order in enumerate(pickup_and_deliveries_data):
        pickup_node_id = order[0]
        deliver_node_id = order[1]
        order_weight = order[2]
        # print(deliver_node_id, len(pickups_and_deliveries_constraint))
        pickups_and_deliveries_constraint[pickup_node_id] = [order_id, order_weight]
        pickups_and_deliveries_constraint[deliver_node_id] = [order_id, 0 - order_weight]
    return pickups_and_deliveries_constraint

def get_pick_up_and_delivery_constraint_without_weight(pickup_and_deliveries_data):
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
        deliveries.append([id , -100])
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
            newCity = City(x=data[i][0], y=data[i][1], id = i)
            while pickups_and_deliveries_constraint[counter] == None: # if parking location then continue until found a valid location
                counter += 1 
            newCity.id_pickup_delivery = pickups_and_deliveries_constraint[counter][0]
            newCity.pickup_delivery_value = pickups_and_deliveries_constraint[counter][1]
            counter += 1 # increase counter only when the location is not a parking location
            pickups_and_deliveries_cluster.append(newCity)
    return pickups_and_deliveries_cluster


# define distance_callback
def distance_callback(cityA, cityB):
    xDis = (cityA.x - cityB.x)*(cityA.x - cityB.x)
    yDis = (cityA.y - cityB.y)*(cityA.y - cityB.y)
    distance = math.ceil(math.sqrt(xDis + yDis) * 100000)

    return distance

# create distance for all nodes without clustering
def create_distance_no_cluster(bigCluster, distance_callback):
    n = bigCluster.get_quantity()
    distance = [[0] * n for i in range(n)]

    for id in range(n):
        for id_ in range(n):
            distance[id][id_] = distance_callback(bigCluster.city_list[id], bigCluster.city_list[id_])

    return distance

# data_amount = input("select the amount of data: 30, 60, 300, 1000: ")
# coor = genfromtxt('./test_data/test_data_' + data_amount +'.csv', delimiter=',')
coor = genfromtxt('./generate_order_input.csv', delimiter=',')
data = coor
print(len(data))
# vehicle_amount = input("select the amount of cars: 4, 16, 20, 100, 200 : ")
# depot_amount = input("select the amount of depots: 1, 5: ")

# pickup_and_deliveries_data = read_csv('./test_data_28062023/data_' + str(int(data_amount) -1) + '_order.csv')
# demands_data = read_csv('./test_data_28062023/data_' + str(int(data_amount) -1) + '_demands.csv')[0]
# vehicles_data = read_csv('./test_data_28062023/data_' + vehicle_amount + '_vehicles_' + depot_amount  + '_depots' +'.csv')

pickup_cluster = Cluster()
delivery_cluster = Cluster()




#get vehicle and parking location data
# park_loc_list, vehicle_list = initiate_vehicle(vehicles_data)
park_loc_list = []
# newCity = City(x=data[0][0], y=data[0][1], id = 0)
# newCity1 = City(x=data[1][0], y=data[1][1], id = 1)
# newCity2 = City(x=data[2][0], y=data[2][1], id = 2)
# depot_list = [0,
# 498,
# 648,
# 748,
# 898,
# 998,
# 1098,
# 1198,
# 1448,
# 1598,
# 1898,
# ]

# depot_list = [
# 0,
# 198,
# 348,
# 498,
# 698,
# 1298,
# 1598,
# 1898,
# 2198,
# 2398,
# 2598,
# 3498,
# 3798,
# 4098,
# 4298,
# 4598,
# 4798,
# 4998,
# 5098,
# 5498,
# 5698,
# 5998,
# 6198,
# 6398,
# 6598,
# 6798,
# 6998,
# 7198,
# 7398,
# 7598,
# 7798,
# ]

depot_list = [0]

# so parkinglot phai la so le
for id in depot_list:
    newCity = City(x=data[id][0], y=data[id][1], id = id)
    park_loc_list.append(newCity)


#if do not have a data source then randomly generate pickup and delivery data without source
number_of_orders = int((len(data) - (len(park_loc_list) + 1)) / 2)
pickups_and_deliveries_constraint = generate_data(park_loc_list,number_of_orders)

pickups_and_deliveries_cluster = create_pick_up_and_delivery_cluster(data, park_loc_list, pickups_and_deliveries_constraint)

for city in pickups_and_deliveries_cluster.city_list:
    # append pickups data into cluster
    if city.pickup_delivery_value > 0: 
        newCity = city
        pickup_cluster.append(newCity)
    # append delivery data into cluster
    else:
        newCity = city
        delivery_cluster.append(newCity)


print(pickups_and_deliveries_constraint)








# test tsp with pickup and deliveries
# initiate cluster
cluster = Cluster()
for i in range(0,len(data) - 1):
    newCity = City(x=data[i][0], y=data[i][1], id = i)
    cluster.append(newCity)
pickups_deliveries = [[-1,-1,-1] for i in range(number_of_orders)]
numbers = [50, 100, 200]
demands = []
for i in range(int(len(data) / 2) - 1):
    random_number = random.choice(numbers)
    demands.append(random_number)
for i, city in enumerate(pickups_and_deliveries_cluster.city_list):
    if city.pickup_delivery_value < 0:
        pickups_deliveries[city.id_pickup_delivery][1] = city.id + OFFSET
    else:
        pickups_deliveries[city.id_pickup_delivery][0] = city.id + OFFSET
    pickups_deliveries[city.id_pickup_delivery][2] = random_number = random.randrange(10, 200)
print(pickups_deliveries)
file_path = 'generate_order_output.csv'
write_to_csv(pickups_deliveries, file_path)

# distance = create_distance_no_cluster(cluster, distance_callback)
# file_path = './test_data_28062023/data_' + str(int(data_amount) -1) + '_distance_matrix.csv'
# write_to_csv(distance, file_path)

  