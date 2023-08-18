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




depot_list1 = [0,
498,
648,
748,
898,
998,
1098,
1198,
1448,
1598,
1898
]

OFFSET = 2001

depot_list2 = [
0,
198,
348,
498,
698,
1298,
1598,
1898,
2198,
2398,
2598,
3498,
3798,
4098,
4298,
4598,
4798,
4998,
5098,
5498,
5698,
5998,
6198,
6398,
6598,
6798,
6998,
7198,
7398,
7598,
7798,
]

all_depot = []
all_depot += depot_list1
for depot_id in depot_list2:
    all_depot.append(depot_id + OFFSET)


vehicle_data = []
vehicle_capacity = [200,500,1000,1500]
vehicle_capacity_counter = 0
depot_counter = 0
res_data = []
for _ in range(42 * 30):
    if vehicle_capacity_counter == len(vehicle_capacity):
        vehicle_capacity_counter = 0
    if depot_counter == len(all_depot):
        depot_counter = 0
    capacity = vehicle_capacity[vehicle_capacity_counter]
    vehicle_capacity_counter += 1
    depot = all_depot[depot_counter]
    depot_counter += 1
    res_data.append([capacity, depot])

file_path = 'generate_vehicle_output.csv'
write_to_csv(res_data, file_path)

    
