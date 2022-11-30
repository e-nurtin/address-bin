from tkinter import *
from tkinter import ttk
import re
import json
import os

info = {}
contacts = []
# Append all the names in our data file to see them in our list box if the file is not
# empty
try:
    if os.stat("address_book_data.json").st_size > 0:
        with open('address_book_data.json', 'r') as file_path:
            data = json.load(file_path)
        for name in data.keys():
            contacts.append(name)
except:
    with open('address_book_data.json', 'w') as file_path:
        file_path.write(json.dumps({}))


# Validate the mandatory information.
def valid_name(name):
    error_msg.set('')
    valid = re.match('([a-zA-Z]{2,}\s?)+', name)
    if valid:
        return True
    else:
        error_msg.set('Name must consist of at least 2 letters!')
        return False


def valid_zip(zip_code):
    error_msg.set('')
    valid = re.match('^[0-9]{4}', zip_code)
    if valid:
        return True
    else:
        error_msg.set('Zip code must be exactly 4 digits!')
        return False


def valid_phone(number):
    error_msg.set('')
    valid = re.match('^\+?[0-9]{7,15}$', number)
    if valid:
        return True
    else:
        error_msg.set('Phone number must be of 7 or more digits!')
        return False


# Check if the mandatory information is available and call the save function if True.
def validate_info(*args):
    entry_name = name_entry.get()
    code = zip_entry.get()
    phone = phone_entry.get()
    if valid_name(entry_name) and valid_zip(code) and valid_phone(phone):
        save_info(entry_name, code, phone)
        error_msg.set('Contact Saved!')
    else:
        error_msg.set('Name, Zip and Phone Number must be filled to save!')


# This function gathers all the info available and saves it to a json file.
def save_info(name, zip_code, phone):
    # Get the info of our new contact and clear the entries.
    info[name] = {}
    info[name]['zip code'] = zip_code
    info[name]['phone number'] = phone
    info[name]['address'] = address_entry.get()
    info[name]['town'] = town_entry.get()
    info[name]['country'] = country_entry.get()
    info[name]['email'] = email_entry.get()

    # Check if the file has any items in it in order to bypass json error,
    # if so open the file as write and add the first item.
    if os.stat("address_book_data.json").st_size == 0:
        with open('address_book_data.json', 'w') as file_path:
            json.dump(info, file_path, indent=2)

    else:
        # Appending the new contact's info and saving it to the json file.
        with open('address_book_data.json', 'r') as file_path:
            data = json.load(file_path)

        data |= info

        with open('address_book_data.json', 'w') as file_path:
            json.dump(data, file_path, indent=2)

    contacts.append(name)
    list_box_var.set(contacts)
    clear_entries()


# When a contact is clicked in the listbox this function puts all the info on the screen
def show_info(*args):
    if contacts:
        contact = contacts[list_box.curselection()[0]]
        with open('address_book_data.json', 'r') as file:
            data = json.load(file)
        name.set(f"Name: {contact}")
        address.set(f"Address: {data[contact]['address']}")
        town.set(f'Town: {data[contact]["town"]}')
        country.set(f'Country: {data[contact]["country"]}')
        zip_code.set(f'Zip code: {data[contact]["zip code"]}')
        email.set(f'Email: {data[contact]["email"]}')
        phone_number.set(f'Phone Number: {data[contact]["phone number"]}')


# Deletes a contact from the address book if the remove button is pressed
def delete_contact():
    if contacts:
        name = contacts[list_box.curselection()[0]]
        with open('address_book_data.json', 'r') as file:
            data = json.load(file)
        if name in data:
            del data[name]
        with open('address_book_data.json', 'w') as file:
            json.dump(data, file, indent=2)
        contacts.remove(name)
        list_box_var.set(contacts)


def edit_contact():
    if contacts:
        contact = contacts[list_box.curselection()[0]]
        with open('address_book_data.json', 'r') as file:
            data = json.load(file)
        name_entry.insert(0, contact)
        address_entry.insert(0, data[contact]['address'])
        town_entry.insert(0, data[contact]["town"])
        country_entry.insert(0, data[contact]["country"])
        zip_entry.insert(0, data[contact]["zip code"])
        email_entry.insert(0, data[contact]["email"])
        phone_entry.insert(0, data[contact]["phone number"])
        del data[contact]
        contacts.remove(contact)
        list_box_var.set(contacts)


# Copy the information to clipboard if copy button is pressed
def copy_contact():
    clipboard_msg = ''

    clipboard_msg += f'{name.get()}\n{address.get()}\n{town.get()}\n{country.get()}\n' \
                     f'{zip_code.get()}\n{email.get()}\n{phone_number.get()}'
    root.clipboard_clear()
    root.clipboard_append(clipboard_msg)


# This function clears all the entries after making sure they are entry widgets.
def clear_entries(*args):
    for widget in entry_frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            widget.delete(0, 'end')
    error_msg.set('')


root = Tk()
root.minsize(660, 350)
root.title('Address Book')
root.iconbitmap('address-book.ico')
content = ttk.Frame(root, padding=(3, 3, 12, 12), relief='sunken')
content.grid(column=0, row=0, sticky=(N, S, E, W))
error_msg = StringVar()

# Define Entry Frame widgets
entry_frame = ttk.Frame(content, borderwidth=5, relief='sunken')
name_wrapper = (entry_frame.register(valid_name), '%P')
name_entry = ttk.Entry(entry_frame, width=20, validate='focusout',
                       validatecommand=name_wrapper)
