from case import Case
from casebook import Casebook
from console import Console
from config import Config

cb = Casebook()
cb.read_csv("lib.csv")

c = cb.find_case(1234)
print(c)

c = cb.find_case(12567)
print(c)

print("\n-----\n")

print(cb)
cb.remove_case(1235)
print(cb)

print("\n-----\n")

c = Case(1234, "vasarlo2", "uj leiras", 1, "2022.02.03. 10:10", "Waiting on customer")
cb.update_case(c)
print(cb)

print("\n-----\n")

c = Case(1236, "vasarlon", "leiras", 1, "2022.02.03. 10:10", "Waiting on customer")
cb.add_case(c)
print(cb)

print("\n-----\n")

todos = cb.todo()
print(todos)

print("\n-----\n")

cb.customer_answered(1234, when="2022.02.14. 16:34")
print(cb)

print("\n-----\n")

cb.engineer_answered(123)
print(cb)

print("\n-----\n")

for case in cb:
    print(str(case))

print("\n-----\n")

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

