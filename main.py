from Integrating.integrating import start_algorithm
from Model.model import Cluster, Location, Vehicle
from Preparing.preparing import create_pick_up_and_delivery_cluster, get_pick_up_and_delivery_constraint, initiate_vehicle, read_csv
from Routing.routing import find_journey
import numpy as np
from numpy import genfromtxt
from time import time
import random
import math
import csv

# # define distance_callback
def distance_callback(cityA, cityB):
    xDis = (cityA.x - cityB.x)*(cityA.x - cityB.x)
    yDis = (cityA.y - cityB.y)*(cityA.y - cityB.y)
    distance = math.ceil(math.sqrt(xDis + yDis) * 100000)

    return distance

data_amount = input("select the amount of data: 30, 60, 300, 1000: ")
coor = genfromtxt('./test_data/test_data_' + data_amount + '.csv', delimiter=',')
data = coor
print(len(data))
vehicle_amount = input("select the amount of cars: 4, 16, 20, 100, 200 : ")
depot_amount = input("select the amount of depots: 1, 5: ")

pickup_and_deliveries_data = read_csv('./test_data_28062023/data_' + str(int(data_amount) -1) + '_order.csv')
vehicles_data = read_csv('./test_data_28062023/data_' + vehicle_amount + '_vehicles_' + depot_amount  + '_depots' +'.csv')

pickup_cluster = Cluster()
delivery_cluster = Cluster()




#get vehicle and parking location data
park_loc_list, vehicle_list = initiate_vehicle(data, vehicles_data)


#if have a data source
number_of_orders = len(pickup_and_deliveries_data)

#if want to run CMPMDVRP (with capacity)
pickups_and_deliveries_constraint = get_pick_up_and_delivery_constraint(data, pickup_and_deliveries_data)

#if want to run MPMDVRP (without capacity)
# pickups_and_deliveries_constraint = get_pick_up_and_delivery_constraint_without_weight(pickup_and_deliveries_data)


#if do not have a data source then randomly generate pickup and delivery data without source
# number_of_orders = int((len(data) - (len(park_loc_list) + 1)) / 2)
# pickups_and_deliveries_constraint = generate_data(park_loc_list,number_of_orders)

pickups_and_deliveries_cluster = create_pick_up_and_delivery_cluster(data, park_loc_list, pickups_and_deliveries_constraint)

for location in pickups_and_deliveries_cluster.location_list:
    # append pickups data into cluster
    if location.pickup_delivery_value > 0: 
        newLocation = location
        pickup_cluster.append(newLocation)
    # append delivery data into cluster
    else:
        newLocation = location
        delivery_cluster.append(newLocation)

# find route
park_loc_location = Location(x=data[0][0], y=data[0][1], id = 0)

t0 = time()
paths = start_algorithm(pickup_cluster, delivery_cluster, pickups_and_deliveries_cluster, park_loc_list, vehicle_list)
t1 = time()
print('QuangVRP takes %f \n' %(t1-t0))
# print('path:', paths)





# test tsp with pickup and deliveries
# initiate cluster
# cluster = Cluster()
# for i in range(0,len(data) - 1):
#     newCity = City(x=data[i][0], y=data[i][1], id = i)
#     cluster.append(newCity)
# pickups_deliveries = [[-1,-1,-1] for i in range(number_of_orders)]
# numbers = [50, 100, 200]
# demands = []
# for i in range(int(len(data) / 2) - 1):
#     random_number = random.choice(numbers)
#     demands.append(random_number)
# for i, city in enumerate(pickups_and_deliveries_cluster.city_list):
#     if city.pickup_delivery_value < 0:
#         pickups_deliveries[city.id_pickup_delivery][1] = city.id
#     else:
#         pickups_deliveries[city.id_pickup_delivery][0] = city.id
#     pickups_deliveries[city.id_pickup_delivery][2] = random_number = random.randrange(10, 200)
# print(pickups_deliveries)
# file_path = './test_data_28062023/data_' + str(int(data_amount) -1) + '_order.csv'
# write_to_csv(pickups_deliveries, file_path)

# distance = create_distance_no_cluster(cluster, distance_callback)
# file_path = './test_data_28062023/data_' + str(int(data_amount) -1) + '_distance_matrix.csv'
# write_to_csv(distance, file_path)

  