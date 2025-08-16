import numpy as np

def hierarchical_clustering(X, n_clusters):
    """
    Performs hierarchical clustering on the given data.

    Args:
        X (np.ndarray): The data to cluster, where each row is a data point.
        n_clusters (int): The number of clusters to create.

    Returns:
        A tuple containing:
            - labels (np.ndarray): The cluster labels for each data point.
    """
    # Initialize each data point as its own cluster
    clusters = [[i] for i in range(X.shape[0])]

    # Calculate the distance between each pair of data points
    distances = np.sqrt(((X - X[:, np.newaxis])**2).sum(axis=2))

    while len(clusters) > n_clusters:
        # Find the two closest clusters
        min_dist = np.inf
        merge_idx = (0, 0)
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = np.mean([distances[p1, p2] for p1 in clusters[i] for p2 in clusters[j]])
                if dist < min_dist:
                    min_dist = dist
                    merge_idx = (i, j)

        # Merge the two closest clusters
        clusters[merge_idx[0]].extend(clusters[merge_idx[1]])
        del clusters[merge_idx[1]]

    # Assign cluster labels to each data point
    labels = np.zeros(X.shape[0])
    for i, cluster in enumerate(clusters):
        for point in cluster:
            labels[point] = i

    return labels.astype(int)
