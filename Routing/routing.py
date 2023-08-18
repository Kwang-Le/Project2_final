

def find_journey(distance:list, start, end, pickup_and_deliveries_locations, vehicle_max_capacities):

    """
    Find the most optimal path starting from start node to end node with memoization
    
    Args:
    
    `distance`: The list distance between each 2 nodes

    `start`: Start location

    `end`: End location

    `pickups_and_deliveries_locations`: array of pickup and deliveries locations

    `vehicle_max_capacities`: a array containing all types of vehicle capacities

    Returns:

    A list presenting the path

    path, min_route

    max_capacity

    no_load_distance

    has_load_distance

    average_capacity_utilization

    number_of_dist_with_no_load

    number_of_dist_with_load

    """

    # Quang algorithm
    
    n = len(distance)
    num_bitmask = (1<<n)
    vehicle_capacity = vehicle_max_capacities
    dp = [[-1] * n for i in range(num_bitmask)]
    dp_capacity = [[-1] * n for i in range(num_bitmask)]
    dist = distance
    max_capacity = vehicle_capacity[0]

    VISITED_ALL = (1<<n) - 1

    def tsp(mask, pos, current_capacity, pickup_and_deliveries_locations, max_capacity, order_onboard):
        # print("recursion round")
        if mask == VISITED_ALL :
            # print("end of a route")
            # if end park_loc location then continue
            if pickup_and_deliveries_locations.location_list[end].pickup_delivery_value == None:
                pass
            elif pickup_and_deliveries_locations.location_list[end].pickup_delivery_value <= 0: # if delivery
                if current_capacity > 0:
                    current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                    order_onboard.remove(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            else:                                    #if pickup
                if current_capacity < max_capacity:
                    current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                else:
                    for new_max_capacity in vehicle_capacity:
                        # upgrade capacity of car
                        if new_max_capacity >= current_capacity + pickup_and_deliveries_locations.location_list[end].pickup_delivery_value:
                            # print("end up capacity!!!!!!!!")
                            max_capacity = new_max_capacity
                            current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                            
                            break
                order_onboard.append(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            return dist[pos][end], max_capacity
            
        if dp[mask][pos]  != -1:
        #     # print(dp_capacity[mask][pos],  pickup_and_deliveries_locations)
            return dp[mask][pos], dp_capacity[mask][pos]
        
        ans = 1e9
        ans_capacity = 1e9
        # if start park_loc then ignore
        if pos == start:
            pass
         # if delivery
        elif pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value <= 0: 
            # if there is cargo on car then deliver
            if current_capacity > 0:
                current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
                # remove finished order after delivery
                order_onboard.remove(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery)
        # if pickup
        else: 
            # if pickup new cargo is within max capacity then pick up                                 
            if current_capacity + pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value <= max_capacity:
                current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
            # else upgrade capacity of car
            else:
                for new_max_capacity in vehicle_capacity:
                    # nang capacity cua xe 
                    if new_max_capacity >= current_capacity + pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value:
                        # print("up capacity!!!!!!!!")
                        # print("current_pos: " + str(pos) + " current_capacity: " + str(current_capacity))
                        # print(current_capacity, pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value)
                        max_capacity = new_max_capacity
                        current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
                        break
            # add pickup order to car
            order_onboard.append(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery)

        # print("current_pos: " + str(pos) + " current_capacity: " + str(current_capacity))
        for location in range(n):
            if mask&(1<<location) == 0: # if the next node is not visited
                # if next node is a delivery but there is no cargo on car or if there is no equivalent pickup and delivery order onboard to deliver then skip
                if pickup_and_deliveries_locations.location_list[location].pickup_delivery_value <= 0:
                    if current_capacity <= 0 or (pickup_and_deliveries_locations.location_list[location].id_pickup_delivery not in order_onboard):
                        # print("skipping")
                        continue
                # else continue with the next node
                result_route, result_capacity = tsp(mask|(1<<location), location, current_capacity, pickup_and_deliveries_locations, max_capacity, order_onboard)
                newAns = dist[pos][location] + result_route
                newAns_capacity = max_capacity + result_capacity
                ans = min(ans, newAns) # find minium total travel distance in route
                # update capacity_utilization
                if min(ans, newAns) < ans:
                    pass
                ans_capacity = min(ans_capacity, newAns_capacity) # find minium total capacity in route         

        # update dp
        dp[mask][pos] = ans
        dp_capacity[mask][pos] = ans_capacity
        return dp[mask][pos], dp_capacity[mask][pos]

    

    mask = (1<<start)|(1<<end) # start and end points are visited
    start_capacity = 0
    starting_order_onboard = []
    min_route, min_capacity_cost = tsp(mask,start, start_capacity, pickup_and_deliveries_locations, max_capacity, starting_order_onboard)
    # print(min_route)
    # print("minium capacity_cost possible: ", min_capacity_cost)
    # print(dp)
    c_city = start
    path = []
    path.append(start)
    remain_dist = min_route

    # # trace the path min route
    while mask != VISITED_ALL:
        for n_city in range(len(dist)):
            if n_city in path:
                continue

            # check if all location are nearly visisted
            if mask|(1<<n_city) ==  VISITED_ALL:
                path.append(n_city)
                mask = mask|(1<<n_city)
                break

            # Backtrack the route and check which point add up to the minium distance
            if dp[mask|(1<<n_city)][n_city] + dist[n_city][c_city] == remain_dist:
                path.append(n_city)

                # update the remain distance 
                remain_dist = dp[mask|(1<<n_city)][n_city]

                c_city = n_city
                mask = mask|(1<<n_city)
                break
    
    path.append(end)

    # find max_capacity of final route, also find the total distance travel without load
    max_capacity = vehicle_capacity[0]
    current_capacity = 0
    no_load_distance = 0
    number_of_dist_with_no_load = 0
    for index, location in enumerate(path):
        if location != start:
            current_capacity += pickup_and_deliveries_locations.location_list[location].pickup_delivery_value
        if current_capacity == 0:
            if index < len(path) - 1:
                no_load_distance += dist[path[index]][path[index +1]]
                number_of_dist_with_no_load += 1
        if current_capacity > max_capacity:
            for new_max_capacity in vehicle_capacity:
                        # nang capacity cua xe 
                        if new_max_capacity >= current_capacity:
                            max_capacity = new_max_capacity
                            break
    number_of_dist_with_load = (len(path) - 1) - number_of_dist_with_no_load
    print("max capacity of route: ", max_capacity)
    # find capacity utilization for final route
    average_capacity_utilization = 0

    # reinitiate current_capacity
    current_capacity = 0
    for city_id in range(1, len(path) - 2):
        current_capacity += pickup_and_deliveries_locations.location_list[path[city_id]].pickup_delivery_value 
        # capacity_between_two_cities = pickup_and_deliveries_locations.location_list[path[city_id]].pickup_delivery_value + pickup_and_deliveries_locations.location_list[path[city_id + 1]].pickup_delivery_value
        average_capacity_utilization += current_capacity / max_capacity
    average_capacity_utilization = average_capacity_utilization /(len(path) - 1)
    print("average capacity utilization: %.2f" % average_capacity_utilization)
    return (path, min_route, max_capacity, no_load_distance, min_route - no_load_distance, average_capacity_utilization, number_of_dist_with_no_load, number_of_dist_with_load)

def find_journey_car_travel_distance_constraint(distance:list, start, end, pickup_and_deliveries_locations, vehicle_max_capacities):
    """
    Find the most optimal path starting from start node to end node with memoization and the constraint where a car can only travel less than 400km before returning
    
    Args:
    
    `distance`: The list distance between each 2 nodes

    `start`: Start location

    `end`: End location

    `pickups_and_deliveries_locations`: array of pickup and deliveries locations

    `vehicle_max_capacities`: a array containing all types of vehicle capacities

    Returns:

    A list presenting the path

    path
    
    min_route

    max_capacity

    no_load_distance

    has_load_distance

    average_capacity_utilization

    number_of_dist_with_no_load

    number_of_dist_with_load

    """

    # Quang algorithm
    
    n = len(distance)
    num_bitmask = (1<<n)
    vehicle_capacity = vehicle_max_capacities
    dp = [[-1] * n for i in range(num_bitmask)]
    dp_capacity = [[-1] * n for i in range(num_bitmask)]
    dist = distance
    max_capacity = vehicle_capacity[0]

    VISITED_ALL = (1<<n) - 1

    def tsp(mask, pos, current_capacity, pickup_and_deliveries_locations, max_capacity, order_onboard):
        # print("recursion round")
        if mask == VISITED_ALL :
            # print("end of a route")
            # if end park_loc location then continue
            if pickup_and_deliveries_locations.location_list[end].pickup_delivery_value == None:
                pass
            elif pickup_and_deliveries_locations.location_list[end].pickup_delivery_value <= 0: # if delivery
                if current_capacity > 0:
                    current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                    order_onboard.remove(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            else:                                    #if pickup
                if current_capacity < max_capacity:
                    current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                else:
                    for new_max_capacity in vehicle_capacity:
                        # upgrade capacity of car
                        if new_max_capacity >= current_capacity + pickup_and_deliveries_locations.location_list[end].pickup_delivery_value:
                            # print("end up capacity!!!!!!!!")
                            max_capacity = new_max_capacity
                            current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                            
                            break
                order_onboard.append(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            return dist[pos][end], max_capacity
            
        if dp[mask][pos]  != -1:
        #     # print(dp_capacity[mask][pos],  pickup_and_deliveries_locations)
            return dp[mask][pos], dp_capacity[mask][pos]
        
        ans = 1e9
        ans_capacity = 1e9
        # if start park_loc then ignore
        if pos == start:
            pass
         # if delivery
        elif pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value <= 0: 
            # if there is cargo on car then deliver
            if current_capacity > 0:
                current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
                # remove finished order after delivery
                order_onboard.remove(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery)
        # if pickup
        else: 
            # if pickup new cargo is within max capacity then pick up                                 
            if current_capacity + pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value <= max_capacity:
                current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
            # else upgrade capacity of car
            else:
                for new_max_capacity in vehicle_capacity:
                    # nang capacity cua xe 
                    if new_max_capacity >= current_capacity + pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value:
                        # print("up capacity!!!!!!!!")
                        # print("current_pos: " + str(pos) + " current_capacity: " + str(current_capacity))
                        # print(current_capacity, pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value)
                        max_capacity = new_max_capacity
                        current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
                        break
            # add pickup order to car
            order_onboard.append(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery)

        # print("current_pos: " + str(pos) + " current_capacity: " + str(current_capacity))
        for location in range(n):
            if mask&(1<<location) == 0: # if the next node is not visited
                # if next node is a delivery but there is no cargo on car or if there is no equivalent pickup and delivery order onboard to deliver then skip
                if pickup_and_deliveries_locations.location_list[location].pickup_delivery_value <= 0:
                    if current_capacity <= 0 or (pickup_and_deliveries_locations.location_list[location].id_pickup_delivery not in order_onboard):
                        # print("skipping")
                        continue
                # else continue with the next node
                result_route, result_capacity = tsp(mask|(1<<location), location, current_capacity, pickup_and_deliveries_locations, max_capacity, order_onboard)
                newAns = dist[pos][location] + result_route
                newAns_capacity = max_capacity + result_capacity
                ans = min(ans, newAns) # find minium total travel distance in route
                # update capacity_utilization
                if min(ans, newAns) < ans:
                    pass
                ans_capacity = min(ans_capacity, newAns_capacity) # find minium total capacity in route         

        # update dp
        dp[mask][pos] = ans
        dp_capacity[mask][pos] = ans_capacity
        return dp[mask][pos], dp_capacity[mask][pos]

    

    mask = (1<<start)|(1<<end) # start and end points are visited
    start_capacity = 0
    starting_order_onboard = []
    min_route, min_capacity_cost = tsp(mask,start, start_capacity, pickup_and_deliveries_locations, max_capacity, starting_order_onboard)
    # print(min_route)
    # print("minium capacity_cost possible: ", min_capacity_cost)
    # print(dp)
    c_city = start
    path = []
    path.append(start)
    remain_dist = min_route

    # # trace the path min route
    while mask != VISITED_ALL:
        for n_city in range(len(dist)):
            if n_city in path:
                continue

            # check if all location are nearly visisted
            if mask|(1<<n_city) ==  VISITED_ALL:
                path.append(n_city)
                mask = mask|(1<<n_city)
                break

            # Backtrack the route and check which point add up to the minium distance
            if dp[mask|(1<<n_city)][n_city] + dist[n_city][c_city] == remain_dist:
                path.append(n_city)

                # update the remain distance 
                remain_dist = dp[mask|(1<<n_city)][n_city]

                c_city = n_city
                mask = mask|(1<<n_city)
                break
    
    path.append(end)

    #TODO: check if car has to travel for more than 400km
    total_distance_routes_list = []
    max_capacity_routes_list = []
    no_load_distance_routes_list = []
    with_load_distance_routes_list = []
    average_capacity_utilization_routes_list = []
    number_of_dist_with_no_load_routes_list = []
    number_of_dist_with_load_routes_list = []

    routes_list = []
    smaller_route_path = [start] # initialize smaller route to be seperated with the parking_location
    car_travel_distance = 0
    max_distance_for_car = 400000
    for index in range(1, len(path)):
        car_travel_distance += dist[path[index-1]][path[index]]
        smaller_route_path.append(path[index])
        if path[index] == end:
            if len(smaller_route_path) > 2:
                routes_list.append(smaller_route_path)
                total_distance_routes_list.append(car_travel_distance)
            break
        if car_travel_distance + dist[path[index]][end] > max_distance_for_car:
            smaller_route_path.append(end) 
            routes_list.append(smaller_route_path)
            total_distance_routes_list.append(car_travel_distance + dist[path[index]][end])
            smaller_route_path = [start] # reinitialize smaller route to be seperated
            car_travel_distance = 0
    

    print(routes_list)
    # find max_capacity of final route, also find the total distance travel without load
    
    # the amount of cargo that was brought back by previous car
    brought_back_cargo = 0
    for route_index, route in enumerate(routes_list):
        max_capacity = vehicle_capacity[0]
        current_capacity = brought_back_cargo
        current_capacity_for_average_load_factor = brought_back_cargo
        no_load_distance = 0
        number_of_dist_with_no_load = 0

        # set the max_capacity to the accomodate the brought_back_cargo
        for capacity in vehicle_capacity:
            if capacity >= brought_back_cargo:
                max_capacity = capacity
                break
        print(current_capacity)
        for city_index, location in enumerate(route):
            if location != start:
                current_capacity += pickup_and_deliveries_locations.location_list[location].pickup_delivery_value
            if current_capacity == 0:
                if city_index < len(route) - 1:
                    no_load_distance += dist[route[city_index]][route[city_index +1]]
                    number_of_dist_with_no_load += 1
            if current_capacity > max_capacity:
                for new_max_capacity in vehicle_capacity:
                    # nang capacity cua xe 
                    if new_max_capacity >= current_capacity:
                        max_capacity = new_max_capacity
                        break
        # update the brought back cargo to the last current capacity of car
        brought_back_cargo = current_capacity

        number_of_dist_with_load = (len(route) - 1) - number_of_dist_with_no_load
        print("max capacity of route: ", max_capacity)
        # find capacity utilization for final route
        average_capacity_utilization = 0

        # reinitiate current_capacity
        for city_id in range(1, len(route) - 2):
            current_capacity_for_average_load_factor += pickup_and_deliveries_locations.location_list[route[city_id]].pickup_delivery_value 
            # capacity_between_two_cities = pickup_and_deliveries_locations.location_list[path[city_id]].pickup_delivery_value + pickup_and_deliveries_locations.location_list[path[city_id + 1]].pickup_delivery_value
            average_capacity_utilization += current_capacity_for_average_load_factor / max_capacity
        average_capacity_utilization = average_capacity_utilization /(len(route) - 1)
        # print("average capacity utilization: %.2f" % average_capacity_utilization)

        max_capacity_routes_list.append(max_capacity)
        no_load_distance_routes_list.append(no_load_distance)
        with_load_distance_routes_list.append(total_distance_routes_list[route_index] - no_load_distance)
        average_capacity_utilization_routes_list.append(average_capacity_utilization)
        number_of_dist_with_no_load_routes_list.append(number_of_dist_with_no_load)
        number_of_dist_with_load_routes_list.append(number_of_dist_with_load)

    return (routes_list, total_distance_routes_list, max_capacity_routes_list, no_load_distance_routes_list, with_load_distance_routes_list, average_capacity_utilization_routes_list, number_of_dist_with_no_load_routes_list, number_of_dist_with_load_routes_list)


def find_journey_without_capacity(distance:list, start, end, pickup_and_deliveries_locations):
    """
    Find the most optimal path starting from start node to end node with memoization and without capacitated constraint
    
    Args:
    
    `distance`: The list distance between each 2 nodes

    `start`: Start location

    `end`: End location

    `pickups_and_deliveries_locations`: array of pickup and deliveries locations

    Returns:

    A list presenting the path

    path
    
    min_route

    max_capacity

    no_load_distance

    has_load_distance

    average_capacity_utilization

    number_of_dist_with_no_load

    number_of_dist_with_load

    """

    # Quang algorithm
    
    n = len(distance)
    num_bitmask = (1<<n)
    dp = [[-1] * n for i in range(num_bitmask)]
    dist = distance

    VISITED_ALL = (1<<n) - 1

    def tsp(mask, pos, current_capacity, pickup_and_deliveries_locations, order_onboard):
        if mask == VISITED_ALL :
            # if end park_loc location then continue
            if pickup_and_deliveries_locations.location_list[end].pickup_delivery_value == None:
                pass
            elif pickup_and_deliveries_locations.location_list[end].pickup_delivery_value <= 0: # if delivery
                if current_capacity > 0:
                    current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                    order_onboard.remove(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            else:                                    #if pickup
                current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                order_onboard.append(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            return dist[pos][end]
            
        if dp[mask][pos]  != -1:
            return dp[mask][pos]
        
        ans = 1e9
        # if start park_loc then ignore
        if pos == start:
            pass
         # if delivery
        elif pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value <= 0: 
            # if there is cargo on car then deliver
            current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
             # remove finished order after delivery
            order_onboard.remove(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery) 
        # if pickup
        else: 
            # add pickup order to car
            current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
            order_onboard.append(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery)

        for location in range(n):
            if mask&(1<<location) == 0: # if the next node is not visited
                # if next node is a delivery but there is no cargo on car or if there is no equivalent pickup and delivery order onboard to deliver then skip
                if pickup_and_deliveries_locations.location_list[location].pickup_delivery_value <= 0:
                    if (pickup_and_deliveries_locations.location_list[location].id_pickup_delivery not in order_onboard):
                        continue
                # else continue with the next node
                result_route = tsp(mask|(1<<location), location, current_capacity, pickup_and_deliveries_locations, order_onboard)
                newAns = dist[pos][location] + result_route
                ans = min(ans, newAns) # find minium total travel distance in route

        # update dp
        dp[mask][pos] = ans
        return dp[mask][pos]

    

    mask = (1<<start)|(1<<end) # start and end points are visited
    starting_order_onboard = []
    start_capacity = 0
    min_route = tsp(mask,start,start_capacity, pickup_and_deliveries_locations, starting_order_onboard)
    c_city = start
    path = []
    path.append(start)
    remain_dist = min_route

    # # trace the path min route
    while mask != VISITED_ALL:
        for n_city in range(len(dist)):
            if n_city in path:
                continue

            # check if all location are nearly visisted
            if mask|(1<<n_city) ==  VISITED_ALL:
                path.append(n_city)
                mask = mask|(1<<n_city)
                break

            # Backtrack the route and check which point add up to the minium distance
            if dp[mask|(1<<n_city)][n_city] + dist[n_city][c_city] == remain_dist:
                path.append(n_city)

                # update the remain distance 
                remain_dist = dp[mask|(1<<n_city)][n_city]

                c_city = n_city
                mask = mask|(1<<n_city)
                break
    
    path.append(end)

    # find max_capacity of final route, also find the total distance travel without load
    current_capacity = 0
    no_load_distance = 0
    number_of_dist_with_no_load = 0
    for index, location in enumerate(path):
        if location != start:
            current_capacity += pickup_and_deliveries_locations.location_list[location].pickup_delivery_value
        if current_capacity == 0:
            if index < len(path) - 1:
                no_load_distance += dist[path[index]][path[index +1]]
                number_of_dist_with_no_load += 1

    return (path, min_route, no_load_distance)

def find_journey_without_update_capacity(distance:list, start, end, pickup_and_deliveries_locations, vehicle_max_capacities):
    """
    Find the most optimal path starting from start node to end node with memoization and without capacitated constraint
    
    Args:
    
    `distance`: The list distance between each 2 nodes

    `start`: Start location

    `end`: End location

    `pickups_and_deliveries_locations`: array of pickup and deliveries locations

    `vehicle_max_capacities`: a array containing all types of vehicle capacities

    Returns:

    A list presenting the path

    path
    
    min_route

    no_load_distance

    """

    # Quang algorithm
    
    n = len(distance)
    num_bitmask = (1<<n)
    vehicle_capacity = vehicle_max_capacities
    dp = [[-1] * n for i in range(num_bitmask)]
    dp_capacity = [[-1] * n for i in range(num_bitmask)]
    dist = distance
    max_capacity = vehicle_capacity[0]

    VISITED_ALL = (1<<n) - 1

    def tsp(mask, pos, current_capacity, pickup_and_deliveries_locations, max_capacity, order_onboard):
        if mask == VISITED_ALL :
            # if end park_loc location then continue
            if pickup_and_deliveries_locations.location_list[end].pickup_delivery_value == None:
                pass
            elif pickup_and_deliveries_locations.location_list[end].pickup_delivery_value <= 0: # if delivery
                if current_capacity > 0:
                    current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                    order_onboard.remove(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            else:                                    #if pickup
                if current_capacity < max_capacity:
                    current_capacity += pickup_and_deliveries_locations.location_list[end].pickup_delivery_value
                order_onboard.append(pickup_and_deliveries_locations.location_list[end].id_pickup_delivery)
            return dist[pos][end], max_capacity
            
        if dp[mask][pos]  != -1:
            return dp[mask][pos], dp_capacity[mask][pos]
        
        ans = 1e9
        ans_capacity = 1e9
        # if start park_loc then ignore
        if pos == start:
            pass
         # if delivery
        elif pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value <= 0: 
            # if there is cargo on car then deliver
            if current_capacity > 0:
                current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
                # remove finished order after delivery
                order_onboard.remove(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery)
        # if pickup
        else: 
            # if pickup new cargo is within max capacity then pick up                                 
            if current_capacity + pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value <= max_capacity:
                current_capacity += pickup_and_deliveries_locations.location_list[pos].pickup_delivery_value
            # add pickup order to car
            order_onboard.append(pickup_and_deliveries_locations.location_list[pos].id_pickup_delivery)

        for location in range(n):
            if mask&(1<<location) == 0: # if the next node is not visited
                # if next node is a delivery but there is no cargo on car or if there is no equivalent pickup and delivery order onboard to deliver then skip
                if pickup_and_deliveries_locations.location_list[location].pickup_delivery_value <= 0:
                    if current_capacity <= 0 or (pickup_and_deliveries_locations.location_list[location].id_pickup_delivery not in order_onboard):
                        continue
                #if next node is a pickup but the added capacity exceeds the max_capacity of car then continue
                elif current_capacity + pickup_and_deliveries_locations.location_list[location].pickup_delivery_value >= max_capacity:
                    continue
                # else continue with the next node
                result_route, result_capacity = tsp(mask|(1<<location), location, current_capacity, pickup_and_deliveries_locations, max_capacity, order_onboard)
                newAns = dist[pos][location] + result_route
                newAns_capacity = max_capacity + result_capacity
                ans = min(ans, newAns) # find minium total travel distance in route
                # update capacity_utilization
                if min(ans, newAns) < ans:
                    pass
                ans_capacity = min(ans_capacity, newAns_capacity) # find minium total capacity in route         

        # update dp
        dp[mask][pos] = ans
        dp_capacity[mask][pos] = ans_capacity
        return dp[mask][pos], dp_capacity[mask][pos]

    

    mask = (1<<start)|(1<<end) # start and end points are visited
    start_capacity = 0
    starting_order_onboard = []
    min_route, min_capacity_cost = tsp(mask,start, start_capacity, pickup_and_deliveries_locations, max_capacity, starting_order_onboard)
    c_city = start
    path = []
    path.append(start)
    remain_dist = min_route

    # # trace the path min route
    while mask != VISITED_ALL:
        for n_city in range(len(dist)):
            if n_city in path:
                continue

            # check if all location are nearly visisted
            if mask|(1<<n_city) ==  VISITED_ALL:
                path.append(n_city)
                mask = mask|(1<<n_city)
                break

            # Backtrack the route and check which point add up to the minium distance
            if dp[mask|(1<<n_city)][n_city] + dist[n_city][c_city] == remain_dist:
                path.append(n_city)

                # update the remain distance 
                remain_dist = dp[mask|(1<<n_city)][n_city]

                c_city = n_city
                mask = mask|(1<<n_city)
                break
    
    path.append(end)

    # find max_capacity of final route, also find the total distance travel without load
    current_capacity = 0
    no_load_distance = 0
    number_of_dist_with_no_load = 0
    for index, location in enumerate(path):
        if location != start:
            current_capacity += pickup_and_deliveries_locations.location_list[location].pickup_delivery_value
        if current_capacity == 0:
            if index < len(path) - 1:
                no_load_distance += dist[path[index]][path[index +1]]
                number_of_dist_with_no_load += 1
    number_of_dist_with_load = (len(path) - 1) - number_of_dist_with_no_load
    print("max capacity of route: ", max_capacity)
    # find capacity utilization for final route
    average_capacity_utilization = 0

    # reinitiate current_capacity
    current_capacity = 0
    for city_id in range(1, len(path) - 2):
        current_capacity += pickup_and_deliveries_locations.location_list[path[city_id]].pickup_delivery_value 
        average_capacity_utilization += current_capacity / max_capacity
    average_capacity_utilization = average_capacity_utilization /(len(path) - 1)
    print("average capacity utilization: %.2f" % average_capacity_utilization)
    return (path, min_route, max_capacity, no_load_distance, min_route - no_load_distance, average_capacity_utilization, number_of_dist_with_no_load, number_of_dist_with_load)