from customtkinter import *
from TwoFA.setup2FA import verify_2FA_code
from Cryptography.crypto import *
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip, json, sys, os, time


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


set_appearance_mode("dark")  # Setting application mode to dark.
set_default_color_theme("green")  # Setting application theme to green.

app = CTk()  # Creating CTk window for application.
app.iconbitmap(resource_path("Images/logo.ico"))  # Setting Icon as logo.ico
app.title("Wake Up, Neo...")  # Adding a title for the application window.


app.configure(fg_color = "black")  # Sets application background color to black.
app.attributes('-fullscreen', True)  # Sets application size to fullscreen.


def matrix_animation():
    """ Animating "Wake up Neo..." introduction to the program. """

    matrix_intro.place(relx=0.15, rely=0.15, anchor=CENTER)
    matrix_text = matrix_intro.create_text(10, 10, text="", font=("roboto", 20, "normal"), fill="#80ff80", anchor=NW)
    matrix_sentence = "Wake up, Neo..."
    small_delta = 200
    large_delta = 400
    delay = 0
    count = 1
    for i in matrix_sentence:
        if i != " " and i !=".":
            delta = small_delta
        else:
            delta = large_delta
        s = matrix_sentence[:count]
        new_text = lambda s=s: matrix_intro.itemconfigure(matrix_text, text=s)
        matrix_intro.after(delay, new_text)
        count += 1
        delay += delta
    app.after(4500, lambda: enter_matrix_button.place(relx=0.5, rely=0.55, anchor=CENTER))
    app.after(4500, lambda: matrix_entry.place(relx=0.5, rely=0.45, anchor=CENTER))
    

def red_pill():
    """ Destroys old widgets and places two factor authentication widgets. """

    app.title("2FA")  # Modifying the title for the application window.

    enter_matrix_button.destroy(), matrix_entry.destroy(), matrix_intro.destroy()  # Destroys matrix widgets.

    two_factor_label.place(relx=0.5, rely=0.45, anchor=CENTER)  # Placing Two Factor Label.
    two_factor_entry.place(relx=0.5, rely=0.5, anchor=CENTER)  # Placing Two Factor Entry Box.
    submit_button.place(relx=0.5, rely=0.55, anchor=CENTER)  # Placing Submit Button.


def matrix_test():
    """ The user must prove worthy in order to enter the application. """

    matrix_value = matrix_entry.get()  # Grabbing value from entry box and storing as "matrix_value".

    if matrix_value.lower() == "the matrix has you..." or matrix_value.lower() == "thematrixhasyou...":  # If value equals string execute "redpill" function.
        red_pill()
    else:  # Else (if string is not equal) destroy the application.
        app.destroy()


def verify_code(code):
    """ Verifies code and opens Password Manager. If code is invalid the application closes. """

    if verify_2FA_code(code):  # If code is valid, update application.
        password_manager()
    else:  # Else, code is invalid and close application.
        app.destroy()


