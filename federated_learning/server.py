import numpy as np

class Server:
    """
    This is a class for a server in a federated learning system.
    """
    def __init__(self, clients):
        """
        Initializes a new server.

        Args:
            clients (list): A list of clients in the system.
        """
        self.clients = clients
        self.model = None

    def train(self, num_rounds):
        """
        Trains the global model for a number of rounds.

        Args:
            num_rounds (int): The number of rounds to train for.
        """
        for i in range(num_rounds):
            print(f"Round {i+1}")
            # Send the global model to each client
            for client in self.clients:
                client.train(self.model)

            # Aggregate the client models
            self.aggregate_models()

    def aggregate_models(self):
        """
        Aggregates the models from all of the clients.
        """
        # Get the models from all of the clients
        client_models = [client.get_model() for client in self.clients]

        # Average the weights of the models
        new_weights = np.mean([model.get_weights() for model in client_models], axis=0)

        # Set the weights of the global model
        self.model.set_weights(new_weights)

    def get_model(self):
        """
        Returns the global model.
        """
        return self.model
