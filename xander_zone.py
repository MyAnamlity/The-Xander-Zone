""" Name of program: Xander Zone
    Author: Gary Bennett
    Class: SVAD140
    Date: 12/13/2023
    This Python program is an application for users to enter a fan site to watch extreme sport videos.
"""
# Imported libraries
import tkinter as tk  # Import the tkinter library for GUI
from PIL import Image, ImageTk, ImageSequence  # Import PIL for image handling
import sqlite3  # Import SQLite for database handling
import re  # Import SQLite for database handling

# Function to open the second window
def open_second_window():
    # Create a new window
    second_window = tk.Toplevel()
    second_window.title("The Xander Zone")  # Set the window title
    second_window.geometry('600x600')   # Set window dimensions
    second_window.config(background="black")   # Set window background color

    # Load GIF frames for display
    gif_frames = []

    try:
        gif = Image.open("riding-motorbike-vin-diesel.gif")  # Load the GIF file
        # Load the GIF file
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
    except Exception as e:
        print("Error loading GIF:", e)
    # Display the GIF frames
    gif_label = tk.Label(second_window)
    gif_label.pack(fill="both", expand=True)
    gif_label.config(background="black")

    # Function to update GIF frames
    def update(frame=0):
        if gif_frames:
            # Display the GIF frame
            gif_label.config(image=gif_frames[frame])
            # Loop through frames for animation
            second_window.after(100, update, (frame + 1) % len(gif_frames))

    update()
    # Display introductory label and setup account button
    intro_label = tk.Label(second_window, text="You've just entered the Xander Zone", fg="red", bg="black", font=30)
    intro_label.pack(padx=20, pady=20)

    setup_account_button = tk.Button(second_window, text="Set-up Your account today", font=30, bg="black", fg="red",
                                     command=open_account_setup)
    setup_account_button.pack(padx=10, pady=10)

# Function to create a table in the database
def create_table():
    user_db = sqlite3.connect("user_info.db")  # Connect to the SQLite database
    cursor = user_db.cursor()
    # Create a table if not exists to store user information
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, login TEXT)")
    user_db.commit()
    user_db.close()  # Close the database connection


# Function to validate email format
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Regular expression pattern for email validation
    return re.match(email_regex, email)  # Return match result for the provided email

# Function to save user data into the database
def save_to_database(name, email, login):
    user_db = sqlite3.connect("user_info.db")  # Connect to the SQLite database
    cursor = user_db.cursor()
    # Insert user data into the database
    cursor.execute("INSERT INTO users (name, email, login) VALUES (?, ?, ?)",
                   (name, email, login))
    user_db.commit()
    user_db.close()  # Close the database connection

# Function to validate and save user information
def save_user_info(name, email, login, name_entry, email_entry, login_entry, welcome_message):
    # Check if any field is empty
    if not all((name, email, login)):
        # Handle empty fields - display an error message or prevent saving
        welcome_message.config(text="All fields are required.", fg='red', bg='black')
        return False

    # Validate email format
    if not validate_email(email):
        # Handle incorrect email format - display an error message or prevent saving
        welcome_message.config(text="Invalid email.", fg='red', bg='black')
        return False

    # Save user info
    try:
        save_to_database(name, email, login)
        # Clear text boxes after successful save
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        login_entry.delete(0, tk.END)
        # Display a welcome message with the user's login
        welcome = f"Welcome {login} to the Xander Zone!"
        welcome_message.config(text=welcome, fg='red', bg='black')
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