def password_manager():
    """ Updates password manager window and creates associated functions. """

    def search():
        """ Search account information based on website / application name. """

        website = website_entry.get()  # Grabs current website text and stores in 'website' variable.
        try:  # Attempts to open 'data.json' in the Bit-Safe folder and loads file into 'data' dictionary.
            with open(resource_path("C:\Bit-Safe\data.json")) as data_dict:
                data = json.load(data_dict)
        except FileNotFoundError:  # If 'FileNotFoundError' occurs error message box appears.
            messagebox.showinfo(title="Error", message="Error: File not found.")
        else:  # Retrieves key from separate hard drive and decrpyts ciphertext, displaying email/username and plaintext password.
            if website in data:
                email_username = data[website]["Email-Username"]
                plaintext = retrieve_key_and_password(website, data[website]["Password"])
                messagebox.showinfo(title=website, message=f"Email or Username: {email_username}\nPassword: {plaintext}")
            else:  # Displays error message box if website details are not found.
                messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


    def generate_password():
        """ Generates a random password and copies the password to clipboard. Be wary, clipboard history can be pulled from Bash. """

        # Storing all letter, number, and symbol options in 'letters', 'numbers', and 'symbols' variables.
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        # Randomly chooses letters, numbers, and symbols in 'password_letters', 'password_numbers', and ' password_symbols'.
        password_letters = [choice(letters) for letter in range(randint(8, 10))]
        password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
        password_numbers = [choice(numbers) for number in range(randint(2, 4))]

        # Adds all randomly choosen characters to 'password_list' and shuffles the characters.
        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        # Joins password, inserts result into 'password_entry' widget, and copies result to clipboard.
        password = "".join(password_list)
        password_entry.insert(0, password)
        pyperclip.copy(password)


    def list_websites():
        """ Returns a list of websites that have password saved. """

        try:  # Attempts to open 'data.json' in the Bit-Safe folder and loads file into 'data' dictionary. 
            with open(resource_path("C:\Bit-Safe\data.json")) as data_dict:
                data = json.load(data_dict)
        except FileNotFoundError:  # If 'FileNotFoundError' occurs error message box appears.
            messagebox.showinfo(title="Error", message="Error: File not found.")
        else:  # Takes a list of website keys from the Bit-Safe and displays websites on screen.
            websites = list(data.keys())  # Bug occurred when displaying 'websites' in message box, so reformatting was necessary.
            formatted_websites = '{}'.format(websites)
            messagebox.showinfo(title="List of Websites", message=formatted_websites)


    def show():
        """ Show Password Entry in Plaintext. """

        password_entry.configure(show="")


    def disguise():
        """ Disguise Password Entry as '*'. """

        password_entry.configure(show="*")


    def save():
        """ Saves a given Email/Username and Password in Ciphertext form."""

        website = website_entry.get()  # Storing 'website_entry' data into 'website' variable.
        email_username = email_username_entry.get()  # Storing 'email_username_entry' data into 'email_username' variable.
        password = password_entry.get()  # Storing 'website_entry' data into 'website' variable.
        plaintext_bytes = text_to_binary(password)  # Turns password into bytes.
        key = generate_key(plaintext_bytes)  # Stores one-time pad key as 'key' based on 'plaintext_bytes' length.
        save_to_drive(name=website, key=key)  # Saves key onto the separate drive under 'website'.txt.
        ciphertext = XOR(key, plaintext_bytes)  # Turns password into bytes.
        key = ''  # Overwrites 'key' variable.
        new_data = {  # Creates data structure to be saved into the Bit-Safe.
            website: {
                "Email-Username": email_username,
                "Password": ciphertext,
            }
        }
        if len(website) == 0 or len(password) == 0:  # If website or password fields are empty, a error message box is displayed.
            messagebox.showinfo(title="Oops", message="Error: One or more field(s) are empty.")
        else:
            try:  # Attempts to open and read 'data.json' file, storing in 'data' dictionary.
                with open(resource_path("C:\Bit-Safe\data.json"), "r") as file:
                    data = json.load(file)
            except FileNotFoundError:  # If 'FileNotFoundError' error occurs, 'Bit-Safe/data.json' is created.
                with open(resource_path("C:\Bit-Safe\data.json"), "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)  # Updates 'data' with 'new_data' adding additional credentials in the process.
                with open(resource_path("C:\Bit-Safe\data.json"), "w") as file:
                    json.dump(data, file, indent=4)
            finally:  # Lastly, delete old 'website' and 'password' entry data.
                website_entry.delete(0, END)
                password_entry.delete(0, END)


    # Reformats app's window size, destroys old widgets, changes the window title, and adds padding around all widgets.
    two_factor_entry.destroy(), two_factor_label.destroy(), submit_button.destroy()
    app.title("Password Manager")
    app.configure(fg_color=["gray92", "gray14"])

    # Loads image and places the logo at the top center of the screen.
    logo = PhotoImage(file=resource_path("Images/logo.png"))
    logo_img = CTkLabel(app, image=logo, text="")
    logo_img.place(relx=0.5, rely=0.25, anchor=CENTER)

    # Creating and placing website label.
    website_label = CTkLabel(app, text="Website:", font=("Helvetica", 36, "bold"))
    website_label.place(relx=0.35, rely=0.6, anchor=CENTER)

    # Creating and placing website entry field.
    website_entry = CTkEntry(app, width=200, height=50, placeholder_text="Enter Website or Application Name")
    website_entry.place(relx=0.5, rely=0.6, anchor=CENTER)
    website_entry.focus()

    # Creating and placing search button. Button checks website field, if field corresponds to data file the username/email and password appear.
    search_button = CTkButton(app, text="Search", height=50, command=search, font=("Helvetica", 24, "normal"))
    search_button.place(relx=0.65, rely=0.6, anchor=CENTER)

    # Creating and placing email/username label.
    email_username_label = CTkLabel(app, text="Email/Username:", font=("Helvetica", 36, "bold"))
    email_username_label.place(relx=0.35, rely=0.7, anchor=CENTER)

    # Creating and placing email/username entry field.
    email_username_entry = CTkEntry(app, width=200, height=50, placeholder_text="Enter Email or Username")
    email_username_entry.place(relx=0.5, rely=0.7, anchor=CENTER)
    email_username_entry.insert(0, "spitzerlucas25@gmail.com")

    # Creating and placing password label.
    password_label = CTkLabel(app, text="Password:", font=("Helvetica", 36, "bold"))
    password_label.place(relx=0.35, rely=0.8, anchor=CENTER)

    # Creating and placing password entry field.
    password_entry = CTkEntry(app, width=200, height=50, show="*", placeholder_text="Enter or Generate Password")
    password_entry.place(relx=0.5, rely=0.8, anchor=CENTER)

    # Creating and placing generate button. Button generates a random password of letters, numbers, and symbols.
    generate_button = CTkButton(app, text="Generate Password", height=50, width=250, command=generate_password, font=("Helvetica", 24, "normal"))
    generate_button.place(relx=0.65, rely=0.8, anchor=CENTER)

    # Creating and placing list button. Button lists the websites which have data stored in the Bit-Safe.
    list_button = CTkButton(app, text="List Websites", height=50, width=175, command=list_websites, font=("Helvetica", 24, "normal"))
    list_button.place(relx=0.65, rely=0.7, anchor=CENTER)

    # Creating and placing add button. Button saves credentials active in the app to the Bit-Safe.
    add_button = CTkButton(app, text="Add Credentials", command=save, font=("Helvetica", 24, "normal"), width=200, height=50)
    add_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    # Creating and placing show button. 
    show_button = CTkButton(app, text="Display PW", command=show, font=("Helvetica", 24, "normal"), width=200, height=50)
    show_button.place(relx=0.65, rely=0.9, anchor=CENTER)

    # Creating and placing disguise button.
    disguise_button = CTkButton(app, text="Disguise PW", command=disguise, font=("Helvetica", 24, "normal"), width=200, height=50)
    disguise_button.place(relx=0.35, rely=0.9, anchor=CENTER)

    # Creating and placing close button.
    close_button = CTkButton(app, text="X", height=50, width=50, command=app.destroy, font=("Helvetica", 24, "normal"), fg_color="red", hover_color="#a52a2a")
    close_button.place(relx=0.985, rely=0.025, anchor=CENTER)

# Creating matrix intro canvas with a global scope.
matrix_intro = CTkCanvas(app, bg="black", highlightbackground="black")

# Creating matrix button with a global scope.
enter_matrix_button = CTkButton(app, width=150, text="Next Move?", fg_color="#80ff80", text_color="black", command=matrix_test)

# Creating matrix value and entry box with a global scope.
matrix_value = StringVar(app, value="")
matrix_entry = CTkEntry(app, border_color="#80ff80", show="*", fg_color="black", text_color="#80ff80", width=200, height=35, textvariable=matrix_value, font=("Roboto", 20, "normal"))

# Creating label widget.
two_factor_label = CTkLabel(app, font=("Roboto", 24, "normal"), text="Enter Code:")

# Creating variable and entry widget.
code = StringVar(app, value="")
two_factor_entry = CTkEntry(app, width=80, height=35, show="*", textvariable=code, font=("Roboto", 20, "normal"))

# Submit button used to call "verify_code()" after entering verification code.
submit_button = CTkButton(app, width=100, text="Submit", command=lambda: verify_code(code=code.get()))

app.after(500, matrix_animation)
app.mainloop()  # Mainloop keeping window persistent until "app.destroy()" is called.
