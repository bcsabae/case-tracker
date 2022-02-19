import datetime
import datetime as dt

STATUS_WAITING_ON_ENGINEER = "Waiting on me"
STATUS_WAITING_ON_CUSTOMER = "Waiting on customer"
STATUS_FIRST_RESPONSE = "First response needed"
STATUS_FROZEN = "Frozen"
TODAY_THRESHOLD = "10:00"


class Case:

    _date_format = "%Y.%m.%d. %H:%M"

    def __init__(self, num, customer, title, tier, lastResp=None, status=None):
        self.num = int(num)
        self.customer = customer
        self.title = title
        self.tier = int(tier)
        self.lastResp = lastResp
        self.status = status
        try_parse = self._parse_datetime(self.lastResp, self._date_format)
        if try_parse is None:
            exit(-1)

        self.lastResp = try_parse
        if self.status is None:
            self.status = STATUS_FIRST_RESPONSE

    def __str__(self):
        out = ""
        out += str(self.num) + ';'
        out += self.customer + ';'
        out += self.title + ';'
        out += str(self.tier) + ';'
        out += self.lastResp.strftime(self._date_format) + ';'
        out += self.get_due_string() + ';'
        out += self.status
        return out

    def to_csv(self):
        out = ""
        out += str(self.num) + ';'
        out += self.customer + ';'
        out += self.title + ';'
        out += str(self.tier) + ';'
        out += self.lastResp.strftime(self._date_format) + ';'
        out += self.status
        return out

    @staticmethod
    def from_csv(csv_str):
        c_arr = csv_str.split(';')

        num = int(c_arr[0])
        customer = c_arr[1]
        title = c_arr[2]
        tier = int(c_arr[3])
        lastResp = c_arr[4]
        status = c_arr[5]

        c = Case(num, customer, title, tier, lastResp=lastResp, status=status)

        return c

    def customer_answered(self, when=None):
        updated_at = self._parse_datetime(when, self._date_format)
        if updated_at is None:
            return
        self.lastResp = updated_at
        self.status = STATUS_WAITING_ON_ENGINEER

    def engineer_answered(self):
        self.status = STATUS_WAITING_ON_CUSTOMER

    def freeze(self):
        self.status = STATUS_FROZEN

    def get_due_date(self):
        if self.status == STATUS_WAITING_ON_CUSTOMER or self.status == STATUS_FROZEN:
            return None
        if self.status == STATUS_WAITING_ON_ENGINEER:
            return self._next_response_due(self.lastResp)
        if self.status == STATUS_FIRST_RESPONSE:
            return self._first_response_due(self.lastResp)

    def is_due_today(self):
        due = self.get_due_date()
        if due is None:
            return False
        threshold = self._add_weekend(datetime.datetime.today(), 1)
        threshold = threshold.replace(hour=int(TODAY_THRESHOLD.split(':')[0]), minute=int(TODAY_THRESHOLD.split(':')[1]))
        if due <= threshold:
            return True
        else:
            return False

    def is_due_tomorrow(self):
        due = self.get_due_date()
        if due is None:
            return False
        threshold = self._add_weekend(datetime.datetime.today(), 2)
        threshold = threshold.replace(hour=int(TODAY_THRESHOLD.split(':')[0]), minute=int(TODAY_THRESHOLD.split(':')[1]))
        if due <= threshold:
            return True
        else:
            return False

    def is_todo(self):
        return self.status == STATUS_WAITING_ON_ENGINEER \
               or self.status == STATUS_FROZEN \
               or self.status == STATUS_FIRST_RESPONSE

    def get_due_string(self):
        due = self.get_due_date()
        if due is None:
            return ""
        else:
            return due.strftime(self._date_format)

    def get_last_resp_string(self):
        return self.lastResp.strftime(self._date_format)

    @staticmethod
    def _parse_datetime(when, format):
        if when is None:
            updated_at = dt.datetime.today()
        elif type(when) == dt.datetime:
            updated_at = when
        else:
            try:
                updated_at = dt.datetime.strptime(when, format)
            except ValueError:
                print("Error while parsing date '{}', please provide the date in the following format:".format(when),
                      format,
                      'e.g:',
                      dt.datetime(year=2022, month=1, day=1, hour=12, minute=30).strftime(format)
                      )
                return None
        return updated_at

    def _next_response_due(self, updated_at):
        delay = 0

        if self.tier == 1:
            delay += 2
        elif self.tier == 2:
            delay += 3
        elif self.tier == 3:
            delay += 3
        elif self.tier == 4:
            delay += 4

        return self._add_weekend(updated_at, delay)

    def _first_response_due(self, opened_at):
        delay = 0

        if self.tier == 1:
            delay += 1
        elif self.tier == 2:
            delay += 1
        elif self.tier == 3:
            delay += 2
        elif self.tier == 4:
            delay += 4

        return self._add_weekend(opened_at, delay)

    @staticmethod
    def _add_weekend(to, delay):
        add_delay = 0
        while delay:
            add_delay += 1
            if (to + dt.timedelta(days=add_delay)).weekday() <= 4:
                delay -= 1
        return to + dt.timedelta(days=add_delay)