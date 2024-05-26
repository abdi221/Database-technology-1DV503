from getpass import getpass
import time
from datetime import datetime, timedelta
# from mysql.connector import cursor
# import mysql.connector
from database import Database

# Global variable for logged in user ID
logged_user_id = None

# Initialize database connection
db = Database()


def pretty_print(content: str, content2: str = None, line_len: int = 45) -> None:
    """Prints formatted messages with a border."""
    print(f"{'*' * line_len}")
    print(f"{'***' + ' ' * (line_len - 6) + '***'}")
    print(
        f"{'***' + ' ' * ((line_len - len(content) - 6) // 2) + content + ' ' * ((line_len - len(content) - 6) // 2) + ' ***'}")
    if content2:
        print(
            f"{'***' + ' ' * ((line_len - len(content2) - 6) // 2) + content2 + ' ' * ((line_len - len(content2) - 6) // 2) + ' ***'}")
    print(f"{'***' + ' ' * (line_len - 6) + '***'}")
    print(f"{'*' * line_len}")


def menu():
    """Displays the main menu and handles user choices."""

    while True:
        pretty_print("Welcome to Online Bookstore!")

        print("\t" * 2 + "1. Member Login")
        print("\t" * 2 + "2. Member Registration")
        print("\t" * 2 + "q. Quit\n")
        ch = input("Type in your option: ")

        if ch == "1":
            login()
        elif ch == "2":
            register()
        elif ch == "q":
            db.close_connection()
            break


def login():
    """Handles member login."""
    global logged_user_id
    email = input("Email: ")
    password = getpass("Password: ")

    db.mycursor.execute("SELECT * FROM members WHERE email = %s AND password = %s", (email, password))
    user = db.mycursor.fetchone()

    if user:
        print("\nSuccessfully logged in!")
        logged_user_id = user[7]
        time.sleep(2)
        main_menu()
    else:
        print("Invalid email or password. Going back to Main Menu.")
        time.sleep(2)


