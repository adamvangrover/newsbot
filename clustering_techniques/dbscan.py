import numpy as np

def dbscan(X, eps, min_samples):
    """
    Performs DBSCAN clustering on the given data.

    Args:
        X (np.ndarray): The data to cluster, where each row is a data point.
        eps (float): The maximum distance between two samples for them to be considered
            as in the same neighborhood.
        min_samples (int): The number of samples in a neighborhood for a point to be
            considered as a core point.

    Returns:
        A tuple containing:
            - labels (np.ndarray): The cluster labels for each data point.
    """
    labels = np.full(X.shape[0], -1)
    cluster_id = 0

    for i in range(X.shape[0]):
        if labels[i] != -1:
            continue

        neighbors = np.where(np.sqrt(((X - X[i])**2).sum(axis=1)) < eps)[0]

        if len(neighbors) < min_samples:
            labels[i] = -1  # Mark as noise
            continue

        labels[i] = cluster_id
        seed_set = set(neighbors)
        seed_set.remove(i)

        while seed_set:
            current_point = seed_set.pop()
            if labels[current_point] == -1:
                labels[current_point] = cluster_id

            if labels[current_point] != -1:
                continue

            labels[current_point] = cluster_id
            new_neighbors = np.where(np.sqrt(((X - X[current_point])**2).sum(axis=1)) < eps)[0]

            if len(new_neighbors) >= min_samples:
                seed_set.update(new_neighbors)

        cluster_id += 1

    return labels
