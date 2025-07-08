import pytest

from src.address_book import AddressBook, Record

def test_add_phone_new_number():
    record = Record("Alice")
    record.add_phone("123")
    assert any(p.value == "123" for p in record.phones)


def test_add_phone_duplicate_raises():
    record = Record("Bob")
    record.add_phone("555")
    with pytest.raises(ValueError):
        record.add_phone("555")


def test_edit_phone_changes_number():
    record = Record("Carol")
    record.add_phone("111")
    record.edit_phone("111", "222")
    assert record.phones[0].value == "222"


def test_edit_phone_nonexistent_no_change():
    record = Record("Dave")
    record.add_phone("333")
    record.edit_phone("999", "000")
    assert [p.value for p in record.phones] == ["333"]


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
