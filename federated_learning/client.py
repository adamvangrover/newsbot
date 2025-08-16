import numpy as np

class Client:
    """
    This is a class for a client in a federated learning system.
    """
    def __init__(self, client_id, data):
        """
        Initializes a new client.

        Args:
            client_id (int): The ID of the client.
            data (np.ndarray): The data that the client has.
        """
        self.client_id = client_id
        self.data = data
        self.model = None

    def train(self, model):
        """
        Trains the client's model on its data.

        Args:
            model: The model to train.
        """
        self.model = model
        self.model.fit(self.data)

    def get_model(self):
        """
        Returns the client's model.
        """
        return self.model
