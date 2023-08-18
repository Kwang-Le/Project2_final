import math
from sklearn.cluster import KMeans, DBSCAN
from Model.model import Location, Cluster, Vehicle

def clusteringDBSCAN(pick_up_cluster, delivery_cluster, average_distance, depot_loc_list, eps):
    """
    Clustering phase using DBSCAN
    
    Args:
    
    `pick_up_cluster`: The cluster with only pickups locations
        
    `delivery_cluster`: The cluster with only delivery locations

    `depot_loc_list` : an array containing all the depot locations

    `eps`: the epsilon value for the DBSCAN algorithm, set by the user
    
    Returns:

    The list of child clusters after clustering
    """
    coor = []
    data_weight = []
    for location in pick_up_cluster.location_list:
        coor.append([location.x, location.y])
        data_weight.append(1)
    # add depot_loc to cluster as well as weight to depot_loc locations so they will be the core nodes in cluster
    for depot_loc in depot_loc_list:
        pick_up_cluster.append(depot_loc)
        coor.append([depot_loc.x, depot_loc.y])
        data_weight.append(50)
    average_distance = average_distance / 100000
    DBscan = DBSCAN(eps=0.05,min_samples=3).fit(coor, sample_weight=data_weight)
    n_clusters_ = len(set(DBscan.labels_))

    cluster_list = [Cluster() for _ in range(n_clusters_)]
    

    for id, label in enumerate(DBscan.labels_):
        cluster_list[label].append(pick_up_cluster.location_list[id])

    # find and cluster big cluster into smaller clusters:
    index  = 0
    while index < len(cluster_list):
        if len(cluster_list[index].location_list) > 7:
            cluster_list += clusteringKMeans(cluster_list[index], math.ceil(len(cluster_list[index].location_list) / 7))
            cluster_list.pop(index)
        else:
            index += 1
    # add delivery nodes to cluster
    
    for cluster in cluster_list:
        res = []
        for pick_up_point in cluster.location_list:
            for delivery_point in delivery_cluster.location_list:
                if pick_up_point.id_pickup_delivery == delivery_point.id_pickup_delivery:
                    res.append(delivery_point)
        cluster.location_list += res

    print(DBscan.labels_)
    return cluster_list

def clusteringKMeans(cluster, n_clusters):
    """
    K-means clustering algorithm
    
    Args:
    
    `cluster`: The cluster
        
    `n_clusters`: Number of clusters you want to cluster
    
    Returns:

    The list of child clusters after clustering
    """
    coor = []
    for location in cluster.location_list:
        coor.append([location.x, location.y])

    kmeans = KMeans(n_clusters=n_clusters, random_state=5, n_init='auto').fit(coor)

    cluster_list = [Cluster() for _ in range(n_clusters)]

    for id, label in enumerate(kmeans.labels_):
        cluster_list[label].append(cluster.location_list[id])
    
    return cluster_list