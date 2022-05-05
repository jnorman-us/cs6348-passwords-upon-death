import os
import json
import env
import oauth

from forms import passwordsForm, loginForm, shamirPage, errorPage
from titles import PASSWORD_FORM_TITLE, LOGIN_FORM_TITLE, SHAMIR_PAGE_TITLE
from handlers import PasswordsFormHandlers, LoginFormHandlers, ShamirPageHandlers

# first step, get oauth token
oauth.getAuth()

# first window to open
window = loginForm()
while True:
    event, values = window.read()
    if event in (None, 'Close'):
        break
    elif type(event) is tuple:
        command = event[0]
        try:
            # LOGIN FORM ACTIONS
            if window.Title == LOGIN_FORM_TITLE():
                if command == 'login':
                    LoginFormHandlers.login(event, values)
                    window.close()
                    window = passwordsForm()
            # PASSWORD FORM ACTIONS
            elif window.Title == PASSWORD_FORM_TITLE():
                if command == 'add':
                    PasswordsFormHandlers.add(event, values)
                    window.close()
                    window = passwordsForm()
                elif command == 'delete':
                    PasswordsFormHandlers.delete(event, values)
                    window.close()
                    window = passwordsForm()
                elif command == 'save':
                    PasswordsFormHandlers.save(event, values)
                    window.close()
                    window = passwordsForm()
                elif command == 'shamir':
                    window.close()
                    window = shamirPage()
            # SHAMIR FORM ACTIONS
            elif window.Title == SHAMIR_PAGE_TITLE():
                if command == 'passwords':
                    window.close()
                    window = passwordsForm()
                elif command == 'generate':
                    hamirPageHandlers.generate(event, values)
                    window.close()
                    window = shamirPage()
                elif command == 'email':
                    ShamirPageHandlers.email(event, values)
        except Exception as e:
            print(e)
            window.close()
            window = errorPage(str(e))

oauth.remove_file_encf()
oauth.remove_file_decf()
env.unset('PWD')
env.unset('SALT')

window.close()
