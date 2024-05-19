import re
import datetime

from collections import UserDict

class Field:
    def __init__(self, value: any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Field):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    pattern = r"[+\d]"
    country_code = "38"

    def __init__(self, value: str) -> None:
        phone = "".join(re.findall(self.pattern, value))

        if not phone.startswith("+"):
            phone = re.sub(fr"^({self.country_code})?", f"+{self.country_code}", phone)

        if len(phone) != 13:
            raise ValueError("Invalid phone number. Use (+38) XXX-XXX-XX-XX format.")

        super().__init__(phone)

class Birthday(Field):
    def __init__(self, value: str) -> None:
        bday = None
        try:
            bday = datetime.datetime.strptime(value, "%d.%m.%Y")
        except ValueError as e:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from e
        if bday > datetime.datetime.now():
            raise ValueError("Birthday can't be in the future.")
        if bday.year < 1900:
            raise ValueError("Birthday can't be earlier than 1900.")
        super().__init__(bday)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        if self.find_phone(phone):
            raise ContactError("Phone number already exists.")

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        existing_phone = self.find_phone(phone)
        if existing_phone:
            self.phones.remove(existing_phone)

    def edit_phone(self, phone: str, new_phone: str):
        existing_phone = self.find_phone(phone)
        if not existing_phone:
            raise ContactError("No such phone number.")

        if self.find_phone(new_phone):
            raise ContactError("New phone number already exists.")

        self.phones[self.phones.index(existing_phone)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        target_phone = Phone(phone)
        return next((p for p in self.phones if p == target_phone), None)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        chunks = []
        chunks.append(f"Contact name: {self.name}")
        chunks.append(f"phones: {'; '.join(p.value for p in self.phones)}")
        if self.birthday:
            chunks.append(f"birthday: {self.birthday.value.strftime('%d.%m.%Y')}")
        return ", ".join(chunks)

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        if record.name in self.data:
            raise ContactError("Contact already exists.")

        self.data[record.name] = record

    def find(self, name: str, raise_error: bool = True) -> Record | None:
        name = Name(name)

        if name not in self.data:
            if raise_error:
                raise ContactError("No such contact.")
            return None

        return self.data[name]

    def delete(self, name: str):
        name = Name(name)

        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.date.today()
        upcoming_birthdays = []

        for user in self.data.values():
            if user.birthday is not None:
                # user.birthday.value is already a datetime.date object
                birthday = user.birthday.value
                birthday_this_year = datetime.date(today.year, birthday.month, birthday.day)
                # 7 days including today is 6 days from today
                if today <= birthday_this_year <= (today + datetime.timedelta(days=6)):
                    congratulation_date = birthday_this_year
                    if birthday_this_year.weekday() in (5, 6):
                        congratulation_date = birthday_this_year + \
                            datetime.timedelta(days = 7 - birthday_this_year.weekday())

                    upcoming_birthdays.append(
                        {
                            'name': user.name.value,
                            'congratulation_date': congratulation_date.strftime("%d.%m.%Y"),
                        }
                    )

        return upcoming_birthdays


class ContactError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
