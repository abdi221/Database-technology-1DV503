import time
from getpass import getpass
from database import Database
import mysql.connector
cursor = mysql.connector
db = Database()
logged_user_id = None

def pretty_print(content: str,content2 = None, line_len: int = 45) -> None:
        print(f"{'*' * line_len}")
        print(f"{'***' + ' ' * (line_len - 6) + '***'}")
        print(f"{'***' + ' ' * ((line_len - len(content) - 6) // 2) + content + ' ' * ((line_len - len(content) - 6) // 2) + ' ***'}")
        print(f"{'***' + ' ' * ((line_len - len(content2) - 6) // 2) + content2 + ' ' * ((line_len - len(content2) - 6) // 2) + ' ***'}") if content2 else None
        print(f"{'***' + ' ' * (line_len - 6) + '***'}")
        print(f"{'*' * line_len}")

def menu():
    pretty_print("Welcome to Online bookstore!")

    while True:
        print(("\t" * 4) + "1. Member Login") 
        print(("\t" * 4) + "2. Member Registration")
        print(("\t" * 4) + "3. exit" + '\n' *2)
        ch = int(input("Type in your option: "))
        # Login
        if ch == 1:
            email = input("Email: ")
            password = input("Password: ")

            # Check if the user exists and the password is correct
            db.mycursor.execute("SELECT * FROM members WHERE email = %s AND password = %s",
                                (email, password))
            user_exists = db.mycursor.fetchone()

            if user_exists:
                print("\nSuccessfully logged in!")
                global logged_user_id
                logged_user_id = user_exists[7]
                time.sleep(2)
                main_menu()
            else:
                print("Couldn't find the email or the password is incorrect. Register")
                time.sleep(2)
                menu()



        elif ch == 2:
            pretty_print("Weclome to the Online Book Store", "New Member Registration")
            fname = input("First name: ")
            lname = input("Lastname: ")
            address = input("Adress: ")
            city = input("City: ")
            zip = input("Zip: ")
            pnumber = input("Phone Number: ")
            email = input("Email Adress: ")
            pw = getpass("Password: ")

            if '@' not in email:
                print("Invalid email adress. Please use @ in the email when registering it")
                menu()
            else:
                db.mycursor.execute("INSERT INTO members(fname, lname, address, city, zip, phone, email, password) \
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                    (fname, lname, address, city, zip, pnumber, email, pw))
                db.conn.commit()
                response = input("You have registered successfully! \n Press ENTER to go back to Menu!: ")
                if response == "":
                    menu()
                else:
                    break
                    
        elif ch == 3:
            db.close_connection()
            break

def main_menu():
    pretty_print("Welcome to the Online Book Store", "Member Menu")
    print(("\t" * 4) + "1. Browse by Subject")
    print(("\t" * 4) + "2. Search By Author/Title")
    print(("\t" * 4) + "3. Check Out")
    print(("\t" * 4) + "4. Logout" + '\n' * 2)
    ch = int(input("Type in your option: "))

    if ch == 1:
        browse_by_subject()
    if ch == 2:
        search_by_author_title()
    if ch == 3:
        checkout()
    if ch == 4:
        global logged_user_id
        logged_user_id = None
        menu()

def browse_by_subject():
    page = 1

    db.mycursor.execute("SELECT * FROM books")
    books = db.mycursor.fetchall()

    subjects = set(book[4] for book in books)
    print("Subjects: \n")

    for number, subject in enumerate(subjects, 1):
        print(f"\t{number}. {subject}")

    chosen_subject_index = input("Enter your choice: ")
    if chosen_subject_index == "":
        browse_by_subject()
    else:
        chosen_subject_index = int(chosen_subject_index) - 1
    chosen_subject = list(subjects)[chosen_subject_index]

    while True:
        display_books_by_subject(db, chosen_subject, page)

        chosen_option = input("Enter ISBN to add to Cart, 'n' to see next page, or ENTER to go back to menu: \n")

        if len(chosen_option) == 10:
            add_book_to_cart(chosen_option)
        elif chosen_option.lower() == 'n':
            page += 1
        elif chosen_option == '':
            main_menu()
        else:
            browse_by_subject()

def display_books_by_subject(db, subject, page):
    db.mycursor.execute("SELECT * FROM books WHERE subject = %s LIMIT 2 OFFSET %s", (subject, (page - 1) * 2))
    books = db.mycursor.fetchall()
    db.mycursor.execute("SELECT * FROM books WHERE subject = %s", (subject,))
    all_books = db.mycursor.fetchall()

    print(f"\n{len(all_books)} books available for this Subject (Page {page})\n")
    for book in books:
        print(f"Author: {book[1]}")
        print(f"Title: {book[2]}")
        print(f"ISBN: {book[0]}")
        print(f"Price: {book[3]}")
        print(f"Subject: {book[4]}\n")

def add_book_to_cart(isbn):
    db.mycursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
    selected_book = db.mycursor.fetchall()

    if not selected_book:
        print("No books available for this ISBN\n")
    else:
        quantity = int(input("Enter quantity: "))
        userid = get_userid()  # Assuming you have a function to get the current user's ID
        db.mycursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)", (userid, isbn, quantity))
        db.commit()
        print("Book added to cart")
        time.sleep(2)

