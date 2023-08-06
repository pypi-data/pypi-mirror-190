class Metadata():
    def __init__(self, meta: list):
        self.data = meta

    def get_data(self):
        """
        Return list with JSON inside. This JSON containe all Metadata object variables.
        :param configuration: Configs object with base data
        :return: JSON
        """
        return self.data