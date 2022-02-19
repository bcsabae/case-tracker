from casebook import Casebook


class Console:
    # commands to support:
    # list [all, todo, today, tomorrow]
    # case [num] [todo, answered, freeze, close]
    # case [new] [params...]
    # exit

    _handlers = None
    _casebook = None

    def __init__(self, casebook):
        self._handlers = {
            'list': {
                'all': self.list_all_handler,
                'todo': self.list_todo_handler,
                'today': self.list_today_handler,
                'tomorrow': self.list_tomorrow_handler
            },
            'case': {
                'num': self.case_num_handler,
                'new': self.case_new_handler
            },
            'exit': self.exit_handler,
            'help': self.help_handler
        }

        self._casebook = casebook
        pass

    def loop(self):
        while True:
            self.read_command()

    def read_command(self):
        command = input('> ')
        if not self.parse_command(command):
            print("Unsupported command")
        return

    def parse_command(self, command_string):
        handlers = self._handlers

        quote_in_progress = False
        command_words = []
        word = ''
        for idx in range(len(command_string)):
            letter = command_string[idx]
            if letter == "'" or letter == '"':
                if quote_in_progress:
                    command_words.append(word)
                    word = ''
                quote_in_progress = not quote_in_progress
                continue
            if not quote_in_progress and letter == ' ':
                if len(word):
                    command_words.append(word)
                word = ''
                continue
            word += letter
            if idx == len(command_string) - 1:
                command_words.append(word)

        if len(command_words) == 1:
            if command_string not in self._handlers:
                self.help_handler()
                return False
            command = handlers[command_string]
            if hasattr(command, '__call__'):
                command()
                return True
            else:
                return False

        if command_words[0] not in self._handlers:
            self.help_handler()
            return False

        for idx, word in enumerate(command_words):
            if word in handlers:
                command = handlers[word]
                if hasattr(command, '__call__'):
                    command(command_words[idx+1:])
                    return True
                else:
                    handlers = command
            else:
                return False

    def list_all_handler(self, *args):
        self._casebook.pretty_print(self._casebook.cases)

    def list_todo_handler(self, *args):
        self._casebook.pretty_print(self._casebook.todo())
        pass

    def list_today_handler(self, *args):
        self._casebook.pretty_print(self._casebook.today())
        pass

    def list_tomorrow_handler(self, *args):
        self._casebook.pretty_print(self._casebook.tomorrow())
        pass

    def case_num_handler(self, *args):
        if len(args) < 1:
            self.help_handler()
            return

        args = args[0]

        num = int(args[0])
        command = args[1]

        if len(args) >= 3:
            date = args[2]
        else:
            date = None

        if command == "update":
            self._casebook.customer_answered(num, when=date)
        elif command == "answer":
            self._casebook.engineer_answered(num)
        elif command == "freeze":
            self._casebook.freeze(num)
        elif command == "close":
            self._casebook.remove_case(num)
        else:
            self.help_handler()
            return

        self._casebook.write_csv()

    def case_new_handler(self, *args):
        args = args[0]
        print(args, len(args))
        if len(args) < 4:
            self.help_handler()
            return

        number, customer, title, tier = args[0], args[1], args[2], int(args[3])
        if len(args) >= 5:
            opened_at = args[4]
        else:
            opened_at = None

        self._casebook.new_case(int(number), customer, title, int(tier), opened_at=opened_at)
        self._casebook.write_csv()

    @staticmethod
    def exit_handler():
        exit()
        return True

    @staticmethod
    def help_handler():
        print("Supported commands:")
        print("list all/todo/today/tomorrow")
        print("case num [num] update/answer/freeze/close [date:optional]")
        print("case new [number] [customer] [title] [tier] [opened_at:optional]")
        print("exit")
        return
