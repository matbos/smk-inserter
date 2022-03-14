from datetime import datetime


class EntryData:

    def __init__(self, row):
        _date = datetime.strptime(row[0], "%Y-%m-%d") #"%d-%m-%Y")
        self.date = _date.strftime("%Y-%m-%d")
        self.year = int(row[1])
        self.procedure_code = int(row[2])
        self.operator = row[3]
        self.execution_place = int(row[4])
        self.internship_place = int(row[5])
        self.initials = self._short(row[6], row[7])
        self.gender = self._gender(row[6])
        self.assist = row[8]
        self.procedure_group = row[9]

    def __str__(self):
        return "{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(self.date, self.year, self.procedure_code, self.operator, self.execution_place, self.internship_place, self.initials, self.gender, self.assist)

    def _short(self, name, surname):
        names = name.split(' ')
        surnames = surname.split('-')
        return self._first_letters(names) + self._first_letters(surnames)

    @staticmethod
    def _gender(name):
        if name.strip()[-1] == 'a':
            return 'K'
        return 'M'

    @staticmethod
    def _first_letters(array):
        first = ""
        for a in array:
            first += a[0]
            first += '. '
        return first.upper()

