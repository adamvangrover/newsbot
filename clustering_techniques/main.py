import numpy as np
from kmeans import kmeans
from dbscan import dbscan
from hierarchical import hierarchical_clustering

def main():
    """
    This is the main function for the clustering algorithms.
    """
    # Create a sample dataset
    X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])

    # Run the k-means algorithm
    labels, centroids = kmeans(X, k=2)
    print("K-means labels:", labels)
    print("K-means centroids:", centroids)

    # Run the DBSCAN algorithm
    labels = dbscan(X, eps=2, min_samples=2)
    print("DBSCAN labels:", labels)

    # Run the hierarchical clustering algorithm
    labels = hierarchical_clustering(X, n_clusters=2)
    print("Hierarchical clustering labels:", labels)

if __name__ == "__main__":
    main()
