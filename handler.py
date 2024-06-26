from datetime import datetime
from decorators import input_error
from models import AddressBook, Record

@input_error(strerror="Invalid command. Usage: add [ім'я] [номер телефону]")
def add_contact(args, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name, raise_error=False)
    message = "Contact added." if record is None else "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
    if phone:
        record.add_phone(phone)
    return message

@input_error(strerror="Invalid command. Usage: change [ім'я] [номер телефону] [новий номер телефону]")
def change_contact(args, book: AddressBook) -> str:
    name, phone, new_phone, *_ = args
    record = book.find(name, raise_error=True)
    record.edit_phone(phone, new_phone)
    return "Contact updated."

@input_error(strerror="Invalid command. Usage: delete [ім'я]")
def delete_contact(args, book: AddressBook) -> str:
    name, *_ = args
    book.delete(name)
    return "Contact deleted."

@input_error(strerror="Invalid command. Usage: contact [ім'я]")
def get_contact(args, book: AddressBook) -> Record:
    name, *_ = args
    record = book.find(name, raise_error=True)
    return record

def get_all_contacts(args, book: AddressBook) -> list:
    return [str(record) for record in book.data.values()]

@input_error(strerror="Invalid command. Usage: add-birthday [ім'я] [дата народження]")
def add_birthday(args, book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name, raise_error=True)
    record.add_birthday(birthday)
    return "Birthday added."

@input_error(strerror="Invalid command. Usage: show-birthday [ім'я]")
def show_birthday(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name, raise_error=True)
    if record.birthday is None:
        return "Birthday not set."
    return datetime.strftime(record.birthday.value, "%d.%m.%Y")

@input_error(strerror="Invalid command. Usage: birthdays")
def birthdays(args, book: AddressBook) -> str:
    bdays = book.get_upcoming_birthdays()
    if len(bdays) == 0:
        return "No upcoming birthdays."
    return "\n".join([f"{item['name']}: {item['congratulation_date']}" for item in bdays])