# Function to open the account setup window
def open_account_setup():
    account_window = tk.Toplevel()  # Create a new window for account setup
    account_window.title("Account Setup")  # Set the window title
    account_window.geometry('600x600')   # Set window dimensions
    account_window.config(background="black")  # Set window background color
    account_window.resizable(width=True, height=True)
    # Label for entering full name
    name_label = tk.Label(account_window, text="Enter Your full name", fg="red", bg="black", font=30,
                          justify="center", anchor="center")
    name_label.pack()
    # Entry field for full name
    name_entry = tk.Entry(account_window)
    name_entry.pack()
    # Label for entering email address
    email_label = tk.Label(account_window, text="Enter your email address", fg="red", bg="black", font=30,
                           justify="center", anchor="center")
    email_label.pack()
    # Entry field for email address
    email_entry = tk.Entry(account_window)
    email_entry.pack()
    # Label for entering login
    login_label = tk.Label(account_window, text="Enter your login", fg="red", bg="black", font=30,
                           justify="center", anchor="center")
    login_label.pack()
    # Entry field for login
    login_entry = tk.Entry(account_window)
    login_entry.pack()

    # Function to update the welcome message on saving
    def update_welcome_message():
        # Calling the save_user_info function with provided data and GUI elements
        save_user_info(name_entry.get(), email_entry.get(), login_entry.get(), name_entry, email_entry,
                       login_entry, welcome_message)

    # Button to trigger saving user info
    save_button = tk.Button(account_window, text="Save",
                            command=update_welcome_message,
                            bg="black", fg="red", font=("Arial", 24))
    save_button.pack()
    # Label for displaying a welcome message
    welcome_message = tk.Label(account_window, text="", fg="white", bg="black", font=("Arial", 18))
    welcome_message.pack()
    # Function call to create the database table
    create_table()


def open_first_window():
    # Creating the main window
    main_window = tk.Tk()
    main_window.title("The Xander Zone")
    main_window.geometry('600x600')
    main_window.resizable(width=True, height=True)
    main_window.config(background="black")
    # Loading the image for the welcome label
    first_page_image = ImageTk.PhotoImage(Image.open("Xxx_movie.jpg"))
    # Label for the welcome image
    welcome_label = tk.Label(main_window, image=first_page_image, bg="black")
    welcome_label.pack(fill="both", expand=True)
    # Label displaying the welcome message
    message_label = tk.Label(main_window, text="Enter the Xander Zone to "
                                               "Watch extreme videos!",
                             width=50, justify="center", anchor="center", bg="black", fg='red', font=('Arial', 18))
    message_label.pack(padx=20, pady=20)
    # Button to navigate to the second window
    enter_button = tk.Button(main_window, text="ENTER", command=open_second_window, bg="black", fg="red",
                             font=("Arial", 24))
    enter_button.pack()
    # Button to exit the application
    exit_button = tk.Button(main_window, text='EXIT', command=main_window.quit, bg='black', fg='red')
    exit_button.pack()
    # Start the main window event loop
    main_window.mainloop()


def run_tests():
    # Creating a Tkinter window for testing purposes
    test_window = tk.Tk()
    test_window.withdraw()  # Hide the test window

    # Simulating GUI elements
    name_entry_value = tk.Entry(test_window)
    name_entry_value.insert(0, "John Doe")

    email_entry_value = tk.Entry(test_window)
    email_entry_value.insert(0, "john@example.com")

    login_entry_value = tk.Entry(test_window)
    login_entry_value.insert(0, "johndoe123")

    welcome_message_label = tk.Label(test_window)

    # Testing save_user_info function
    assert save_user_info("John Doe", "john@example.com", "johndoe123",
                          name_entry_value, email_entry_value, login_entry_value, welcome_message_label) is True
    assert save_user_info("", "invalidemail", "johndoe123",
                          name_entry_value, email_entry_value, login_entry_value, welcome_message_label) is False
    assert save_user_info("John Doe", "", "johndoe123",
                          name_entry_value, email_entry_value, login_entry_value, welcome_message_label) is False
    assert save_user_info("John Doe", "john@example.com", "",
                          name_entry_value, email_entry_value, login_entry_value, welcome_message_label) is False
    assert save_user_info("John Doe", "invalidemail", "johndoe123",
                          name_entry_value, email_entry_value, login_entry_value, welcome_message_label) is False

    # Close the test window
    test_window.destroy()

#  runs test before application begins
run_tests()
# runs application
open_first_window()

