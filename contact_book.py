# READ.me file information
# Contact Book using JSON.
# Contact book functionality.


# After closing the program, the contacts will be retrievable, since they are stored in a JSON file.


import json     # Used to read and write contact information from and to the JSON file.
import os       # Handle file paths safely.


# Contact class
# Used for creating a single contact.
class Contact:
    def __init__(self, full_name, phone_number, email_address):
        self.full_name = full_name
        self.phone_number = phone_number
        self.email_address = email_address

    # Python objects, like the contact objects here, cannot directly be saved to a JSON file.
    # Dictionaries, however, can be saved to a JSON file.
    # This function essentially takes the contact object information and stores it in a dictionary.
    def convert_to_dict(self):
        return {                                    # Return a dictionary.
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "email_address": self.email_address
        }


# Contact Book class
# Used for loading an existing contact from the JSON file, saving contacts, adding new contacts, searching for contacts, displaying all contacts, and deleting contacts.
class ContactBook:
    def __init__(self, filename = "contacts.json"):     # File is automatically called 'contacts.json'.
        self.filename = filename        
        self.contacts = []     # A list that will hold all of the contacts loaded from the JSON file.
        # We initialize the class with a call to the load_contacts() function.
        # When the constructor is called, the load_contacts() function is called with it.
        self.load_contacts()    # The instance automatically calls the load_contacts() function. This ensures the retrieval of the modifications that we made during the last execution of our program.


    # Load contacts
    # Load contacts from the JSON file.
    # Converts the JSON file into something that our program here in Python can work with.
    # Contacts in JSON file -> Python list of contacts
    def load_contacts(self):
        if os.path.exists(self.filename):       # Check if the JSON file still exists. If we deleted it after the first execution, this will return False.
            # It exists.
            with open(self.filename, 'r') as file:   # Open (i.e. access) the JSON file in read mode.
                self.contacts = json.load(file)     # Read all contacts from the JSON file into the contact book's list for contacts.


    # Save contacts
    # This function will add the updated list of contacts to the JSON file.
    # This will ensure that even after we close the program, we'll be able to retrieve the contacts during the next execution of the program.
    def save_contacts(self):
        with open(self.filename, 'w') as the_json_file:     # 'w' means that the existing content will be overwritten.
            json.dump(self.contacts, the_json_file, indent=4)   # Takes all of the contacts in the 'contacts' list, and adds them to the JSON file. Add indentation for neatness.


    # Add contacts
    # Creates a Contact object.
    def add_contact(self, full_name, phone_number, email_address):
        new_contact = Contact(full_name, phone_number, email_address)
        self.contacts.append(new_contact.convert_to_dict())       # Append the new contact to the contact list, but be sure to append it in dictionary form by calling the convert_to_dict() method.
        self.save_contacts()     # Update the list of contacts to include the newly added one.
        print("\nContact added successfully.\n\n")


    # Search contacts
    # Search for a specific contact using a keyword.
    def search_contacts(self, keyword):
        keyword = keyword.lower()
        results = []    # All matching results will be appended to this list
        
        for each_contact in self.contacts:
            if (keyword in each_contact["full_name"].lower() or
                keyword in each_contact["phone_number"].lower() or
                keyword in each_contact["email_address"].lower()):
                results.append(each_contact)
        
        return results 


    # Displays all contacts that have been saved in the system.
    def display_all(self):
        # Check if list is empty.
        if not self.contacts:
            print("\nContact list is empty, brother.\n")
            return      # Stop the function.
        print(f"\n######## ALL CONTACTS ########\n")
        for i, each_contact in enumerate(self.contacts, start=1):   # Start the list from 1.    # "1.", "2.", ...
            print(f"{i}. {each_contact["full_name"]}    |    {each_contact["phone_number"]}    |    {each_contact["email_address"]}")
        print()

    
    # Delete contacts
    def delete_contact(self, exact_name):
        # Record how many contacts we had before deletion
        original_count = len(self.contacts)     
        
        # Only keep contacts that don't match
        self.contacts = [
            each_contact for each_contact in self.contacts
            if each_contact["full_name"].lower() != exact_name
        ]

        # Save the updated list to the JSON file.
        self.save_contacts()

        # Confirmation
        if len(self.contacts) < original_count:
            print(f"\nContact deleted successfully.\n")
        else:
            print(f"{exact_name} is not in your contacts.")


def main():
    # Initialize the contact book.
    contact_book = ContactBook()
    # load_contacts() is called. This retrieves the modifications that we made in the last execution of our program.

    user_name = input("\nWhat is your first name?\n> ").upper()

    # Main menu display 
    while True: 
        print(f"\n######## {user_name}'S CONTACTS ########\n")
        print("Enter '1' to add a contact.")
        print("Enter '2' to search for a contact.")
        print("Enter '3' to display all of your contacts.")
        print("Enter '4' to delete a contact.")
        print("Enter 'Q' to quit.")


        # User chooses an option
        user_choice = input("\n> ")


        # User wants to add a contact.
        if user_choice == "1":
            # Ask user for information.
            full_name = input("\nFull Name: ")
            phone_number = input("Phone Number: ")
            email_address = input("Email Address:")
            print()
            contact_book.add_contact(full_name, phone_number, email_address)

        # User wants to search for a specific contact.
        elif user_choice == "2":
            # Ask user for a keyword.
            results = contact_book.search_contacts(input("\nEnter a search keyword:\n> "))
            
            if results:     # If the contact book is not empty.
                print(f"\n{len(results)} contact{"s" if len(results) > 1 else ""} found:\n")
                for i, each_contact in enumerate(results, start=1):
                    print(f"{i}. {each_contact["full_name"]}    |    {each_contact["phone_number"]}    |    {each_contact["email_address"]}")
            else:
                print("No match found.")

        # User wants to display all of their contacts.
        elif user_choice == "3":
            contact_book.display_all()

        # User wants to delete a contact.
        elif user_choice == "4":
            # Ask user for the name of the contact.
            name_to_delete = input("Enter the name of the contact that you'd like to delete:\n> ")
            contact_book.delete_contact(name_to_delete.lower())
        
        # User wants to quit.
        elif user_choice == "5":
            print(f"\nTake care, {user_name}!")
            print("Your contacts will be here when you come back.\n")
            break


if __name__ == "__main__":
    main()