def get_userid():
    global logged_user_id
    return logged_user_id if logged_user_id else menu()

def search_by_author_title():
    while True:
        pretty_print("Search by Author/Title")
        print("\t1. Author Search")
        print("\t2. Title Search")
        print("\t3. Go Back to Main Menu\n")

        option = int(input("Enter your option: "))

        if option == 1:
            author_search()
        elif option == 2:
            title_search()
        elif option == 3:
            main_menu()
            break
        else:
            print("Invalid option. Please choose again.")

def author_search():

    while True:
        search_term = input("Enter a substring of the author's name (or press Enter to go back to the previous menu): ").strip()

        if search_term == "":
            search_by_author_title()
            break

        db.mycursor.execute("SELECT * FROM books WHERE author LIKE %s LIMIT 3", (f"%{search_term}%",))
        books = db.mycursor.fetchall()

        if not books:
            print("No books found for the given author.")
            author_search()
        else:
            display_books(books)

        chosen_option = input("\nEnter ISBN to add to Cart, 'n' to see next page, or ENTER to go back to previous menu: ").strip().lower()
        handle_option(chosen_option)

def title_search():

    while True:
        search_term = input("Enter title or part of the title (or press Enter to go back to the previous menu): ").strip()

        if search_term == "":
            search_by_author_title()
            break

        db.mycursor.execute("SELECT * FROM books WHERE title LIKE %s LIMIT 3", (f"%{search_term}%",))
        books = db.mycursor.fetchall()

        if not books:
            print("No books found for the given title.")
            title_search()
        else:
            display_books(books)

        chosen_option = input("\nEnter ISBN to add to Cart, 'n' to see next page, or ENTER to go back to previous menu: ").strip().lower()
        handle_option(chosen_option)

def display_books(books):
    print("\nBooks:")
    for book in books:
        print(f"Title: {book[2]}\n Author: {book[1]}\n ISBN: {book[0]}\n Price: {book[3]}\n Subject: {book[4]}\n")

def handle_option(chosen_option):
    if len(chosen_option) == 10:
        add_book_to_cart(chosen_option)
    elif chosen_option == "":
        search_by_author_title()
    elif chosen_option == "n":
        continue_browsing()
    else:
        print("Invalid option. Please try again.")

def continue_browsing():
    print("Continuing browsing...\n")


from datetime import datetime, timedelta


def checkout():
    pretty_print("Check Out")

    # Display invoice
    display_invoice()



def display_invoice():
    user_id = get_userid()  # Function to get the current user's ID

    # Display invoice header
    print("Curent Cart Contents:\n")
    # Fetch cart items for the user
    db.mycursor.execute("SELECT isbn, qty FROM cart WHERE userid = %s", (user_id,))
    cart_items = db.mycursor.fetchall()
    if len(cart_items) == 0:
        print("No cart items available for this user.\n")
        time.sleep(2)
        main_menu()

    total_price = 0
    rows = list()
    for item in cart_items:
        isbn, quantity = item
        db.mycursor.execute("SELECT title, price FROM books WHERE isbn = %s", (isbn,))
        book = db.mycursor.fetchone()

        if book:
            title, price = book
            item_total = price * quantity
            total_price += item_total
            rows.append([isbn, title, price, quantity, round(item_total, 2)])
        else:
            print(f"Book with ISBN {isbn} not found.")

    print_table(rows, total_price)
    choice = input("Proceed to check out (Y/N)?: ").strip().lower()

    if choice == 'y':
        save_order(user_id, cart_items)
    elif choice == 'n':
        main_menu()
    else:
        print("Invalid choice. Please enter 'Y' to proceed or 'N' to go back to the main menu.")
        display_invoice()


