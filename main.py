from customtkinter import *
from twoFA.setup2FA import verify_2FA_code
from Cryptography.crypto import *
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip, json

set_appearance_mode("dark")  # Setting application mode to dark.
set_default_color_theme("green")  # Setting application theme to green.

app = CTk()  # Creating CTk window for application.
app.title("2FA")  # Adding a title for the application window.
app.geometry("360x180")  # Sets applications dimensions.


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
            with open("Bit-Safe/data.json") as data_dict:
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
            with open("Bit-Safe/data.json") as data_dict:
                data = json.load(data_dict)
        except FileNotFoundError:  # If 'FileNotFoundError' occurs error message box appears.
            messagebox.showinfo(title="Error", message="Error: File not found.")
        else:  # Takes a list of website keys from the Bit-Safe and displays websites on screen.
            websites = list(data.keys())  # Bug occurred when displaying 'websites' in message box, so reformatting was necessary.
            formatted_websites = '{}'.format(websites)
            messagebox.showinfo(title="List of Websites", message=formatted_websites)


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
                with open("Bit-Safe/data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:  # If 'FileNotFoundError' error occurs, 'Bit-Safe/data.json' is created.
                with open("Bit-Safe/data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)  # Updates 'data' with 'new_data' adding additional credentials in the process.
                with open("Bit-Safe/data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:  # Lastly, delete old 'website' and 'password' entry data.
                website_entry.delete(0, END)
                password_entry.delete(0, END)


    # Reformats app's window size, destroys old widgets, changes the window title, and adds padding around all widgets.
    app.geometry("600x800")
    two_factor_entry.destroy(), two_factor_label.destroy(), submit_button.destroy()
    app.title("Password Manager")
    app.config(padx=50, pady=50)

    # Loads image and places the logo at the top center of the screen.
    logo = PhotoImage(file="Bit-Safe/logo.png")
    logo_img = CTkLabel(app, image=logo, text="")
    logo_img.grid(row=0, column=0, columnspan=2)

    # Creating and placing website label.
    website_label = CTkLabel(app, text="Website:")
    website_label.grid(row=1, column=0, padx=5, pady=5)

    # Creating and placing website entry field.
    website_entry = CTkEntry(app, width=175, placeholder_text="Enter Website or Application Name")
    website_entry.grid(row=1, column=1, padx=5, pady=5)
    website_entry.focus()

    # Creating and placing search button. Button checks website field, if field corresponds to data file the username/email and password appear.
    search_button = CTkButton(app, text="Search", command=search)
    search_button.grid(row=4, column=0, padx=5, pady=5)

    # Creating and placing email/username label.
    email_username_label = CTkLabel(app, text="Email/Username:")
    email_username_label.grid(row=2, column=0, padx=5, pady=5)

    # Creating and placing email/username entry field.
    email_username_entry = CTkEntry(app, width=175, placeholder_text="Enter Email or Username")
    email_username_entry.grid(row=2, column=1, padx=5, pady=5)
    email_username_entry.insert(0, "spitzerlucas25@gmail.com")

    # Creating and placing password label.
    password_label = CTkLabel(app, text="Password:")
    password_label.grid(row=3, column=0, padx=5, pady=5)

    # Creating and placing password entry field.
    password_entry = CTkEntry(app, width=175, placeholder_text="Enter or Generate Password")
    password_entry.grid(row=3, column=1, padx=5, pady=5)

    # Creating and placing generate button. Button generates a random password of letters, numbers, and symbols.
    generate_button = CTkButton(app, text="Generate Password", command=generate_password)
    generate_button.grid(row=4, column=1, padx=5, pady=5)

    # Creating and placing list button. Button lists the websites which have data stored in the Bit-Safe.
    list_button = CTkButton(app, text="List Websites", command=list_websites)
    list_button.grid(row=5, column=0, padx=5, pady=15)

    # Creating and placing add button. Button saves credentials active in the app to the Bit-Safe.
    add_button = CTkButton(app, text="Add Credentials", command=save)
    add_button.grid(row=5, column=1, padx=5, pady=15)


# Creating label and placing label in the center.
two_factor_label = CTkLabel(app, font=("Roboto", 24, "normal"), text="Enter Code:")
two_factor_label.place(relx=0.5, rely=0.25, anchor=CENTER)

# Creating variable and entry placing entry in the center.
code = StringVar(app, value="")
two_factor_entry = CTkEntry(app, width=80, height=35, textvariable=code, font=("Roboto", 20, "normal"))
two_factor_entry.place(relx=0.5, rely=0.5, anchor=CENTER)

# Submit button used to call "verify_code()" after entering verification code.
submit_button = CTkButton(app, width=100, text="Submit", command=lambda: verify_code(code=code.get()))
submit_button.place(relx=0.5, rely=0.75, anchor=CENTER)

app.mainloop()  # Mainloop keeping window persistent until "app.destroy()" is called.