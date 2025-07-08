#AI-generated

import pytest
from datetime import date, timedelta

from src.address_book import AddressBook, Record

def test_add_phone_new_number():
    record = Record("Alice")
    record.add_phone("1234567890")
    assert any(p.value == "1234567890" for p in record.phones)


def test_add_phone_duplicate_raises():
    record = Record("Bob")
    record.add_phone("5555555555")
    with pytest.raises(ValueError):
        record.add_phone("5555555555")


def test_edit_phone_changes_number():
    record = Record("Carol")
    record.add_phone("1111111111")
    record.edit_phone("1111111111", "2222222222")
    assert record.phones[0].value == "2222222222"


def test_edit_phone_nonexistent_no_change():
    record = Record("Dave")
    record.add_phone("3333333333")
    with pytest.raises(ValueError):
        record.edit_phone("9999999999", "0000000000")
    assert [p.value for p in record.phones] == ["3333333333"]


def test_address_book_add_record():
    book = AddressBook()
    record = Record("Eve")
    book.add_record(record)
    assert book.data["Eve"] is record


def test_address_book_add_record_duplicate_raises():
    book = AddressBook()
    record1 = Record("Frank")
    record2 = Record("Frank")
    book.add_record(record1)
    with pytest.raises(KeyError):
        book.add_record(record2)


def test_add_valid_birthday():
    record = Record("Grace")
    record.add_birthday("01.01.2000")
    assert record.birthday.value.strftime("%d.%m.%Y") == "01.01.2000"


def test_add_invalid_birthday_format():
    record = Record("Henry")
    with pytest.raises(ValueError):
        record.add_birthday("01/01/2000")


def test_add_future_birthday():
    record = Record("Ivy")
    future_date = (date.today().replace(year=date.today().year + 1)).strftime("%d.%m.%Y")
    with pytest.raises(ValueError):
        record.add_birthday(future_date)


def test_get_upcoming_birthdays():
    book = AddressBook()

    today = date.today()

    record1 = Record("Alice")
    birthday1 = (today + timedelta(days=3)).replace(year=today.year - 25)
    record1.add_birthday(birthday1.strftime("%d.%m.%Y"))
    book.add_record(record1)

    record2 = Record("Bob")
    birthday2 = (today + timedelta(days=10)).replace(year=today.year - 30)
    record2.add_birthday(birthday2.strftime("%d.%m.%Y"))
    book.add_record(record2)

    record3 = Record("Charlie")
    birthday3 = (today - timedelta(days=1)).replace(year=today.year - 40)
    record3.add_birthday(birthday3.strftime("%d.%m.%Y"))
    book.add_record(record3)

    record4 = Record("David")
    birthday4 = today.replace(year=today.year - 35)
    record4.add_birthday(birthday4.strftime("%d.%m.%Y"))
    book.add_record(record4)

    record5 = Record("Eve")
    book.add_record(record5)

    upcoming_birthdays = book.get_upcoming_birthdays()

    assert len(upcoming_birthdays) == 2

    names = [entry["name"] for entry in upcoming_birthdays]
    assert "Alice" in names
    assert "David" in names
    assert "Bob" not in names
    assert "Charlie" not in names
    assert "Eve" not in names

    for entry in upcoming_birthdays:
        assert "congratulation_date" in entry
        date_str = entry["congratulation_date"]
        assert len(date_str) == 10, f"Invalid date length: {date_str}"
        assert date_str[2] == "." and date_str[5] == ".", f"Invalid date format: {date_str}"
        day, month, year = date_str.split(".")
        assert len(day) == 2, f"Invalid day format: {day}"
        assert len(month) == 2, f"Invalid month format: {month}"
        assert len(year) == 4, f"Invalid year format: {year}"
        assert day.isdigit(), f"Day is not a number: {day}"
        assert month.isdigit(), f"Month is not a number: {month}"
        assert year.isdigit(), f"Year is not a number: {year}"