def save_order(user_id, cart_items):
    user = get_user_data(user_id)

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Generate shipment date (one week ahead)
    shipment_date = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")

    shipping_address, city, zip = get_shipping_data(user_id)
    # Insert into Order table
    db.mycursor.execute(
        "INSERT INTO orders (userid, created, shipAddress, shipCity, shipZip) VALUES (%s, %s, %s, %s, %s)",
        (user_id, current_date, shipping_address, city, zip))
    order_id = db.mycursor.lastrowid
    total_price = 0
    # Insert into Odetails table
    for item in cart_items:
        isbn, quantity = item
        amount = quantity * get_book_price_by_isbn(isbn)
        db.mycursor.execute("INSERT INTO odetails (ono, isbn, qty, amount) VALUES (%s, %s, %s, %s)",
                            (order_id, isbn, quantity, amount))

    # Commit changes
    db.commit()

    print("Order successfully saved.\n")

    clear_cart(user_id)

    print(f"Invoice fo Order no.{order_id}\n")
    print("Shipping Address")
    print(f"Name: {user[0]} {user[1]}")
    print(f"Adress: {user[2]}\n{user[3]}\n{user[4]}")
    print(f"Estimated delivery date: f{shipment_date}")
    print('-' * 45)
    rows = list()
    for item in cart_items:
        isbn, quantity = item
        amount = quantity * get_book_price_by_isbn(isbn)
        total_price += amount
        rows.append([isbn, get_book_title_by_isbn(isbn), get_book_price_by_isbn(isbn), quantity, round(amount, 2)])
    print_table(rows, total_price)

    time.sleep(5)

    main_menu()



def get_shipping_data(user_id):
    db.mycursor.execute("SELECT address, city, zip FROM members WHERE userid = %s", (user_id,))
    members = db.mycursor.fetchone()
    address, city, zip = members
    return address, city, zip

def get_book_price_by_isbn(isbn):
    db.mycursor.execute("SELECT price FROM books WHERE isbn = %s", (isbn,))
    price = db.mycursor.fetchone()
    if not price:
        print("there is not price")
        return None
    else:
        return price[0]

def get_book_title_by_isbn(isbn):
    db.mycursor.execute("SELECT title FROM books WHERE isbn = %s", (isbn,))
    title = db.mycursor.fetchone()
    if not title:
        print("there is not title")
        return None
    else:
        return title[0]

def clear_cart(user_id):
    db.mycursor.execute("DELETE FROM cart WHERE userid = %s", (user_id,))
    db.commit()
    print("Cart has been cleared.\n")

def get_user_data(user_id):
    db.mycursor.execute("SELECT * FROM members WHERE userid = %s", (user_id,))
    member = db.mycursor.fetchone()
    return member


def print_table(rows, total):
    headers = ["ISBN", "Title", "$", "Qty", "Total"]
    footers = ["Total", "", "", "", total]
    # Determine the width of each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*rows, headers)]

    # Print the headers
    header_line = " ".join(f"{header:{col_widths[i]}}" for i, header in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    # Print each row
    for row in rows:
        print(" ".join(f"{str(item):{col_widths[i]}}" for i, item in enumerate(row)))

    print("-" * len(header_line))

    footer_line = " ".join(f"{footer:{col_widths[i]}}" for i, footer in enumerate(footers))
    print(footer_line)

    print("-" * len(header_line))





def main():
    while True:
        try:
            # username = input("Enter SQL Server username: ")
            # password = getpass("Enter SQL Server Password: ")
            db = Database()
            print("Database object created successfully.")
            break  # Break the loop if connection is successful
        except Exception as e:
            print("Connection failed, check credentials and try again.", e)
    try:
        menu()
    #   main_menu()
    finally:
        db.close_connection()

if __name__ == "__main__":
    # main_menu()
    menu()

