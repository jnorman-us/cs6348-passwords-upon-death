import os
import json
import quickstart

from forms import passwordsForm, loginForm
from handlers import PasswordsFormHandlers, LoginFormHandlers


password = None
salt = None
key = None

# FIRST FORM
# Get the user to login!

window = loginForm()
while True:
    event, values = window.read()
    if type(event) is tuple:
        command = event[0]
        if command == 'login':
            password, key, salt = LoginFormHandlers.login(event, values)
            window.close()
            break
    elif event in (None, 'Close'):
        break

print(password)
print(key)
print(salt)

passwords = []
if os.path.exists('localcopy.json'):
    with open('localcopy.json', 'r+') as file:
        passwords = json.load(file)

# SECOND FORM
# Allow the user to edit the passwords
window = passwordsForm(passwords)
while True:
    event, values = window.read()
    if type(event) is tuple:
        command = event[0]
        if command == 'add':
            passwords = PasswordsFormHandlers.add(event, values)
            window.close()
            window = passwordsForm(passwords)
        if command == 'delete':
            passwords = PasswordsFormHandlers.delete(event, values)
            window.close()
            window = passwordsForm(passwords)
        if command == 'save':
            passwords = PasswordsFormHandlers.save(event, values)
            window.close()
            window = passwordsForm(passwords)
    elif event in (None, 'Close'):
        break

window.close()
