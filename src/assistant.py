from address_book import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please provide both name and phone number, e.g.: add John 123456789"
        except KeyError:
            return "Contact not found. Please check the name and try again"
        except IndexError:
            return "Not enough arguments provided. Please follow the command format"
    return inner

@input_error
def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        raise ValueError
    cmd, *args = parts
    return cmd.lower(), args

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return f"{name}: {'; '.join(p.value for p in record.phones)}"

@input_error
def show_all(args, book):
    if args:
        raise ValueError
    if not book.data:
        return "No contacts saved."
    return "\n".join([str(record) for record in book.data.values()])

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return f"{name} has no birthday set."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book):
    if args:
        raise ValueError
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No birthdays in the upcoming week."
    result = []
    for birthday in upcoming_birthdays:
        result.append(f"{birthday['name']}: {birthday['congratulation_date']}")
    return "Upcoming birthdays:\n" + "\n".join(result)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")

        if user_input.lower().strip() in ("exit", "close"):
            print("Good bye!")
            break

        parsed = parse_input(user_input)
        if isinstance(parsed, str):
            print(parsed)
            continue

        command, args = parsed

        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(args, book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(args, book))
            case _:
                print("Invalid command. Available: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, exit/close")

if __name__ == "__main__":
    main()
