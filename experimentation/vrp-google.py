"""Simple Pickup Delivery Problem (PDP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
from time import time
import csv

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

def read_csv_pickup_delivery(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # Skip the header (if any)
        header = next(reader, None)
        
        # Read the data rows
        data = []
        for row in reader:
            num_arr = []
            for i in range(2):
                num_arr.append(int(row[i]))
            # for data_str in row:
            #     num_arr.append(int(data_str))
            data.append(num_arr)
            
    return data

def pickup_and_delivery_order_to_indexes(orders, data_length):
    res = [None for i in range(data_length)]
    for order in orders:
        res[order[0]] = 1
        res[order[1]] = -1
    return res


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = read_csv('./test_data_28062023/data_59_distance_matrix.csv')
    for rows in data['distance_matrix']:
        for number in rows:
            number = math.floor(int(number))
    data['pickups_deliveries'] = read_csv_pickup_delivery('./test_data_28062023/data_59_order.csv')
    data['pickups_deliveries_indexes_values'] = pickup_and_delivery_order_to_indexes(data['pickups_deliveries'], len(data['distance_matrix']))
    data['num_vehicles'] = 16
    data['depot'] = 1
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_no_load_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_no_load_distance = 0
        current_capacity = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
            
            if previous_index < len(data['distance_matrix']):
                pickup_delivery_index_value_weight = data['pickups_deliveries_indexes_values'][previous_index]
                if pickup_delivery_index_value_weight != None:
                    current_capacity += pickup_delivery_index_value_weight
            if current_capacity <= 0:
                route_no_load_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
            # print("route distance: ", route_distance)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'No load distance of the route: {}m\n'.format(route_no_load_distance)
        print(plan_output)
        total_distance += route_distance
        total_no_load_distance += route_no_load_distance
    print('Total Distance of all routes: {}m'.format(total_distance))
    print('Total Distance without load: {}m'.format(total_no_load_distance))


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    # print(data['distance_matrix'])

    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # print(data['distance_matrix'][0][1])
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        999999999999,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(
                delivery_index))
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == '__main__':
    t0 = time()
    main()
    t1 = time()
    print('Google OR takes %f \n' %(t1-t0))
