# Contact_List.py

FILE_NAME = "contacts.txt"


def display_menu():
    print("\n--- Contact List Menu ---")
    print(f"(Using file: {FILE_NAME})")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Quit")


# Load contacts from file
def load_contacts():
    contact_list = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                name, phone, email = line.strip().split(",")
                contact_list.append({
                    "name": name,
                    "phone": phone,
                    "email": email
                })
    except FileNotFoundError:
        print(f"\nNo existing file found. A new '{FILE_NAME}' will be created.")
    return contact_list


# Save contacts to file
def save_contacts(contact_list):
    with open(FILE_NAME, "w") as file:
        for contact in contact_list:
            file.write(f"{contact['name']},{contact['phone']},{contact['email']}\n")


def add_contact(contact_list):
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")

    contact_list.append({
        "name": name,
        "phone": phone,
        "email": email
    })

    save_contacts(contact_list)
    print(f"\nSaved to {FILE_NAME}.")


def view_contacts(contact_list):
    if not contact_list:
        print("\nNo contacts found.")
        return

    print(f"\n--- Contacts from {FILE_NAME} ---")
    for contact in contact_list:
        print(f"{contact['name']} | {contact['phone']} | {contact['email']}")


def main():
    contact_list = load_contacts()

    while True:
        display_menu()
        choice = input("\nChoose (1-3): ")

        if choice == "1":
            add_contact(contact_list)
        elif choice == "2":
            view_contacts(contact_list)
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()