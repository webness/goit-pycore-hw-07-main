"""Module for testing the handler functions."""

import datetime
import unittest
import handler

from models import AddressBook, Record, ContactError

class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        record = Record("Test")
        record.add_phone("068-123-45-67")
        self.book.add_record(record)

    def test_add_contact(self):
        msg = handler.add_contact(["John", "123-456-78-90"], self.book)
        self.assertIsNotNone(self.book.find("John", raise_error=False))
        self.assertEqual(msg, "Contact added.")


    def test_add_contact_phone(self):
        msg = handler.add_contact(["Test", "123-456-78-90"], self.book)
        contact = self.book.find("Test")
        self.assertEqual(contact.phones[1].value, "+381234567890")
        self.assertEqual(msg, "Contact updated.")

    def test_add_contact_phone_existing_error(self):
        msg = handler.add_contact(["Test", "096-123-46-57"], self.book)
        self.assertIn("Phone number already exists.", msg)

    def test_change_contact(self):
        msg = handler.change_contact(["Test", "096-123-46-57", "123-456-78-90"], self.book)
        contact = self.book.find("Test")
        self.assertEqual(contact.phones[0].value, "+381234567890")
        self.assertEqual(msg, "Contact updated.")

    def test_delete_contact(self):
        handler.delete_contact(["Test"], self.book)
        self.assertIsNone(self.book.find("Test", raise_error=False))

    def test_get_contact(self):
        contact = handler.get_contact(["Test"], self.book)
        self.assertEqual(contact.name.value, "Test")

    def test_get_all_contacts(self):
        contacts = handler.get_all_contacts(None, self.book)
        self.assertEqual(len(contacts), 1)

    def test_add_birthday(self):
        handler.add_birthday(["Test", "01.04.1990"], self.book)
        contact = handler.get_contact(["Test"], self.book)
        self.assertEqual(contact.birthday.value, datetime.datetime(1990, 4, 1))

    def test_show_birthday(self):
        handler.add_birthday(["Test", "01.04.1990"], self.book)
        birthday = handler.show_birthday(["Test"], self.book)
        self.assertEqual(birthday, "01.04.1990")

    def test_upcoming_birthdays(self):
        bday = datetime.datetime.today() + datetime.timedelta(days=4)
        handler.add_birthday(["Test", f"{bday.day:02}.{bday.month:02}.1990"], self.book)
        msg = handler.birthdays(None, self.book)
        self.assertIn("Test", msg)


if __name__ == "__main__":
    unittest.main()