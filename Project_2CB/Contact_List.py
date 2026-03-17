import json

FILE_NAME = "contacts.json"


# Load contacts from JSON file - Def defines the funciton and the function below is opening the additional json file to read the contacts
def load_contacts():
    try:
        with open(FILE_NAME) as file:
            return json.load(file)
    except:
        return []


# Save contacts to JSON file - def defines the function; this will open the the json list and add the data and go back in to read the data - "w" is not needed but pulls the information 
def save_contacts(contact_list):
    with open(FILE_NAME, "w") as file:
        json.dump(contact_list, file, indent=4)


# Check name (letters only) - def defines the function - is alpha constrains the answerable data to letters only
def valid_name(name):
    return name.isalpha() #spaces will not be accepted with function as is - problem for another day


# Check phone (numbers only) - def defines the funciton, isdigit is the contraint for the acceptable data for this menu choice, numbers only
def valid_phone(phone):
    return phone.isdigit()


# Add a contact - def defines the newly added function; this function is fun because it leaves to the json, adds the data and comes back to this file with the information (reads the data from json)
def add_contact(contact_list):
    name = input("Enter name: ")
    if not valid_name(name):
        print("Name must contain only letters.")
        return

    phone = input("Enter phone: ")
    if not valid_phone(phone):
        print("Phone must contain only numbers.")
        return

    email = input("Enter email: ")

    contact_list.append({
        "name": name,
        "phone": phone,
        "email": email
    })

    save_contacts(contact_list)
    print("Contact saved.")


# View all contacts - def is defining the action - if allows both the ability to use the funtion if they follow through on the action and if the funciton cannot be completed considereing lack of constraints or information (not listed)
def view_contacts(contact_list):
    if not contact_list:
        print("No contacts found.")
        return

    print("\nContacts:")
    for c in contact_list:
        print(c["name"], "|", c["phone"], "|", c["email"])


# Search for a contact - def defines the funcion, and the if allows the action and prints an error if no name is found
def search_contact(contact_list):
    name = input("Search name: ")

    for c in contact_list:
        if name.lower() in c["name"].lower():
            print(c["name"], "|", c["phone"], "|", c["email"])
            return

    print("Not found.")


# Delete a contact - def is defining the action and delete and remove pull the item from the list - if prints errors if the name is not on the list already
def delete_contact(contact_list):
    name = input("Delete name: ")

    for c in contact_list:
        if c["name"].lower() == name.lower():
            contact_list.remove(c)
            save_contacts(contact_list)
            print("Deleted.")
            return

    print("Not found.")


# Menu display - Printed Menu, Here to look pretty, jk, but simply printed text
def menu():
    print("\n--- Contact List Menu ---")
    print("1. Add")
    print("2. View")
    print("3. Search")
    print("4. Delete")
    print("5. Quit")


# Main program - Functional Menu - If/Elif allows the choice of the listed options
def main():
    contacts = load_contacts()

    while True:
        menu()
        choice = input("Choose: ")

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


main()