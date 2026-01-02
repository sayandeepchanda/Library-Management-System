import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys
from datetime import datetime
from tkinter import ttk
import os


# ---------------- COLORS ---------------- #
BG_COLOR = "#F7F3D6"
TITLE_COLOR = "#000000"
LABEL_COLOR = "#000000"
BTN_BG = "#003264"
BTN_TEXT = "white"
BTN_HOVER = "#00264D"
EXIT_BG = "#8B0000"
EXIT_HOVER = "#5C0000"
ENTRY_BG = "white"
ENTRY_TEXT = "#111827"
BACK_BG = "#000000"
BACK_TEXT = "#ffffff"
BACK_HOVER = "#111111"

# ---------------- BORDER COLORS ---------------- #
BORDER_OUTER = "#1F2937"   # thick window border
BORDER_INNER = "#9CA3AF"   # thin window border
TEAM_BOX_BG = "white"
TEAM_TEXT = "#000000"


root = tk.Tk()
root.withdraw()   # hide root window

style = ttk.Style(root)
style.configure("Treeview", font=("Arial", 12), rowheight=22)
style.configure("Treeview.Heading", font=("Arial", 14, "bold"))


# ---------------- DATABASE ---------------- #
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as .py file
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_path()
db_path = os.path.join(BASE_DIR, "library.db")

