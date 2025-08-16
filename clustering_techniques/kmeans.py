import numpy as np

def kmeans(X, k, max_iters=100):
    """
    Performs k-means clustering on the given data.

    Args:
        X (np.ndarray): The data to cluster, where each row is a data point.
        k (int): The number of clusters to create.
        max_iters (int): The maximum number of iterations to perform.

    Returns:
        A tuple containing:
            - labels (np.ndarray): The cluster labels for each data point.
            - centroids (np.ndarray): The coordinates of the cluster centroids.
    """
    # Randomly initialize the centroids
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]

    for i in range(max_iters):
        # Assign each data point to the closest centroid
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)

        # Update the centroids
        new_centroids = np.array([X[labels == j].mean(axis=0) for j in range(k)])

        # If the centroids have not changed, then we have converged
        if np.all(centroids == new_centroids):
            break

        centroids = new_centroids

    return labels, centroids
