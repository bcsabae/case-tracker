import json


class Config:

    date_format = []
    today_threshold = []
    response_times = []
    library = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self, file='config.json'):
        Config.date_format = "%Y.%m.%d. %H:%M"
        Config.today_threshold = "10:00"
        Config.library = "lib.csv"
        Config.response_times = []
        if not self.read_config(file):
            print("Could not initialize configuration")

    def read_config(self, file):
        try:
            with open(file) as file:
                config = json.load(file)
        except FileNotFoundError:
            print("ERROR: file", file, "not found")
            return False

        try:
            Config.date_format = config["time_format"]
        except KeyError:
            pass

        try:
            Config.today_threshold = config["today_threshold"]
        except KeyError:
            pass

        try:
            Config.library = config["library"]
        except KeyError:
            pass

        try:
            Config.response_times = config["response_times"]
        except KeyError:
            print("ERROR: response times not set in", file)
            return False

        return True

    @staticmethod
    def get_config(key):
        try:
            return getattr(Config, key)
        except AttributeError:
            return None

    @staticmethod
    def get_response_time(tier, first=False):
        for possible_match in Config.response_times:
            if possible_match["tier"] == tier:
                return possible_match["follow_up_response"] if not first else possible_match["first_response"]
        return None
