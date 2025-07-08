from collections import UserDict
from datetime import date, datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) < 10:
            raise ValueError("Phone number must be at least 10 digits long")
        super().__init__(value)
        self.value = value


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, '%d.%m.%Y').date()
            if parsed_date > date.today():
                raise ValueError("Birthday cannot be in the future")
            super().__init__(parsed_date)
        except ValueError as e:
            if str(e) == "Birthday cannot be in the future":
                raise e
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        birthday_info = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_info}"

    def add_phone(self, phone_number: str):
        if any(p.value == phone_number for p in self.phones):
            raise ValueError("Phone number already exists")
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        if any(p.value == new_phone_number for p in self.phones):
            raise ValueError("Phone number already exists")

        for i, phone in enumerate(self.phones):
            if phone.value == old_phone_number:
                self.phones[i] = Phone(new_phone_number)
                return

        raise ValueError("Phone number not found")

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone.value
        return None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise KeyError
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = date.today()
        congratulation_date_limit = today + timedelta(days=7)
        congratulation_list = []

        for name, record in self.data.items():
            if not record.birthday:
                continue

            birthday_date = record.birthday.value

            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= congratulation_date_limit:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                congratulation_list.append({
                    "name": name,
                    "congratulation_date": congratulation_date.strftime('%d.%m.%Y')
                })

        return congratulation_list
