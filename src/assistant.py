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
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args, contacts):
    name = args[0]
    return f"{name}: {contacts[name]}"

@input_error
def show_all(args, contacts):
    if args:
        raise ValueError
    if not contacts:
        return "No contacts saved."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    contacts = {}
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
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(args, contacts))
            case _:
                print("Invalid command. Available: hello, add, change, phone, all, exit/close")

if __name__ == "__main__":
    main()
