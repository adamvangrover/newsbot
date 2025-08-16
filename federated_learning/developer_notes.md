# Developer Notes

This directory contains a basic federated learning framework. The framework consists of a `Client` class and a `Server` class. The `Client` class represents a single client in the system, and the `Server` class represents the central server.

## How to Use

To use the federated learning framework, you first need to create a list of clients. Each client should have its own data. You can then create a `Server` object and pass it the list of clients. Finally, you can call the `train()` method on the `Server` object to train the global model.

```python
from client import Client
from server import Server

# Create a list of clients
clients = [
    Client(client_id=1, data=...),
    Client(client_id=2, data=...),
]

# Create a server
server = Server(clients)

# Train the global model
server.train(num_rounds=10)
```

## How to Extend

To extend the federated learning framework, you can modify the `Client` and `Server` classes. For example, you could add support for different types of models, or you could implement a more sophisticated aggregation algorithm.

You should also add a `README.md` file to the directory that explains how to use your new features.