con = sqlite3.connect(db_path)
cur = con.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS USER (UID INTEGER PRIMARY KEY, UNAME TEXT,
UAGE INTEGER, UCONTACT TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS BOOK (BID INTEGER PRIMARY KEY, BNAME TEXT,
BAUTHOR TEXT, BPUBLISHER TEXT, BEDITION TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS ISSUE (ISSUE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
UID INTEGER, BID INTEGER, ISSUE_DATE TEXT, TILL_DATE TEXT)""")

con.commit()


TODAYS_DATE = ""


# ---------------- CLEAN EXIT ---------------- #
def exit_program(win=None):
    try:
        cur.close()
        con.close()
    except:
        pass

    try:
        root.destroy()
    except:
        pass


# ---------------- COMMON ---------------- #
def fullscreen(win, title):
    win.title(title)
    win.state("zoomed")

def create_window_layout(win):
    # OUTER THICK BLACK
    f1 = tk.Frame(win, bg="black")
    f1.pack(fill="both", expand=True)

    # GAP
    g1 = tk.Frame(f1, bg=BG_COLOR)
    g1.pack(fill="both", expand=True, padx=8, pady=8)

    # INNER THIN BLACK
    f2 = tk.Frame(g1, bg="black")
    f2.pack(fill="both", expand=True, padx=1, pady=1)

    # GAP
    g2 = tk.Frame(f2, bg=BG_COLOR)
    g2.pack(fill="both", expand=True, padx=3, pady=3)

    # FINAL CONTENT
    content = tk.Frame(g2, bg=BG_COLOR)
    content.pack(fill="both", expand=True)

    # TEAM BOX
    team_box = tk.Frame(content, bg="white", bd=1, relief="solid")
    team_box.place(relx=0.01, rely=0.98, anchor="sw")

    tk.Label(team_box, text="Team", bg="white", font=("Arial", 11)).pack(padx=6)
    tk.Label(team_box, text="PHOENIX", bg="white",
             font=("Arial", 14, "bold")).pack(padx=6)

    return content


# ---------------- WELCOME ---------------- #
def welcome():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Welcome")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    welcome_box = tk.Frame(
    center,
    bg=BG_COLOR,
    highlightbackground="#000000",
    highlightthickness=6)
    welcome_box.pack()

    welcome_content = tk.Frame(welcome_box, bg=BG_COLOR)
    welcome_content.pack(padx=20, pady=30)


    tk.Label(welcome_content, text="WELCOME TO\nLIBRARY MANAGEMENT SYSTEM !",
             font=("Arial", 28, "bold"), bg=BG_COLOR, fg=TITLE_COLOR ).pack(pady=30)

    tk.Label(welcome_content, text="Enter Today's Date (YYYY-MM-DD)", font=("Arial", 16),
             bg=BG_COLOR, fg=LABEL_COLOR).pack()

    date_entry = tk.Entry(welcome_content, font=("Arial", 14), bg=ENTRY_BG, fg=ENTRY_TEXT,
                          insertbackground=ENTRY_TEXT, justify="center")
    date_entry.pack(pady=10)

    def go():
        date_value = date_entry.get()

        if date_value == "":
            messagebox.showwarning("Missing Date", "Please enter today's date.")
            date_entry.focus_set()
            return
        try:
            datetime.strptime(date_value, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date Format",
                                 "Please enter the date in YYYY-MM-DD format.")
            date_entry.focus_set()
            return
        global TODAYS_DATE
        TODAYS_DATE = date_value

        win.destroy()
        main_menu()


    # Buttons row
    btn_frame = tk.Frame(welcome_content, bg=BG_COLOR)
    btn_frame.pack(pady=30)
    tk.Button(btn_frame, text="ENTER", width=18, height=2, font=("Arial", 16),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=go).pack(side="left", padx=15)

    tk.Button(btn_frame, text="EXIT", width=18, height=2, font=("Arial", 16),
              bg=EXIT_BG, fg=BTN_TEXT, activebackground=EXIT_HOVER,
              command=lambda: exit_program(win)).pack(side="left", padx=15)


# ---------------- MAIN MENU ---------------- #
def main_menu():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Main Menu")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)
    

    tk.Label(center,
    text="LIBRARY MANAGEMENT SYSTEM\nMAIN MENU",
    font=("Arial", 26, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
).pack(pady=30)


    tk.Button(center, text="Modify Users", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), modify_users()]).pack(pady=8)

    tk.Button(center, text="Modify Books", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), modify_books()]).pack(pady=8)

    tk.Button(center, text="Issue Book", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), issue_book()]).pack(pady=8)

    tk.Button(center, text="Return Book", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), return_book()]).pack(pady=8)

    tk.Button(center, text="Display Users", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), display_users()]).pack(pady=8)

    tk.Button(center, text="Display Books", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), display_books()]).pack(pady=8)

    tk.Button(center, text="Exit", width=30, height=2, font=("Arial", 14),
              bg=EXIT_BG, fg=BTN_TEXT, activebackground=EXIT_HOVER,
              command=lambda: exit_program(win)).pack(pady=8)


# ---------------- MODIFY USERS MENU ---------------- #
def modify_users():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Modify Users")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)


    tk.Label(center, text="MODIFY USERS", font=("Arial", 24, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=30)

    tk.Button(center, text="Add User", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), add_user()]).pack(pady=8)

    tk.Button(center, text="Delete User", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), delete_user()]).pack(pady=8)

    tk.Button(center, text="Update User Contact", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), update_user_contact()]).pack(pady=8)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), main_menu()]).pack(pady=20)


# ---------------- ADD USER ---------------- #
def add_user():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Add User")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="ADD USER",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="User ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    uid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    uid.pack(pady=8)

    tk.Label(center, text="User Name", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    uname = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    uname.pack(pady=8)

    tk.Label(center, text="User Age", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    uage = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    uage.pack(pady=8)

    tk.Label(center, text="Contact Number", font=("Arial", 14), bg=BG_COLOR,
             fg=LABEL_COLOR).pack()
    ucontact = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    ucontact.pack(pady=8)

    def save_user():
        if not uid.get() or not uname.get() or not uage.get() or not ucontact.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not uid.get().isdigit():
            messagebox.showerror("Error", "User ID must be numeric")
            return
        if not uage.get().isdigit():
            messagebox.showerror("Error", "Age must be numeric")
            return
        if not ucontact.get().isdigit() or len(ucontact.get()) != 10:
            messagebox.showerror("Error", "Contact number must be exactly 10 digits")
            return
        try:
            cur.execute("INSERT INTO USER VALUES(?, ?, ?, ?)",
                        (uid.get(), uname.get(), uage.get(), ucontact.get()))
            con.commit()
            messagebox.showinfo("Success", "User Added Successfully")
        except:
            messagebox.showerror("Error", "User ID already exists")

        uid.delete(0, tk.END)
        uname.delete(0, tk.END)
        uage.delete(0, tk.END)
        ucontact.delete(0, tk.END)

    tk.Button(center, text="Add User", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=save_user).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), modify_users()]).pack()


# ---------------- UPDATE USER (CONTACT ONLY) ---------------- #
def update_user_contact():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Update User Contact")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="UPDATE USER CONTACT",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="User ID", font=("Arial", 14),bg=BG_COLOR, fg=LABEL_COLOR).pack()
    uid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    uid.pack(pady=8)

    tk.Label(center, text="New Contact Number", font=("Arial", 14),
             bg=BG_COLOR, fg=LABEL_COLOR).pack()
    contact = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    contact.pack(pady=8)

    def update_contact():
        if not uid.get() or not contact.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not uid.get().isdigit():
            messagebox.showerror("Error", "User ID must be numeric")
            return
        if not contact.get().isdigit() or len(contact.get()) != 10:
            messagebox.showerror("Error", "Contact number must be exactly 10 digits")
            return
        cur.execute("SELECT * FROM USER WHERE UID=?", (uid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "User not found")
            return
        cur.execute("UPDATE USER SET UCONTACT=? WHERE UID=?",
                (contact.get(), uid.get()))
        con.commit()

        messagebox.showinfo("Success", "Contact Updated Successfully")
        uid.delete(0, tk.END)
        contact.delete(0, tk.END)

    tk.Button(center, text="Update", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=update_contact).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), modify_users()]).pack()


# ---------------- DELETE USER ---------------- #
def delete_user():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Delete User")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="DELETE USER",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="User ID", font=("Arial", 14),bg=BG_COLOR, fg=LABEL_COLOR).pack()
    uid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    uid.pack(pady=8)

    def delete():
        if not uid.get():
            messagebox.showerror("Error", "Please enter User ID")
            return

        if not uid.get().isdigit():
            messagebox.showerror("Error", "User ID must be numeric")
            return
        cur.execute("SELECT * FROM USER WHERE UID=?", (uid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "User not found")
            return
        cur.execute("SELECT 1 FROM ISSUE WHERE UID=?", (uid.get(),))
        if cur.fetchone():
            messagebox.showerror("Error", "User has issued books")
            return

        cur.execute("DELETE FROM USER WHERE UID=?", (uid.get(),))
        con.commit()
        messagebox.showinfo("Deleted", "User Deleted")
        uid.delete(0, tk.END)

    tk.Button(center, text="Delete", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=delete).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), modify_users()]).pack()


# ---------------- MODIFY BOOKS MENU ---------------- #
def modify_books():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Modify Books")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="MODIFY BOOKS",
             font=("Arial", 24, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=30)

    tk.Button(center, text="Add Book", width=30, height=2,
              font=("Arial", 14), bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), add_book()]).pack(pady=8)

    tk.Button(center, text="Delete Book", width=30, height=2,
              font=("Arial", 14), bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), delete_book()]).pack(pady=8)

    tk.Button(center, text="Update Book", width=30, height=2,
              font=("Arial", 14), bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), update_book_menu()]).pack(pady=8)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), main_menu()]).pack(pady=20)


# ---------------- ADD BOOK ---------------- #
def add_book():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Add Book")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="ADD BOOK",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="Book ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    tk.Label(center, text="Book Name", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    name = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    name.pack(pady=8)

    tk.Label(center, text="Author", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    author = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    author.pack(pady=8)

    tk.Label(center, text="Publisher", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    pub = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    pub.pack(pady=8)

    tk.Label(center, text="Edition", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    edi = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    edi.pack(pady=8)

    def save():
        if not bid.get() or not name.get() or not author.get() or not pub.get() or not edi.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not bid.get().isdigit():
            messagebox.showerror("Error", "Book ID must be numeric")
            return
        try:
            cur.execute("INSERT INTO BOOK VALUES(?, ?, ?, ?, ?)",
                        (bid.get(), name.get(), author.get(), pub.get(), edi.get()))
            con.commit()
            messagebox.showinfo("Success", "Book Added Successfully")
        except:
            messagebox.showerror("Error", "Book ID already exists")

        bid.delete(0, tk.END)
        name.delete(0, tk.END)
        author.delete(0, tk.END)
        pub.delete(0, tk.END)
        edi.delete(0, tk.END)
        
    tk.Button(center, text="Add Book", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=save).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), modify_books()]).pack()


# ---------------- DELETE BOOK ---------------- #
def delete_book():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Delete Book")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))
 
    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="DELETE BOOK",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="Book ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    def delete():
        if not bid.get():
            messagebox.showerror("Error", "Please enter Book ID")
            return
        if not bid.get().isdigit():
            messagebox.showerror("Error", "Book ID must be numeric")
            return
        cur.execute("SELECT * FROM BOOK WHERE BID=?", (bid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "Book not found")
            return
        cur.execute("SELECT 1 FROM ISSUE WHERE BID=?", (bid.get(),))
        if cur.fetchone():
            messagebox.showerror("Error", "Book is currently issued")
            return

        cur.execute("DELETE FROM BOOK WHERE BID=?", (bid.get(),))
        con.commit()

        messagebox.showinfo("Deleted", "Book Deleted Successfully")
        bid.delete(0, tk.END)
        
    tk.Button(center, text="Delete", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=delete).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), modify_books()]).pack()


# ---------------- UPDATE BOOK MENU ---------------- #
def update_book_menu():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Update Book")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="UPDATE BOOK",
             font=("Arial", 24, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=30)

    tk.Button(center, text="Update Book Name", width=30, height=2,
              font=("Arial", 14), bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), update_book_name()]).pack(pady=8)

    tk.Button(center, text="Update Author Name", width=30, height=2,
              font=("Arial", 14), bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), update_book_author()]).pack(pady=8)

    tk.Button(center, text="Update Publisher Name", width=30, height=2,
              font=("Arial", 14), bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), update_book_publisher()]).pack(pady=8)

    tk.Button(center, text="Update Edition", width=30, height=2,
              font=("Arial", 14), bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=lambda: [win.destroy(), update_book_edition()]).pack(pady=8)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), modify_books()]).pack(pady=20)


def update_book_name():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Update Book Name")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="UPDATE BOOK NAME",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="Book ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    tk.Label(center, text="New Book Name", font=("Arial", 14), bg=BG_COLOR,
             fg=LABEL_COLOR).pack()
    name = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    name.pack(pady=8)

    def update():
        if not bid.get() or not name.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not bid.get().isdigit():
            messagebox.showerror("Error", "Book ID must be numeric")
            return
        cur.execute("SELECT * FROM BOOK WHERE BID=?", (bid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "Book not found")
            return
        cur.execute("UPDATE BOOK SET BNAME=? WHERE BID=?",
                (name.get(), bid.get()))
        con.commit()

        messagebox.showinfo("Success", "Book Name Updated")
        bid.delete(0, tk.END)
        name.delete(0, tk.END)

    tk.Button(center, text="Update", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=update).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), update_book_menu()]).pack()


def update_book_author():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Update Author")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="UPDATE AUTHOR NAME",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="Book ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    tk.Label(center, text="New Author Name", font=("Arial", 14), bg=BG_COLOR,
             fg=LABEL_COLOR).pack()
    author = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    author.pack(pady=8)

    def update():
        if not bid.get() or not author.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not bid.get().isdigit():
            messagebox.showerror("Error", "Book ID must be numeric")
            return
        cur.execute("SELECT * FROM BOOK WHERE BID=?", (bid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "Book not found")
            return
        cur.execute("UPDATE BOOK SET BAUTHOR=? WHERE BID=?",
                (author.get(), bid.get()))
        con.commit()

        messagebox.showinfo("Success", "Author Updated Successfully")
        author.delete(0, tk.END)
        bid.delete(0, tk.END)

    tk.Button(center, text="Update", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=update).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), update_book_menu()]).pack()


def update_book_publisher():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Update Publisher")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="UPDATE PUBLISHER NAME",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="Book ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    tk.Label(center, text="New Publisher Name", font=("Arial", 14),
             bg=BG_COLOR, fg=LABEL_COLOR).pack()
    pub = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    pub.pack(pady=8)

    def update():
        if not bid.get() or not pub.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not bid.get().isdigit():
            messagebox.showerror("Error", "Book ID must be numeric")
            return
        cur.execute("SELECT * FROM BOOK WHERE BID=?", (bid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "Book not found")
            return
        cur.execute("UPDATE BOOK SET BPUBLISHER=? WHERE BID=?",
                (pub.get(), bid.get()))
        con.commit()
        messagebox.showinfo("Success", "Publisher Updated Successfully")
        pub.delete(0, tk.END)
        bid.delete(0, tk.END)

    tk.Button(center, text="Update", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=update).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), update_book_menu()]).pack()


def update_book_edition():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Update Edition")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))
    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="UPDATE EDITION",
             font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

    tk.Label(center, text="Book ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    tk.Label(center, text="New Edition", font=("Arial", 14), bg=BG_COLOR,
             fg=LABEL_COLOR).pack()
    edi = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    edi.pack(pady=8)

    def update():
        if not bid.get() or not edi.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not bid.get().isdigit():
            messagebox.showerror("Error", "Book ID must be numeric")
            return
        cur.execute("SELECT * FROM BOOK WHERE BID=?", (bid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "Book not found")
            return
        cur.execute("UPDATE BOOK SET BEDITION=? WHERE BID=?",
                (edi.get(), bid.get()))
        con.commit()
        messagebox.showinfo("Success", "Edition Updated Successfully")
        edi.delete(0, tk.END)
        bid.delete(0, tk.END)

    tk.Button(center, text="Update", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=update).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), update_book_menu()]).pack()


# ---------------- ISSUE BOOK ---------------- #
def issue_book():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Issue Book")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="ISSUE BOOK",
             font=("Arial", 24, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=30)

    tk.Label(center, text="Book ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    tk.Label(center, text="User ID", font=("Arial", 14), bg=BG_COLOR, fg=LABEL_COLOR).pack()
    uid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    uid.pack(pady=8)

    # TODAY'S DATE (FROM HOME SCREEN)
    tk.Label(center, text="Today's Date", font=("Arial", 14), bg=BG_COLOR,
             fg=LABEL_COLOR).pack()
    today = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    today.insert(0, TODAYS_DATE)
    today.config(state="readonly")
    today.pack(pady=8)

    tk.Label(center, text="Till Date (YYYY-MM-DD)", font=("Arial", 14),
             bg=BG_COLOR, fg=LABEL_COLOR).pack()
    till = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG,
                   fg=ENTRY_TEXT, insertbackground=ENTRY_TEXT, justify="center")
    till.pack(pady=8)

    def issue():
        if not uid.get() or not bid.get() or not till.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not uid.get().isdigit() or not bid.get().isdigit():
            messagebox.showerror("Error", "ID must be numeric")
            return
        try:
            till_date_obj = datetime.strptime(till.get(), "%Y-%m-%d")
            issue_date_obj = datetime.strptime(TODAYS_DATE, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Till date must be YYYY-MM-DD")
            return
        # Till date must be AFTER issue date
        if till_date_obj <= issue_date_obj:
            messagebox.showerror("Invalid Date","Till date must be greater than Issue Date")
            return

        cur.execute("SELECT * FROM USER WHERE UID=?", (uid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "User not found")
            return
        cur.execute("SELECT * FROM BOOK WHERE BID=?", (bid.get(),))
        if not cur.fetchone():
            messagebox.showerror("Error", "Book not found")
            return
        cur.execute("SELECT * FROM ISSUE WHERE BID=?", (bid.get(),))
        if cur.fetchone():
            messagebox.showerror("Error", "Book already issued")
            return
        cur.execute("SELECT COUNT(*) FROM ISSUE WHERE UID=?", (uid.get(),))
        count = cur.fetchone()[0]
        if count >= 5:
            messagebox.showerror("Limit Reached",
                             "User has already issued 5 books")
            return
        cur.execute("""INSERT INTO ISSUE (UID, BID, ISSUE_DATE, TILL_DATE)
VALUES (?, ?, ?, ?)""",(uid.get(), bid.get(), TODAYS_DATE, till.get()))

        con.commit()

        messagebox.showinfo("Success", "Book Issued Successfully")
        uid.delete(0, tk.END)
        bid.delete(0, tk.END)



    tk.Button(center, text="Issue", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=issue).pack(pady=15)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14), bg=BACK_BG,
              fg=BACK_TEXT, activebackground=BACK_HOVER, activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), main_menu()]).pack()


# ---------------- RETURN BOOK ---------------- #
def return_book():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Return Book")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    center = tk.Frame(frame, bg=BG_COLOR)
    center.pack(expand=True)

    tk.Label(center, text="RETURN BOOK", font=("Arial", 24, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=30)

    tk.Label(center, text="Book ID", font=("Arial", 14),
             bg=BG_COLOR, fg=LABEL_COLOR).pack()

    bid = tk.Entry(center, font=("Arial", 16), width=32, bg=ENTRY_BG, fg=ENTRY_TEXT,
                   insertbackground=ENTRY_TEXT, justify="center")
    bid.pack(pady=8)

    def return_now():
        if not bid.get():
            messagebox.showerror("Error", "Please enter Book ID")
            return

        if not bid.get().isdigit():
            messagebox.showerror("Error", "Book ID must be numeric")
            return

        book_id = bid.get()

        cur.execute("SELECT * FROM ISSUE WHERE BID=?", (book_id,))
        data = cur.fetchone()

        if data is None:
            messagebox.showerror("Error", "Book not issued")
            return

        till_date = data[4]  # TILL_DATE

        today_date = datetime.strptime(TODAYS_DATE, "%Y-%m-%d")
        till_date_obj = datetime.strptime(till_date, "%Y-%m-%d")

        late_days = max(0, (today_date - till_date_obj).days)

        if late_days > 0:
            fine = late_days * 5
            msg = f"Book Returned\n\nLate by {late_days} days\nFine: Rs {fine}"
        else:
            fine = 0
            msg = "Book Returned\n\nReturned on time\nNo fine"

        cur.execute("DELETE FROM ISSUE WHERE BID=?", (book_id,))
        con.commit()

        messagebox.showinfo("Book Returned", msg)
        bid.delete(0, tk.END)

    tk.Button(center, text="Return Book", width=30, height=2, font=("Arial", 14),
              bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
              command=return_now).pack(pady=10)

    tk.Button(center, text="Back", width=30, height=2, font=("Arial", 14),
              bg=BACK_BG, fg=BACK_TEXT, activebackground=BACK_HOVER,
              activeforeground=BACK_TEXT, command=lambda: [win.destroy(), main_menu()]).pack()


# ---------------- DISPLAY ---------------- #
def display_users():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Display Users")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    top = tk.Frame(frame, bg=BG_COLOR)
    top.pack(pady=(10, 5))

    table_area = tk.Frame(frame, bg=BG_COLOR)
    table_area.pack(expand=True, fill="both")

    bottom = tk.Frame(frame, bg=BG_COLOR)
    bottom.pack(pady=(5, 20))

    tk.Label(top, text="DISPLAY USERS",
             font=("Arial", 24, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=10)

    search_box = tk.Frame(top, bg=BG_COLOR)
    search_box.pack(pady=10)

    tk.Label(search_box, text="Enter User ID / Name / Contact",
             font=("Arial", 14), bg=BG_COLOR).pack()

    search_row = tk.Frame(search_box, bg=BG_COLOR)
    search_row.pack(pady=5)
    tk.Label(search_row, text="Search",
             font=("Arial", 14),
             bg=BG_COLOR).pack(side="left", padx=(0, 8))

    search_entry = tk.Entry(search_row, font=("Arial", 16),
                        width=30, justify="center")
    search_entry.pack(side="left")

    tk.Label(search_row, text="", bg=BG_COLOR, width=6).pack(side="left")

    cols = ("UID", "NAME", "AGE", "CONTACT", "ISSUED BOOKS (ID)")
    tree = ttk.Treeview(table_area, columns=cols, show="headings", height=15)
    tree.pack(expand=True, fill="both", padx=20, pady=10)

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center", width=180)

    def load_users(text=""):
        tree.delete(*tree.get_children())

        cur.execute("""SELECT * FROM USER WHERE UID LIKE ? OR LOWER(UNAME) LIKE ?
OR UCONTACT LIKE ?""", (f"%{text}%", f"%{text.lower()}%", f"%{text}%"))

        users = cur.fetchall()

        if text and not users:
            messagebox.showinfo("Result", "No user found")
            return

        for u in users:
            cur.execute("""SELECT BID FROM ISSUE WHERE UID=?""", (u[0],))

            books = cur.fetchall()
            issued = "None" if not books else ", ".join(str(b[0]) for b in books)

            tree.insert("", "end", values=(*u, issued))

    load_users()
    search_entry.bind("<KeyRelease>",
                      lambda e: load_users(search_entry.get().strip()))

    tk.Button(bottom, text="Back", width=30, height=2, font=("Arial", 14), bg=BACK_BG,
              fg=BACK_TEXT, activebackground=BACK_HOVER, activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), main_menu()]).pack()
    

def display_books():
    win = tk.Toplevel(root)
    win.configure(bg=BG_COLOR)
    fullscreen(win, "Display Books")
    win.protocol("WM_DELETE_WINDOW", lambda: exit_program(win))

    frame = create_window_layout(win)
    top = tk.Frame(frame, bg=BG_COLOR)
    top.pack(pady=(10, 5))

    table_area = tk.Frame(frame, bg=BG_COLOR)
    table_area.pack(expand=True, fill="both")

    bottom = tk.Frame(frame, bg=BG_COLOR)
    bottom.pack(pady=(5, 20))

    tk.Label(top, text="DISPLAY BOOKS",
             font=("Arial", 24, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=10)

    search_box = tk.Frame(top, bg=BG_COLOR)
    search_box.pack(pady=10)

    tk.Label(search_box, text="Enter Book ID / Book Name",
             font=("Arial", 14), bg=BG_COLOR).pack()

    search_row = tk.Frame(search_box, bg=BG_COLOR)
    search_row.pack(pady=5)
    tk.Label(search_row, text="Search",
             font=("Arial", 14),
             bg=BG_COLOR).pack(side="left", padx=(0, 8))

    search_entry = tk.Entry(search_row, font=("Arial", 16),
                        width=30, justify="center")
    search_entry.pack(side="left")

    tk.Label(search_row, text="", bg=BG_COLOR, width=6).pack(side="left")

    cols = ("BID", "NAME", "AUTHOR", "PUBLISHER", "EDITION", "AVAILABLE")
    tree = ttk.Treeview(table_area, columns=cols, show="headings", height=15)
    tree.pack(expand=True, fill="both", padx=20, pady=10)

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center", width=160)

    def load_books(text=""):
        tree.delete(*tree.get_children())

        cur.execute("""SELECT * FROM BOOK WHERE CAST(BID AS TEXT) LIKE ?
OR LOWER(BNAME) LIKE ?""", (f"%{text}%", f"%{text.lower()}%"))


        books = cur.fetchall()

        if text and not books:
            messagebox.showinfo("Result", "No book found")
            return

        for b in books:
            cur.execute("SELECT 1 FROM ISSUE WHERE BID=?", (b[0],))
            status = "NO" if cur.fetchone() else "YES"
            tree.insert("", "end", values=(*b, status))

    load_books()
    search_entry.bind("<KeyRelease>",
                      lambda e: load_books(search_entry.get().strip()))

    tk.Button(bottom, text="Back", width=30, height=2, font=("Arial", 14), bg=BACK_BG,
              fg=BACK_TEXT, activebackground=BACK_HOVER, activeforeground=BACK_TEXT,
              command=lambda: [win.destroy(), main_menu()]).pack()


# ---------------- START ---------------- #
welcome()
root.mainloop()
