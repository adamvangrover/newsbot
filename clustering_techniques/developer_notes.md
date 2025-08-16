# Developer Notes

This directory contains various clustering algorithms that can be used to group similar news articles, social media posts, and other data sources.

## How to Use

To use a clustering algorithm, import the corresponding function from the appropriate file and call it with your data. For example, to use the k-means algorithm, you would do the following:

```python
from kmeans import kmeans

# Load your data
data = ...

# Cluster the data
labels, centroids = kmeans(data, k=3)
```

## How to Extend

To add a new clustering algorithm, create a new Python file in this directory that implements the algorithm. The file should have a function that takes a list of data points as input and returns a list of cluster labels.

You should also add a `README.md` file to the directory that explains how to use the new algorithm.
