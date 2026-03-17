# Contact_List.py

FILE_NAME = "contacts.txt" #Pulling from a separate list (text file) - Change to JSON


def display_menu(): #Displaying the functional menus by ennumerating; written out 
    print("\n--- Contact List Menu ---")
    print(f"(Using file: {FILE_NAME})")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Quit")


# Load contacts from file
def load_contacts(): #Defining the list and "machine" to add and remove contacts
    contact_list = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                name, phone, email = line.strip().split(",")
                contact_list.append({ #Append is adding each as it is listed 
                    "name": name,
                    "phone": phone,
                    "email": email
                })
    except FileNotFoundError:
        print(f"\nNo existing file found. A new '{FILE_NAME}' will be created.")
    return contact_list


# Save contacts to file
def save_contacts(contact_list): #saving the to txt list, is viewable in txt file
    with open(FILE_NAME, "w") as file:
        for contact in contact_list:
            file.write(f"{contact['name']},{contact['phone']},{contact['email']}\n")


def add_contact(contact_list): #display list to show added items
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


def view_contacts(contact_list): #defining the print for when there are no items
    if not contact_list:
        print("\nNo contacts found.")
        return

    print(f"\n--- Contacts from {FILE_NAME} ---")
    for contact in contact_list:
        print(f"{contact['name']} | {contact['phone']} | {contact['email']}")


def main(): #defining the following actions when using the menu based on the defined actions above
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


if __name__ == "__main__": #closing code
    main()