import sys

if sys.version_info.major < 3:
    print("Python major versions below 3 are not supported")
    exit()

from case import Case
from casebook import Casebook
from console import Console
from config import Config

if __name__ == '__main__':
    conf = Config(file='config.json')

    if Config.date_format:
        Case.date_format = Config.date_format
    if Config.today_threshold:
        Case.today_threshold = Config.today_threshold
    Case.response_times = Config.response_times

    cb = Casebook()
    cb.read_csv(Config.library)
    c = Console(cb)
    c.loop()

