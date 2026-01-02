import mysql.connector as m
from datetime import datetime


# ---------------- DATABASE SETUP ---------------- #
def setup_database():
    con = m.connect(host="localhost", user="root", password="12345")
    cur = con.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS LIBRARY")
    cur.execute("USE LIBRARY")

    cur.execute("""CREATE TABLE IF NOT EXISTS USER(UID INT PRIMARY KEY, UNAME VARCHAR(50),
UAGE INT, UCONTACT VARCHAR(10))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS BOOK(BID INT PRIMARY KEY, BNAME VARCHAR(100),
BAUTHOR VARCHAR(100), BPUBLISHER VARCHAR(100), BEDITION VARCHAR(10))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS ISSUE(ISSUE_ID INT AUTO_INCREMENT PRIMARY KEY,
UID INT, BID INT, ISSUE_DATE DATE, TILL_DATE DATE)""")

    con.commit()
    con.close()

setup_database()

con = m.connect(host="localhost", user="root", password="12345", database="LIBRARY")
cur = con.cursor()


# ---------------- USER LOGIC ---------------- #
def modify_users():
    while True:
        print("""
--- MODIFY USERS ---
1. Add User
2. Delete User
3. Update User Contact
4. Back
""")
        ch = input("Your Choice: ")

        if ch == "1":
            add_user()

        elif ch == "2":
            delete_user()

        elif ch == "3":
            uid = input("User ID: ")
            if not uid.isdigit():
                print("Invalid User ID")
                return
            cur.execute("SELECT * FROM USER WHERE UID=%s", (uid,))
            if not cur.fetchone():
                print("User not found")
                continue

            contact = input("Enter new contact number: ")
            if contact.isdigit() and len(contact) == 10:
                cur.execute("UPDATE USER SET UCONTACT=%s WHERE UID=%s",(contact, uid))
                con.commit()
                print("User contact updated successfully")
            else:
                print("Invalid contact number")

        elif ch == "4":
            break
        else:
            print("Invalid choice")

def add_user():
    uid = input("Enter User ID: ")
    name = input("Enter Name: ")
    age = input("Enter User Age: ")
    contact = input("Enter User Contact (10 digits): ")

    if not uid.isdigit() or not age.isdigit() or not contact.isdigit() or len(contact) != 10:
        print("Invalid input")
        return

    try:
        cur.execute("INSERT INTO USER VALUES (%s,%s,%s,%s)",
                    (uid, name, age, contact))
        con.commit()
        print("User added successfully.")
    except:
        print("User ID already exists")

def delete_user():
    uid = input("Enter User ID: ")

    if not uid.isdigit():
        print("Invalid User ID")
        return

    cur.execute("SELECT * FROM ISSUE WHERE UID=%s", (uid,))
    if cur.fetchone():
        print("User has issued books, hence can't be deleted.")
        return

    cur.execute("DELETE FROM USER WHERE UID=%s", (uid,))
    con.commit()
    print("User deleted successfully")


# ---------------- BOOK LOGIC ---------------- #
def modify_books():
    while True:
        print("""
--- MODIFY BOOKS ---
1. Add Book
2. Delete Book
3. Update Book
4. Back
""")
        ch = input("Your Choice: ")

        if ch == "1":
            add_book()

        elif ch == "2":
            delete_book()

        elif ch == "3":
            bid = input("Enter Book ID: ")

            cur.execute("SELECT * FROM BOOK WHERE BID=%s", (bid,))
            if not cur.fetchone():
                print("Sorry, book not found")
                continue

            print("""
a. Update Name
b. Update Author
c. Update Publisher
d. Update Edition
""")
            op = input("Your Choice: ")

            if op == "a":
                name = input("Enter new name: ")
                cur.execute("UPDATE BOOK SET BNAME=%s WHERE BID=%s", (name, bid))
                con.commit()
                print("Book name updated successfully.")

            elif op == "b":
                author = input("Enter new author: ")
                cur.execute("UPDATE BOOK SET BAUTHOR=%s WHERE BID=%s",
                            (author, bid))
                con.commit()
                print("Author updated successfully")

            elif op == "c":
                pub = input("Enter new publisher: ")
                cur.execute("UPDATE BOOK SET BPUBLISHER=%s WHERE BID=%s",
                            (pub, bid))
                con.commit()
                print("Publisher updated successfully")

            elif op == "d":
                edi = input("Enter new edition: ")
                cur.execute("UPDATE BOOK SET BEDITION=%s WHERE BID=%s",
                            (edi, bid))
                con.commit()
                print("Edition updated successfully")

            else:
                print("Invalid option")

        elif ch == "4":
            break
        else:
            print("Invalid choice")
            
def add_book():
    bid = input("Enter Book ID: ")
    name = input("Enter Book Name: ")
    author = input("Enter Book Author: ")
    pub = input("Enter Book Publisher: ")
    edi = input("Enter Book Edition: ")

    if not bid.isdigit():
        print("Invalid Book ID")
        return

    try:
        cur.execute("INSERT INTO BOOK VALUES (%s,%s,%s,%s,%s)",
                    (bid, name, author, pub, edi))
        con.commit()
        print("Book added successfully")
    except:
        print("Book ID exists already.")

def delete_book():
    bid = input("Enter Book ID: ")

    if not bid.isdigit():
        print("Invalid Book ID")
        return

    cur.execute("SELECT * FROM ISSUE WHERE BID=%s", (bid,))
    if cur.fetchone():
        print("Book is issued, hence can't be deleted")
        return

    cur.execute("DELETE FROM BOOK WHERE BID=%s", (bid,))
    con.commit()
    print("Book deleted successfully")


