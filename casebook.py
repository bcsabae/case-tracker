import case

class Casebook:
    def __init__(self):
        self.cases = []
        pass

    def __str__(self):
        out = ""
        for case in self.cases:
            out += str(case)
            out += "\r\n"
        return out

    def __iter__(self):
        self._ind = 0
        return self

    def __next__(self):
        if self._ind < len(self.cases):
            act = self.cases[self._ind]
            self._ind += 1
            return act
        else:
            raise StopIteration

    def pretty_print(self, cases):
        space = 12
        heads = ["Number", "Customer", "Title", "Tier", "Last response", "Next response due", "Status"]
        all_spaces = 0
        for head in heads:
            if head is "Last response" or head is "Next response due" or head is "Status" or head is "Title":
                mult = 2
            else:
                mult = 1

            print(head, end=(' ' * (mult * space - len(head))))
            all_spaces += mult

        print("")
        print('-' * all_spaces * space)

        for case in cases:
            print(case.num, end=(' ' * (space - len(str(case.num)))))
            print(case.customer, end=(' ' * (space - len(case.customer))))
            print(case.title, end=(' ' * (2 * space - len(case.title))))
            print(case.tier, end=(' ' * (space - len(str(case.tier)))))
            print(case.getLastRespString(), end=(' ' * (2 * space - len(case.getLastRespString()))))
            print(case.getDueString(), end=(' ' * (2 * space - len(case.getDueString()))))
            print(case.status, end=(' ' * (2 * space - len(case.status))))
            print("")

    def read_csv(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                c = case.Case.fromCsv(line.rstrip())
                self.cases.append(c)
        self._library_file = filename
        return

    def write_csv(self, filename=None):
        if filename is None:
            filename = self._library_file
        with open(filename, 'w') as f:
            for case in self.cases:
                f.write(case.toCsv() + '\r\n')
        return

    def add_case(self, c):
        self.cases.append(c)

    def find_case(self, number):
        for case in self.cases:
            if case.num == number:
                return case
        return None

    def remove_case(self, number):
        for ind, case in enumerate(self.cases):
            if case.num == number:
                self.cases.pop(ind)
                return True
        return False

    def update_case(self, c):
        for ind, _case in enumerate(self.cases):
            if _case.num == c.num:
                self.cases[ind] = c
                return True
        return False

    def todo(self):
        todo_cases = Casebook()
        for case in self.cases:
            if case.isToDo():
                todo_cases.add_case(case)
        return todo_cases

    def today(self):
        today_cases = Casebook()
        for case in self.cases:
            if case.isDueToday():
                today_cases.add_case(case)
        return today_cases

    def tomorrow(self):
        tomorrow_cases = Casebook()
        for case in self.cases:
            if case.isDueTomorrow():
                tomorrow_cases.add_case(case)
        return tomorrow_cases

    def customer_answered(self, num, when=None):
        _case = self.find_case(num)
        if _case is None:
            print("No case with number", num)
            return None
        _case.customerAnswered(when=when)

    def engineer_answered(self, num):
        _case = self.find_case(num)
        if _case is None:
            print("No case with number", num)
            return None
        _case.aeAnswered()

    def freeze(self, num):
        _case = self.find_case(num)
        if _case is None:
            print("No case with number", num)
            return None
        _case.freeze()

    def new_case(self, num, customer, title, tier, opened_at=None):
        c = case.Case(num, customer, title, tier, lastResp=opened_at)
        self.cases.append(c)


