import os
import json
import env
import oauth
import traceback
import titles

from forms import passwordsForm, loginForm, shamirPage, errorPage, shamirForm, passwordsPage, changePwForm
from handlers import PasswordsFormHandlers, LoginFormHandlers, ShamirPageHandlers, ShamirFormHandlers, ChangePwFormHandlers

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
            if window.Title == titles.LOGIN_FORM():
                if command == 'login':
                    LoginFormHandlers.login(event, values)
                    window.close()
                    window = passwordsForm()
                elif command == 'shamir':
                    window.close()
                    window = shamirForm()
            # PASSWORD FORM ACTIONS
            elif window.Title == titles.PASSWORD_FORM():
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
                elif command == 'changePassword': 
                    window.close
                    window = changePwForm()

            # CHANGE PASSWORD FORM ACTIONS
            elif window.Title == titles.CHANGE_PW_FORM():
                if command == 'changePassword':
                    ChangePwFormHandlers.change(event, values)
                    window.close()
                    window = passwordsForm() #must press save again after you change the password
                    
            # SHAMIR PAGE ACTIONS
            elif window.Title == titles.SHAMIR_PAGE():
                if command == 'passwords':
                    window.close()
                    window = passwordsForm()
                elif command == 'generate':
                    ShamirPageHandlers.generate(event, values)
                    window.close()
                    window = shamirPage()
                elif command == 'email':
                    ShamirPageHandlers.email(event, values)
            # SHAMIR FORM ACTIONS
            elif window.Title == titles.SHAMIR_FORM():
                if command == 'login':
                    window.close()
                    window = loginForm()
                elif command == 'add':
                    ShamirFormHandlers.add(event, values)
                    window.close()
                    window = shamirForm()
                elif command == 'delete':
                    ShamirFormHandlers.delete(event, values)
                    window.close()
                    window = shamirForm()
                elif command == 'combine':
                    ShamirFormHandlers.combine(event, values)
                    window.close()
                    window = passwordsPage()
        except Exception as e:
            traceback.print_exc()
            print(e)
            window.close()
            window = errorPage(str(e))

oauth.remove_file_encf()
oauth.remove_file_decf()
oauth.remove_token()
env.unset('PWD')
env.unset('SALT')
env.unset('SHARES')
env.unset('RECEIVERS')
env.unset('INPUT_SHARES')
env.unset('SENDER')
env.unset('K')
env.unset('N')

window.close()
