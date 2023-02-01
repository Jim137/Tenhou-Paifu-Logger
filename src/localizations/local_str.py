class local_str():
    def __init__(self):
        pass

    def load_data(self, data):
        for key in data:
            self.__setattr__(key, data[key])

    def __setattr__(self, name, val):
        super().__setattr__(name, val)

    def __getattr__(self, name):
        import json
        with open('./src/localizations/en.json') as f:
            data = json.load(f)
        return data[name]