# ---------------- ISSUE BOOK ---------------- #
def issue_book():
    uid = input("Enter User ID: ")
    bid = input("Enter Book ID: ")

    if not uid.isdigit() or not bid.isdigit():
        print("Invalid User ID or Book ID")
        return

    till = input("Till date (YYYY-MM-DD): ")

    try:
        till_date = datetime.strptime(till, "%Y-%m-%d").date()
    except:
        print("Invalid date")
        return

    issue_date = datetime.strptime(TODAYS_DATE, "%Y-%m-%d").date()

    if till_date <= issue_date:
        print("Error: Till date must be after issue date")
        return

    cur.execute("SELECT * FROM USER WHERE UID=%s", (uid,))
    if not cur.fetchone():
        print("Sorry, user not found")
        return

    cur.execute("SELECT * FROM BOOK WHERE BID=%s", (bid,))
    if not cur.fetchone():
        print("Sorry, book not found")
        return

    cur.execute("SELECT * FROM ISSUE WHERE BID=%s", (bid,))
    if cur.fetchone():
        print("Sorry, book already issued")
        return

    cur.execute("SELECT COUNT(*) FROM ISSUE WHERE UID=%s", (uid,))
    if cur.fetchone()[0] >= 5:
        print("Sorry, user reached issue limit")
        return

    cur.execute("INSERT INTO ISSUE (UID, BID, ISSUE_DATE, TILL_DATE) VALUES (%s,%s,%s,%s)",
            (uid, bid, issue_date, till_date))
    con.commit()
    print("Book issued successfully")


# ---------------- RETURN BOOK ---------------- #
def return_book():
    bid = input("Enter Book ID: ")

    if not bid.isdigit():
        print("Invalid Book ID")
        return

    cur.execute("SELECT TILL_DATE FROM ISSUE WHERE BID=%s", (bid,))
    data = cur.fetchone()

    if not data:
        print("Book was not issued")
        return

    till_date = data[0]
    today = datetime.strptime(TODAYS_DATE, "%Y-%m-%d").date()

    late = (today - till_date).days
    fine = late * 5 if late > 0 else 0

    print(f"Late Fine(Rs 5 per day): Rs {fine}")

    cur.execute("DELETE FROM ISSUE WHERE BID=%s", (bid,))
    con.commit()
    print("Book returned successfully")


# ---------------- DISPLAY ---------------- #
def show_users():
    text = input('''Search User By (User ID / Name / Contact) OR Press Enter For Full List: ''').strip()

    if text == "":
        cur.execute("SELECT * FROM USER")
    else:
        cur.execute("""SELECT * FROM USER WHERE UID LIKE %s OR LOWER(UNAME) LIKE %s
OR UCONTACT LIKE %s""", (f"%{text}%", f"%{text.lower()}%", f"%{text}%"))

    users = cur.fetchall()

    if not users:
        print("Sorry, no users found.")
        return

    for u in users:
        cur.execute("SELECT BID FROM ISSUE WHERE UID=%s", (u[0],))
        books = cur.fetchall()
        issued = "None" if not books else ", ".join(str(b[0]) for b in books)

        print(f"ID: {u[0]}, Name: {u[1]}, Age: {u[2]}, Contact: {u[3]}, Issued Book ID: {issued}")

def show_books():
    text = input("Search Book By(Book ID / Book Name) OR Press Enter For Full List: ").strip()

    if text == "":
        cur.execute("SELECT * FROM BOOK")
    else:
        cur.execute("""SELECT * FROM BOOK WHERE CAST(BID AS CHAR) LIKE %s
OR LOWER(BNAME) LIKE %s""", (f"%{text}%", f"%{text.lower()}%"))

    books = cur.fetchall()

    if not books:
        print("Sorry, no books found.")
        return

    for b in books:
        cur.execute("SELECT 1 FROM ISSUE WHERE BID=%s", (b[0],))
        status = "Available" if not cur.fetchone() else "Issued"

        print(f"ID: {b[0]}, Name: {b[1]}, Author: {b[2]}, "
              f"Publisher: {b[3]}, Edition: {b[4]}, Status: {status}")


# ---------------- PROGRAM START UI ---------------- #
print("=" * 45)
print("   WELCOME TO THE LIBRARY MANAGEMENT SYSTEM")
print("=" * 45)

while True:
    TODAYS_DATE = input("Enter today's date (YYYY-MM-DD): ")
    try:
        datetime.strptime(TODAYS_DATE, "%Y-%m-%d")
        break
    except:
        print("Invalid date format. Please try again.")


print("\nDate set successfully. Launching main menu...\n")


# ---------------- MAIN MENU ---------------- #
while True:
    print("""
==============================
 LIBRARY MANAGEMENT SYSTEM
==============================

1. Modify Users
2. Modify Books
3. Issue Book
4. Return Book
5. Show / Search Users
6. Show / Search Books
7. Exit
""")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        modify_users()

    elif choice == "2":
        modify_books()

    elif choice == "3":
        issue_book()

    elif choice == "4":
        return_book()

    elif choice == "5":
        show_users()

    elif choice == "6":
        show_books()

    elif choice == "7":
        print("Thank you for using the Library Management System!")
        con.close()
        break

    else:
        print("Invalid choice. Please try again.")
