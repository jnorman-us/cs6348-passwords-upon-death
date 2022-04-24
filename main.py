import PySimpleGUI as sg
import quickstart

sg.theme('Black')
layout = [  [sg.Text('File authentication')],
            [sg.Text('Enter password: '), sg.InputText(key='pwd'), sg.Button('Enter')],
            [sg.Multiline(size=(30, 5), key='fileContent')],
            [sg.Button('Submit'), sg.Button('Close')]]

window = sg.Window('Passwords upon death', layout, finalize=True)

while True:
    event, values = window.read()
    if event in (None, 'Close'):
        break
    if event in ('Enter'):
        print('Entered password:')
        print(values['pwd'])
    if event in ('Submit'):
        print('You entered in the fileContent:')
        print(values['fileContent'])
        quickstart.createFile() 

window.close()
