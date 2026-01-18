import csv
import maskpass
import os
from datetime import datetime

# ------------------------------
# Authentication Class
# ------------------------------
class Authentication:
    def __init__(self, email="", username="", password=""):
        self.email = email
        self.username = username
        self.password = password

    def valid_email(self, email):
        return '@' in email and '.' in email

    def register(self):
        email = input("Enter email: ").strip()
        while not self.valid_email(email):
            print("Invalid email! Please enter a valid email.")
            email = input("Enter email: ").strip()
        
        username = input("Enter full name: ").strip()
        password = maskpass.advpass("Enter password: ").strip()
        confirm_password = maskpass.advpass("Confirm password: ").strip()

        if confirm_password == password:
            with open('user.csv', 'a', newline='') as w:
                writer = csv.writer(w)
                writer.writerow([email, username, password])
            print("Registration successful!")
            return True
        else:
            print("Passwords do not match. Try again.")
            return False

    def login(self):
        email = input("Enter email: ").strip()
        while not self.valid_email(email):
            print("Invalid email! Please enter a valid email.")
            email = input("Enter email: ").strip()

        password = maskpass.advpass("Enter password: ").strip()

        with open('user.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 3:
                    continue
                stored_email, stored_username, stored_password = row
                if email == stored_email and password == stored_password:
                    print("Login successful!")
                    self.username = stored_username
                    return True
        print("Login failed!")
        return False

# ------------------------------
# View Ticket Categories
# ------------------------------
class ViewCategory:
    def __init__(self, filename):
        self.filename = filename

    def show_categories(self):
        seen = []
        count = 1
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                category = row[1]
                if category not in seen:
                    print(f"{count}. {category}")
                    seen.append(category)
                    count += 1
        return seen

    def get_category_by_number(self, chosen_number):
        categories = self.show_categories()
        try:
            return categories[int(chosen_number)-1]
        except (ValueError, IndexError):
            print("Invalid category number.")
            return None

# ------------------------------
# View Tickets (Top-ups) under a Category
# ------------------------------
class ViewTickets:
    def __init__(self, filename):
        self.filename = filename

    def show_tickets(self, selected_category):
        seen = set()
        tickets_list = []
        count = 1
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[1] == selected_category:   # category column
                    ticket = row[4]               # ticket/top-up column
                    if ticket not in seen:
                        print(f"{count}. {ticket}")
                        seen.add(ticket)
                        tickets_list.append(row)
                        count += 1
        return tickets_list

# ------------------------------
# Purchase Menu Class
# ------------------------------
class ticket_purchase:
    def __init__(self, filename="mobile_products.csv"):
        self.filename = filename

    # Show details of selected ticket and allow purchase
    def purchase_ticket(self, selected_category, ticket_number):
        tickets_list = []

        # Read tickets under the selected category
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if row[1] == selected_category:
                    tickets_list.append(row)

        try:
            chosen_index = int(ticket_number) - 1
        except ValueError:
            print("Invalid number.\n")
            return

        if chosen_index < 0 or chosen_index >= len(tickets_list):
            print("Invalid option. Please try again.\n")
            return

        selected_ticket = tickets_list[chosen_index]
        ticket_name = selected_ticket[4]     # top-up/ticket column
        description = selected_ticket[5]     # description column
        price_pence = selected_ticket[6]     # price column

        # Show ticket details
        print("\n---------------------------------------------")
        print(f" Ticket Name : {ticket_name}")
        print(f" Description : {description}")
        print(f" Price       : {price_pence} pence")
        print("---------------------------------------------\n")

        # Ask if user wants to purchase
        choice = input("Do you want to purchase this ticket? (y/n): ").lower()
        if choice == "y":
            self.save_purchase(selected_category, ticket_name, description, price_pence)
        else:
            print("Returning to menu...\n")

    # Save purchase record
    def save_purchase(self, category, ticket_name, description, price_pence):
        filename = "purchase_records.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                # Write header if file does not exist
                writer.writerow(["Category", "Ticket Name", "Description", "Price (pence)", "Date & Time", "Status"])
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([category, ticket_name, description, price_pence, timestamp, "Completed"])

        print("\n✔ Purchase completed successfully!\n")

# ------------------------------
# Customer Menu
# ------------------------------
class CustomerMenu:
    def __init__(self, filename="mobile_products.csv"):
        self.filename = filename
        self.view_category = ViewCategory(filename)
        self.view_tickets = ViewTickets(filename)
        self.purchase = ticket_purchase(filename)

    def display_menu(self):
        while True:
            choice = input(""" 
1.) View ticket categories
2.) Return to main menu
Enter your option: """)

            if choice == "1":
                categories = self.view_category.show_categories()
                chosen_number = input("\nEnter the ticket category number: ")
                selected_category = self.view_category.get_category_by_number(chosen_number)
                if selected_category:
                    print(f"\nTickets under '{selected_category}':\n")
                    tickets_list = self.view_tickets.show_tickets(selected_category)

                    if tickets_list:
                        ticket_num = input("\nEnter the ticket number to view/purchase: ")
                        self.purchase.purchase_ticket(selected_category, ticket_num)

            elif choice == "2":
                break
            else:
                print("Invalid option. Try again.")

# ------------------------------
# Help / About Class
# ------------------------------
class HelpAbout:
    def show_about(self):
        print("""
---------------------------------------------
            ABOUT NCTX BUS APPLICATION
---------------------------------------------
NCTX Bus Application is a console-based system
designed to help users view and purchase bus
tickets easily.

Features:
- User registration and login
- View bus ticket categories
- View available tickets
- Purchase tickets securely
- View purchase history (Admin)
- Simple and user-friendly interface

Developed using:
- Python
- CSV file handling
- Object-Oriented Programming (OOP)

Version: 1.0
---------------------------------------------
""")

    def show_help(self):
        print("""
---------------------------------------------
                HELP SECTION
---------------------------------------------
1. Login:
   - Use your registered email and password
   - If you are new, select Signup first

2. Signup:
   - Enter a valid email address
   - Passwords must match

3. Customer Menu:
   - View ticket categories
   - Select and purchase tickets

4. Admin Menu:
   - View registered users
   - View tickets and purchases

5. Logout:
   - Safely exit your session

If you face issues:
- Ensure required CSV files exist
- Enter valid menu options
---------------------------------------------
""")

    def display(self):
        while True:
            choice = input("""
--- Help / About Menu ---
1.) About Application
2.) How to Use (Help)
3.) Back
Enter your option: """)

            if choice == "1":
                self.show_about()
            elif choice == "2":
                self.show_help()
            elif choice == "3":
                break
            else:
                print("Invalid option. Try again.")


# ------------------------------
# Main Menu
# ------------------------------
def main_menu(logged_in):
    while logged_in:
        user_input = input(""" 
1.) Customer Menu 
2.) Help/About
3.) Logout
Enter the option: """)

        if user_input == "1":
            customer = CustomerMenu()
            customer.display_menu()
        elif user_input == "2":
            help_about = HelpAbout()
            help_about.display()
        elif user_input == "3":
            print("Logged out successfully!")
            logged_in = False
        else:
            print("Invalid option")

    while logged_in:
        user_input = input(""" 
2.) Customer Menu 
3.) Help/About
4.) Logout
Enter the option: """)

        if user_input == "1":
            print("Admin Menu (coming soon)")
        elif user_input == "2":
            customer = CustomerMenu()
            customer.display_menu()
        elif user_input == "3":
            print("Help/About Section")
        elif user_input == "4":
            print("Logged out successfully!")
            logged_in = False
        else:
            print("Invalid option")

# ------------------------------
# Home / Entry
# ------------------------------
def Home():
    print("""
---------------------------------------------
            NCTX BUS APPLICATION 
---------------------------------------------
""")
    auth_input = input(""" 
1. Login
2. Signup
3. Exit   
Enter Your Option: """ )
    auth = Authentication()
    if auth_input == "1":
        logged_in = auth.login()
        if logged_in:
            main_menu(logged_in)
    elif auth_input == "2":
        logged_in = auth.register()
        if logged_in:
            main_menu(logged_in)
    elif auth_input == "3":
        print("Thanks for using the app")
    else:
        print("Invalid option")

Home()
