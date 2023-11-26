class DummyModel:
    def __init__(self, name, return_value):
        self.return_value = return_value
        self.name = name

    def predict(self, data):
        return self.return_value
