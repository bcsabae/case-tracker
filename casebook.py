import case


class Casebook:
    def __init__(self):
        self.cases = []
        self._library_file = None
        pass

    def __str__(self):
        out = ""
        for _case in self.cases:
            out += str(_case)
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

    @staticmethod
    def pretty_print(cases):
        space = 12
        heads = ["Number", "Customer", "Title", "Tier", "Last response", "Next response due", "Status", "Drafted"]
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

        for _case in cases:
            print(_case.num, end=(' ' * (space - len(str(_case.num)))))
            print(_case.customer, end=(' ' * (space - len(_case.customer))))
            print(_case.title, end=(' ' * (2 * space - len(_case.title))))
            print(_case.tier, end=(' ' * (space - len(str(_case.tier)))))
            print(_case.get_last_resp_string(), end=(' ' * (2 * space - len(_case.get_last_resp_string()))))
            print(_case.get_due_string(), end=(' ' * (2 * space - len(_case.get_due_string()))))
            print(_case.status, end=(' ' * (2 * space - len(_case.status))))
            print(_case.draft_str(), end=(' ' * (2 * space - len(_case.draft_str()))))
            print("")

    def read_csv(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                c = case.Case.from_csv(line.rstrip())
                self.cases.append(c)
        self._library_file = filename
        return

    def write_csv(self, filename=None):
        if filename is None:
            filename = self._library_file
        with open(filename, 'w') as f:
            for _case in self.cases:
                f.write(_case.to_csv() + '\r\n')
        return

    def add_case(self, c):
        self.cases.append(c)

    def find_case(self, number):
        for _case in self.cases:
            if _case.num == number:
                return _case

        # if no direct match was found, try guessing
        potential_case = self.guess_case(number)

        if potential_case != None:
            print(f"Guessed case {potential_case.num}")
        return potential_case
    
    def guess_case(self, short_number):
        short_num_str = str(short_number)
        found_case = None
        for _case in self.cases:
            num_str = str(_case.num)
            if num_str.endswith(short_num_str):
                if found_case == None:
                    found_case = _case
                else:
                    print(f"Ambiguous case numbers with ending {short_number}")
                    return None
        return found_case

    def remove_case(self, number):
        for ind, _case in enumerate(self.cases):
            if _case.num == number:
                self.cases.pop(ind)
                return True
        return False

    def update_case(self, c):
        for ind, _case in enumerate(self.cases):
            if _case.num == c.num:
                self.cases[ind] = c
                return True
        return False

    def _order_cases(self, cases):
      def sorter(case):
        possible_due_date = case.get_due_date()
        if possible_due_date == None:
          return case.get_last_resp()
        else:
          return possible_due_date
      sorted_cases = sorted(cases, key=sorter)
      return sorted_cases
        
    def todo(self):
        todo_cases = Casebook()
        for _case in self.cases:
            if _case.is_todo():
                todo_cases.add_case(_case)
        return self._order_cases(todo_cases)

    def today(self):
        today_cases = Casebook()
        for _case in self.cases:
            if _case.is_due_today():
                today_cases.add_case(_case)
        return self._order_cases(today_cases)

    def tomorrow(self):
        tomorrow_cases = Casebook()
        for _case in self.cases:
            if _case.is_due_tomorrow():
                tomorrow_cases.add_case(_case)
        return self._order_cases(tomorrow_cases)

    def customer_answered(self, num, when=None):
        _case = self.find_case(num)
        if _case is None:
            print("No case with number", num)
            return None
        _case.customer_answered(when=when)

    def engineer_answered(self, num):
        _case = self.find_case(num)
        if _case is None:
            print("No case with number", num)
            return None
        _case.engineer_answered()

    def drafted(self, num, undraft=False):
        _case = self.find_case(num)
        if _case is None:
            print("No case with number", num)
            return None
        _case.drafted(undraft=undraft)

    def freeze(self, num):
        _case = self.find_case(num)
        if _case is None:
            print("No case with number", num)
            return None
        _case.freeze()

    def new_case(self, num, customer, title, tier, opened_at=None):
        c = case.Case(num, customer, title, tier, lastResp=opened_at, isDraft=False)
        self.cases.append(c)


