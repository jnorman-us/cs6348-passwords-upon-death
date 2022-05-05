import os
import json
import quickstart
from dotenv import get_key, set_key, unset_key

from forms import passwordsForm, loginForm, shamirPage
from titles import PASSWORD_FORM_TITLE, LOGIN_FORM_TITLE, SHAMIR_PAGE_TITLE
from handlers import PasswordsFormHandlers, LoginFormHandlers, ShamirPageHandlers

passwords = []
if os.path.exists('localcopy.json'):
    with open('localcopy.json', 'r+') as file:
        passwords = json.load(file)

# first window to open
window = loginForm()
while True:
    event, values = window.read()
    if event in (None, 'Close'):
        break
    elif type(event) is tuple:
        command = event[0]
        # LOGIN FORM ACTIONS
        if window.Title == LOGIN_FORM_TITLE():
            if command == 'login':
                password, key, salt = LoginFormHandlers.login(event, values)
                window.close()
                window = passwordsForm(passwords)
        # PASSWORD FORM ACTIONS
        elif window.Title == PASSWORD_FORM_TITLE():
            if command == 'add':
                passwords = PasswordsFormHandlers.add(event, values)
                window.close()
                window = passwordsForm(passwords)
            elif command == 'delete':
                passwords = PasswordsFormHandlers.delete(event, values)
                window.close()
                window = passwordsForm(passwords)
            elif command == 'save':
                passwords = PasswordsFormHandlers.save(event, values)
                window.close()
                window = passwordsForm(passwords)
            elif command == 'shamir':
                window.close()
                window = shamirPage(shamir_t, shamir_n, shares)
        # SHAMIR FORM ACTIONS
        elif window.Title == SHAMIR_PAGE_TITLE():
            if command == 'passwords':
                window.close()
                window = passwordsForm(passwords)
            elif command == 'generate':
                shamir_t, shamir_n, shares = ShamirPageHandlers.generate(event, values)
                window.close()
                window = shamirPage(shamir_t, shamir_n, shares)
            elif command == 'email':
                ShamirPageHandlers.email(event, values, shares)
        # CHANGE PASSWORD ACTIONS

    # unset env vars before closing
    unset_key("persist.env", "SALT")
    unset_key("persist.env", "PWD")
    unset_key("persist.env", "DECF")
    unset_key("persist.env", "ENCF")
window.close()
