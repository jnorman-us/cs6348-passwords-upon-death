import PySimpleGUI as sg
import quickstart


size = (20, 1)
password_rows = 0
deleted_rows = []

def newPasswordLine(id):
    return [
        sg.InputText(key=('row-site', id), size=size),
        sg.InputText(key=('row-username', id), size=size),
        sg.InputText(key=('row-password', id), size=size),
        sg.Button('Delete Row', key=('row-delete', id))
    ]

def removeRow(id):
    keys = ['row-site', 'row-password', 'row-username', 'row-delete']
    for key in keys:
        element = window[(key, id)]
        element.update(visible=False)
        element = None
    deleted_rows.append(id)

sg.theme('Black')
layout = [
    [sg.Text('File authentication')],
    [sg.Text('Enter password: '), sg.InputText(key='pwd'), sg.Button('Enter')],
    [sg.Column([
        [
            sg.Text('Site:', size=size), 
            sg.Text('Username:', size=size),
            sg.Text('Password:', size=size)
        ],
        newPasswordLine(password_rows),
    ], key="Passwords Column")],
    [sg.Button('Add Password')],
    [sg.Button('Submit'), sg.Button('Close')],
]
window = sg.Window('Passwords upon death', layout, finalize=False)

while True:
    event, values = window.read()
    if type(event) is tuple:
        if event[0] in ('row-delete'):
            id = event[1]
            print('Delete', id)
            removeRow(id)
    else:
        if event in (None, 'Close'):
            break
        if event in ('Enter'):
            print('Entered password:')
            print(values['pwd'])
        if event in ('Submit'):
            print(values)
            # quickstart.createFile(values['fileContent']) #create file in drive
        if event in ('Add Password'):
            password_rows = password_rows + 1
            passwords_column = window['Passwords Column']
            window.extend_layout(passwords_column, [newPasswordLine(password_rows)])

window.close()