name_lbl = ttk.Label(entry_frame, text='Name:', anchor='n')

address_entry = ttk.Entry(entry_frame, width=25)
address_lbl = ttk.Label(entry_frame, text='Address:')

town_entry = ttk.Entry(entry_frame, width=20)
town_lbl = ttk.Label(entry_frame, text='Town:')

country_entry = ttk.Entry(entry_frame, width=15)
country_lbl = ttk.Label(entry_frame, text='Country:')

zip_wrapper = (entry_frame.register(valid_zip), '%P')
zip_entry = ttk.Entry(entry_frame, width=8, validate='focusout',
                      validatecommand=zip_wrapper)
zip_lbl = ttk.Label(entry_frame, text='Zip Code:')

email_entry = ttk.Entry(entry_frame, width=20)
email_lbl = ttk.Label(entry_frame, text='Email address:')

phone_wrapper = (entry_frame.register(valid_phone), '%P')
phone_entry = ttk.Entry(entry_frame, width=20, validate='focusout',
                        validatecommand=phone_wrapper)
phone_lbl = ttk.Label(entry_frame, text='Phone Number:')

save_button = ttk.Button(entry_frame, text='Save', command=validate_info,
                         default='active')
clear_button = ttk.Button(entry_frame, text='Clear', command=clear_entries)

exit_button = ttk.Button(entry_frame, text='Exit Program', command=quit)

error_lbl = ttk.Label(entry_frame, textvariable=error_msg, foreground='red')

# Grids for the Entry frame. Place all the widgets on their place on the window.
entry_frame.grid(rowspan=2, columnspan=2, row=0, column=0, sticky=(N, W, S, E))

name_entry.grid(row=1, column=1, sticky=W)
name_lbl.grid(row=1, column=0, sticky=E)
address_entry.grid(row=2, column=1, sticky=W)
address_lbl.grid(row=2, column=0, sticky=E)
town_entry.grid(row=3, column=1, sticky=W)
town_lbl.grid(row=3, column=0, sticky=E)
country_entry.grid(row=4, column=1, sticky=W)
country_lbl.grid(row=4, column=0, sticky=E)
zip_entry.grid(row=5, column=1, sticky=W)
zip_lbl.grid(row=5, column=0, sticky=E)
email_entry.grid(row=6, column=1, sticky=W)
email_lbl.grid(row=6, column=0, sticky=E)
phone_entry.grid(row=7, column=1, sticky=W)
phone_lbl.grid(row=7, column=0, sticky=E)
save_button.grid(row=12, column=0, sticky=W)
clear_button.grid(row=12, column=1, sticky=W)
error_lbl.grid(row=10, column=0, columnspan=3, sticky=E)
exit_button.grid(row=14, column=3, sticky=(S, E))

for widget in entry_frame.winfo_children():
    widget.grid_configure(padx=5, pady=5)

# Define Listbox frame widgets
lb_frame = ttk.Frame(content, borderwidth=5, padding=(3, 3, 7, 7))

list_box_var = StringVar(value=contacts)
list_box = Listbox(lb_frame, height=10, listvariable=list_box_var, width=30)

scrollbar = ttk.Scrollbar(lb_frame)

edit_button = ttk.Button(lb_frame, text='Edit', command=edit_contact)
copy_button = ttk.Button(lb_frame, text='Copy', command=copy_contact)
remove_button = ttk.Button(lb_frame, text='Remove', command=delete_contact)

# Grids for Listbox frame
lb_frame.grid(row=0, column=2, columnspan=3, sticky=(E, W, S, N))
list_box.grid(columnspan=3, rowspan=5, row=0, column=0, sticky=(N, W, E, S))
scrollbar.grid(columnspan=3, rowspan=5, row=0, column=0, sticky=(N, E, S))

edit_button.grid(row=0, column=5, sticky=(W, E))
copy_button.grid(row=1, column=5, sticky=(W, E))
remove_button.grid(row=2, column=5, sticky=(W, E))

# Define information frame widgets
info_frame = ttk.Frame(content, borderwidth=5)

name = StringVar()
address = StringVar()
town = StringVar()
country = StringVar()
zip_code = StringVar()
email = StringVar()
phone_number = StringVar()

name_info = ttk.Label(info_frame, textvariable=name)
address_info = ttk.Label(info_frame, textvariable=address)
town_info = ttk.Label(info_frame, textvariable=town)
country_info = ttk.Label(info_frame, textvariable=country)
zip_info = ttk.Label(info_frame, textvariable=zip_code)
email_info = ttk.Label(info_frame, textvariable=email)
phone_info = ttk.Label(info_frame, textvariable=phone_number)


# Grids for information frame
info_frame.grid(row=1, column=2, columnspan=3, sticky=(E, W, S, N))
name_info.grid(row=0, column=0, sticky=(N, W))
address_info.grid(row=1, column=0, sticky=W)
town_info.grid(row=2, column=0, sticky=W)
country_info.grid(row=3, column=0, sticky=W)
zip_info.grid(row=4, column=0, sticky=W)
email_info.grid(row=5, column=0, sticky=W)
phone_info.grid(row=6, column=0, sticky=W)


# Make the widgets grow if the window is resized
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)
content.columnconfigure(2, weight=3)
content.rowconfigure(1, weight=1)
entry_frame.rowconfigure(14, weight=1)
entry_frame.columnconfigure(3, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(2, weight=1)

list_box.bind('<<ListboxSelect>>', show_info)
save_button.bind('<Return>', validate_info)
root.mainloop()
