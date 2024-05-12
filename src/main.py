from getpass import getpass
from database import Database
import mysql.connector
from mysql.connector import connect
# from flask import Flask, render_template, request, redirect, url_for, session, flash
cursor = mysql.connector 


# def pretty_print(content: str, line_len: int = 45) -> None:
#     print(f"{'*' * line_len}")
#     print(f"{'***' + ' ' * (line_len - 6) + '***'}")
#     print(f"{'***' + ' ' * ((line_len - len(content) - 6) // 2) + content + ' ' * ((line_len - len(content) - 6) // 2) + ' ***'}")
#     print(f"{'***' + ' ' * (line_len - 6) + '***'}")
#     print(f"{'*' * line_len}")

# pretty_print("Welcome to Online bookstore!")

# make a choice

def pretty_print(content: str, line_len: int = 45) -> None:
        print(f"{'*' * line_len}")
        print(f"{'***' + ' ' * (line_len - 6) + '***'}")
        print(f"{'***' + ' ' * ((line_len - len(content) - 6) // 2) + content + ' ' * ((line_len - len(content) - 6) // 2) + ' ***'}")
        print(f"{'***' + ' ' * (line_len - 6) + '***'}")
        print(f"{'*' * line_len}")

def menu():
    pretty_print("Welcome to Online bookstore!")

    db = Database()
    while True:
        print(("\t" * 4) + "1. Member Login") 
        print(("\t" * 4) + "2. Member Registration")
        print(("\t" * 4) + "3. exit" + '\n' *2)
        ch = int(input("Type in your option: "))
        # Login
        if ch == 1:
            email = input("Email: ")
            password = getpass("Password: ")
            # TODO: if the typed in username/password is incorrect, let them  know. If the user doesn't exist let them know
            # if they forgot their password create a hint that would let them restore their password
            db.mycursor.execute("SELECT EXISTS(SELECT * FROM members WHERE userid = %s AND password = %s)", (email, password))
            tries = 3
            userExists = db.mycursor.fetchone()[0]
            while tries > 0:

                if userExists():
                    print("\nSuccessfully login!")
                    pretty_print("Welcome to Online bookstore\n\t     Member Menu")
                    break
                else:
                    print("Couln't find the email or password is incorrect. Register")
                tries -= 1
                break
    
        elif ch == 2:
            pretty_print("      Weclome to the Online Book Store\n         New Member Registration")
            fname = input("First name: ")
            lname = input("Lastname: ")
            adress = input("Adress: ")
            city = input("City: ")
            zip = input("Zip: ")
            pnumber = input("Phone Number: ")
            eadress = input("Email Adress: ")
   
            while True:
                if '@' not in eadress:
                    print("Invalid email adress. Please use @ in the email when registering it")
                else:
                    break
                    
            pw = getpass("Password: ")
        db = Database()
        db.mycursor.execute("INSERT INTO members(fname, lname, adress, city, zip, pnumber, eadress, pw) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s)", (fname, lname, adress, city, zip, pnumber, eadress))
        
        db.conn.commit()
        input("You have registered successfully! \
            Press ENTER to go back to Menu!: ")
        
        if "ENTER":
            menu()

def main_menu():
    pretty_print("Weclome to the Online Book Store\n\tNew Member Registration\n\n")
    print(("\t" * 4) + "1. Browse by Subject") 
    print(("\t" * 4) + "2. Search By Author/Title")
    print(("\t" * 4) + "3. Check Out")
    print(("\t") * 4 + "4. Logout" + '\n' *2)
    ch = int(input("Type in your option: "))
    db = Database()
    if ch == 1:
        db.mycursor.execute("SELECT * FROM books")
        books = db.mycursor.fetchall()

        subjects = set(books[4] for book in books)
        print("Subjects: " + "\n")



    
        


 

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
    main()