def register():
    # Handles member registration
    pretty_print("Welcome to the Online Book Store\n" \
                      '\t'+"New Member Registration")
    fname = input("First name: ")
    lname = input("Lastname: ")
    address = input("Address: ")
    city = input("City: ")
    zip = input("Zip: ")
    pnumber = input("Phone Number: ")
    email = input("Email Address: ")
    pw = input("Password: ")

    if not all([fname, lname, address, city, zip, pnumber, email, pw]):
        print("All fields are required. Please fill in all the details.")
        time.sleep(2)
        menu()

    if '@' not in email:
        print("Invalid email address. Please include '@' in the email.")
        time.sleep(2)
        menu()
    else:
        db.mycursor.execute("INSERT INTO members(fname, lname, address, city, zip, phone, email, password) \
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (fname, lname, address, city, zip, pnumber, email, pw))
        db.conn.commit()
        print("You have registered successfully!")
        enter = input("Press ENTER to go back to Menu.")
        if enter == '':
            menu()
 
def main_menu():
    """Displays the main menu for logged in members and handles user choices."""
    while True:
        pretty_print("Welcome to the Online Book Store","Member Menu")
        print("\t     " + "1. Browse by Subject")
        print("\t     " + "2. Search By Author/Title")
        print("\t     " + "3. Check Out")
        print("\t     " + "4. Logout")
        print("\t     " + "5. Quit\n")
        try:
            ch = int(input("Type in your option: "))
        except ValueError:
            print("Invalid input. Please enter number between 1 and 5.")
            continue
        if ch == 1:
            browse_by_subject()
        elif ch == 2:
            search_by_author_title()
        elif ch == 3:
            checkout()
        elif ch == 4:
            print("Logging Out!")
            global logged_user_id
            logged_user_id = None
            menu()
        elif ch == 5:
            db.close_connection()
            break
        # else:
        #     print("Invalid input, go back to menu by pressing enter key")
        #     if 


def browse_by_subject():
    """Allows browsing books by subject."""
    page = 1
    db.mycursor.execute("SELECT DISTINCT subject FROM books")
    subjects = db.mycursor.fetchall()

    if subjects:
        print("Subjects:\n")
        for number, subject in enumerate(subjects, 1):
            print(f"\t{number}. {subject[0]}")

        chosen_subject_index = int(input("Enter your choice: ")) - 1
        chosen_subject = subjects[chosen_subject_index][0]

        while True:
            display_books_by_subject(chosen_subject, page)

            chosen_option = input(
                "Enter ISBN to add to Cart, 'n' to see next page, or press the enter key to go back to menu: \n")
            if len(chosen_option) == 10:
                add_book_to_cart(chosen_option)
            elif chosen_option == 'n':
                page += 1
            elif chosen_option == '':
                main_menu()
                break
    else:
        print("No subjects found.")
        time.sleep(2)
        main_menu()


def display_books_by_subject(subject, page):
    """Displays books by subject with pagination."""
    offset = (page - 1) * 2
    db.mycursor.execute("SELECT * FROM books WHERE subject = %s LIMIT 2 OFFSET %s", (subject, offset))
    books = db.mycursor.fetchall()
    db.mycursor.execute("SELECT COUNT(*) FROM books WHERE subject = %s", (subject,))
    total_books = db.mycursor.fetchone()[0]

    print(f"\n{total_books} books available for this Subject (Page {page})\n")
    for book in books:
        print(f"Author: {book[1]}")
        print(f"Title: {book[2]}")
        print(f"ISBN: {book[0]}")
        print(f"Price: {book[3]}")
        print(f"Subject: {book[4]}\n")


def add_book_to_cart(isbn):
    """Adds a book to the user's cart."""
    db.mycursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
    book = db.mycursor.fetchone()

    if book:
        quantity = int(input("Enter quantity: "))
        userid = get_userid()
        check_query = "SELECT qty FROM cart WHERE userid = %s AND isbn = %s"
        db.mycursor.execute(check_query, (userid, isbn))
        result = db.mycursor.fetchone()
        if result:
            # If the entry exists, update the quantity
            update_query = "UPDATE cart SET qty = qty + %s WHERE userid = %s AND isbn = %s"
            db.mycursor.execute(update_query, (quantity, userid, isbn))
        else:
            # If the entry does not exist, insert the new entry
            insert_query = "INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)"
            db.mycursor.execute(insert_query, (userid, isbn, quantity))
        # db.mycursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)", (userid, isbn, quantity))
        db.conn.commit()
        print("Book added to cart")
        time.sleep(2)
    else:
        print("Book not found.")


def get_userid():
    """Returns the logged in user's ID."""
    global logged_user_id
    if logged_user_id:
        return logged_user_id
    else:
        print("No user is logged in.")
        menu()


def search_by_author_title():
    """Allows searching books by author or title."""
    while True:
        print("Search by Author/Title")
        print("\t1. Author Search")
        print("\t2. Title Search")
        print("\t3. Go Back to Main Menu\n")

        option = input("Enter your option: ")

        if option == '':
            print("Returning to the main menu...")
            main_menu()
            break

        try:
            option = int(option)
        except ValueError:
            print("Invalid option. Please choose again.")
            continue

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
    # Handles book search by author
    while True:
        search_term = input(
            "Enter a substring of the author's name (or press Enter to go back to the previous menu): ")

        if search_term == "":
            search_by_author_title()
            break

        db.mycursor.execute("SELECT * FROM books WHERE author LIKE %s LIMIT 3", (f"%{search_term}%",))
        books = db.mycursor.fetchall()

        if books:
            display_books(books)
        else:
            print("No books found for the given author.")

        chosen_option = input(
            "\nEnter ISBN to add to Cart, 'n' to see next page, or ENTER to go back to previous menu: ").strip().lower()
        handle_option(chosen_option)


def title_search():
    # Handles book search by title
    while True:
        search_term = input(
            "Enter title or part of the title (or press Enter to go back to the previous menu): ")

        if search_term == "":
            search_by_author_title()
            break

        db.mycursor.execute("SELECT * FROM books WHERE title LIKE %s LIMIT 3", (f"%{search_term}%",))
        books = db.mycursor.fetchall()

        if books:
            display_books(books)
        else:
            print("No books found for the given title.")

        chosen_option = input(
            "\nEnter ISBN to add to Cart, 'n' to see next page, or ENTER to go back to previous menu: ").strip().lower()
        handle_option(chosen_option)


def display_books(books):
    """Displays a list of books."""
    print("\nBooks:")
    for book in books:
        print(f"Title: {book[2]}\nAuthor: {book[1]}\nISBN: {book[0]}\nPrice: {book[3]}\nSubject: {book[4]}\n")


def handle_option(chosen_option):
    """Handles options after displaying books."""
    if len(chosen_option) == 10:
        add_book_to_cart(chosen_option)
    elif chosen_option == "":
        search_by_author_title()
    elif chosen_option == "n":
        continue_browsing()
    else:
        print("Invalid option. Please try again.")


def continue_browsing():
    """Placeholder function for continued browsing."""
    print("Continuing browsing...\n")
    print("All results are displayed returning to main menu...\n")
    time.sleep(2)
    main_menu()


def checkout():
    """Handles the checkout process."""
    pretty_print("Check Out")
    display_invoice()


def display_invoice():
    """Displays the invoice for the current cart."""
    user_id = get_userid()

    print("Current Cart Contents:\n")
    db.mycursor.execute("SELECT isbn, qty FROM cart WHERE userid = %s", (user_id,))
    cart_items = db.mycursor.fetchall()

    if not cart_items:
        print("No cart items available for this user.\n")
        time.sleep(2)
        main_menu()
        return

    total_price = 0
    rows = []

    for item in cart_items:
        isbn, quantity = item
        db.mycursor.execute("SELECT title, price FROM books WHERE isbn = %s", (isbn,))
        book = db.mycursor.fetchone()

        if book:
            title, price = book
            item_total = price * quantity
            total_price += item_total
            rows.append([isbn, title, price, quantity, round(item_total, 2)])

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
    """Saves the order and displays the invoice."""
    user = get_user_data(user_id)
    current_date = datetime.now().strftime("%Y-%m-%d")
    shipment_date = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
    shipping_address, city, zip = get_shipping_data(user_id)

    db.mycursor.execute(
        "INSERT INTO orders (userid, created, shipAddress, shipCity, shipZip) VALUES (%s, %s, %s, %s, %s)",
        (user_id, current_date, shipping_address, city, zip)
    )
    order_id = db.mycursor.lastrowid
    total_price = 0

    for item in cart_items:
        isbn, quantity = item
        amount = quantity * get_book_price_by_isbn(isbn)
        db.mycursor.execute("INSERT INTO odetails (ono, isbn, qty, amount) VALUES (%s, %s, %s, %s)",
                            (order_id, isbn, quantity, amount))

    db.conn.commit()
    clear_cart(user_id)

    print(f"Invoice for Order no. {order_id}\n")
    print("Shipping Address")
    print(f"Name: {user[0]} {user[1]}")
    print(f"Address: {user[2]}\n{user[3]}\n{user[4]}")
    print(f"Estimated delivery date: {shipment_date}")
    print('-' * 45)

    rows = []
    for item in cart_items:
        isbn, quantity = item
        amount = quantity * get_book_price_by_isbn(isbn)
        total_price += amount
        rows.append([isbn, get_book_title_by_isbn(isbn), get_book_price_by_isbn(isbn), quantity, round(amount, 2)])

    print_table(rows, total_price)
    time.sleep(5)
    main_menu()


def get_shipping_data(user_id):
    """Retrieves shipping data for the user."""
    db.mycursor.execute("SELECT address, city, zip FROM members WHERE userid = %s", (user_id,))
    address, city, zip = db.mycursor.fetchone()
    return address, city, zip


def get_book_price_by_isbn(isbn):
    """Retrieves the price of a book given its ISBN."""
    db.mycursor.execute("SELECT price FROM books WHERE isbn = %s", (isbn,))
    price = db.mycursor.fetchone()
    if price:
        return price[0]
    else:
        print("Price not found for the given ISBN.")
        return None


def get_book_title_by_isbn(isbn):
    """Retrieves the title of a book given its ISBN."""
    db.mycursor.execute("SELECT title FROM books WHERE isbn = %s", (isbn,))
    title = db.mycursor.fetchone()
    if title:
        return title[0]
    else:
        print("Title not found for the given ISBN.")
        return None


def clear_cart(user_id):
    """Clears the cart for the user."""
    db.mycursor.execute("DELETE FROM cart WHERE userid = %s", (user_id,))
    db.conn.commit()
    print("Cart has been cleared.\n")


def get_user_data(user_id):
    """Retrieves user data."""
    db.mycursor.execute("SELECT * FROM members WHERE userid = %s", (user_id,))
    return db.mycursor.fetchone()


def print_table(rows, total):
    """Prints a formatted table of the order details."""
    headers = ["ISBN", "Title", "$", "Qty", "Total"]
    footers = ["Total", "", "", "", total]
    col_widths = [max(len(str(item)) for item in col) for col in zip(*rows, headers)]

    header_line = " ".join(f"{header:{col_widths[i]}}" for i, header in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    for row in rows:
        print(" ".join(f"{str(item):{col_widths[i]}}" for i, item in enumerate(row)))

    print("-" * len(header_line))
    footer_line = " ".join(f"{footer:{col_widths[i]}}" for i, footer in enumerate(footers))
    print(footer_line)
    print("-" * len(header_line))


def main():
    """Main function to initiate the program."""
    while True:
        try:
            db = Database()
            print("Database object created successfully.")
            break
        except Exception as e:
            print("Connection failed, check credentials and try again.", e)
    try:
        menu()
    finally:
        db.close_connection()


if __name__ == "__main__":
    main()