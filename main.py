from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '$', '%', '&', '(', ')', '*', '+', '#']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()
    new_data = {
        website_data: {
            "email": email_data,
            "password": password_data,
        }
    }

    if len(website_data) == 0 or len(password_data) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", 'r') as saved_data:
                #Reading old data
                data = json.load(saved_data)
        except FileNotFoundError:
            with open('data.json', "w") as saved_data:
                json.dump(new_data, saved_data, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as saved_data:
                #Saving updated data
                json.dump(data, saved_data, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# --------------------------- Search password -------------------------#
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exits.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

#Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1)
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2)
email_entry.insert(0, "audranwolfhards@gmail.com")
password_entry = Entry(width=31)
password_entry.grid(column=1, row=3)

#Buttons
generatePassword_button = Button(text="Generate Password", command=generate_password)
generatePassword_button.grid(column=2, row=3)
Add_button = Button(text="Add", width=36, command=save)
Add_button.grid(column=1, row=4, columnspan=1)

#Search button
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2)

canvas = Canvas(width=200, height=200)
locker_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_image)
canvas.grid(column=1, row=0)

window.mainloop()
