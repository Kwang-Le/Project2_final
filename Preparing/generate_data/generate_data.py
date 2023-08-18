from numpy import genfromtxt
from time import time
import random
import math
import csv
import random

import pandas as pd

def write_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header (if any)
        header = ['Column1', 'Column2', 'Column3']  # Replace with your desired header names
        writer.writerow(header)
        
        # Write the data rows
        # for row in data:
        #     writer.writerow(row)
        writer.writerow(data)
            
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

data_amount = input("select the amount of data: 30, 60, 300, 1000: ")
coor = genfromtxt('./test_data/test_data_' + data_amount +'.csv', delimiter=',')
data = coor

#randomly generate data without source
# id_list = random.sample(range(len(data)-2), int(len(data) / 2) - 1)
# print(id_list)
# print(len(id_list))
# for id in range(len(id_list)):
#     pickups.append([id, 100])
#     deliveries.append([id, -100])
# pickups_and_deliveries_constraint = pickups + deliveries
# # randomize the pickups and deliveries
# np.random.shuffle(pickups_and_deliveries_constraint)

numbers = [50, 100, 200]
demands = []
for i in range(int(len(data) / 2) - 1):
    random_number = random.choice(numbers)
    demands.append(random_number)
# write_to_csv(demands, './test_data_28062023/data_299_demands.csv')
# print(demands)







def load_order(file, d):

    '''

    Load the order file, which contains order_id, src_id, dest_id and order_weight

    '''

    path = file + d + '.csv'

    dataframe = pd.read_csv(path)

    delivery_weight = dataframe["order_weight"]*(-1)

    dataframe["delivery_weight"] = delivery_weight

    pickups = dataframe[["order_id","src_id","order_weight"]]

    deliveries = dataframe[["order_id","dest_id","delivery_weight"]]

    pdorders = pd.concat([pickups, deliveries], names=['order_id',"loc_id","weight"])

    #return pickups, deliveries

    return pdorders

   

    #return pickup[], delivery[]





def load_location(file, d):

    '''

    Load the location file, which contains all possible locations with loc_id, lat and long

    '''

    path = file + d + '.csv'

    coor = pd.read_csv(path)

    return coor

    #return coor.values.tolist()






def generate_order_lists(df1, df2):

    '''

    Merge the location file with the order file to generate a new data frame which contains the order_id, the location_id.

    '''

    merge_src = pd.merge(left=df1, right=df2, left_on='src_id', right_on='loc_id')

    tmp1 = merge_src[["order_id","loc_id","lat","long", "order_weight"]]

    src_loc = tmp1.rename(columns = {"order_weight":"weight"})    

   

    merge_dest = pd.merge(left=df1, right=df2, left_on='dest_id', right_on='loc_id')

    tmp2 = merge_dest[["order_id","loc_id","lat","long","delivery_weight"]]

    dest_loc =tmp2.rename(columns = {"delivery_weight":"weight"})




    all_loc = pd.concat([src_loc,dest_loc])      

    all_loc.to_csv("./test_data/frame.csv")

   

    return all_loc, src_loc, dest_loc


data = generate_order_lists()