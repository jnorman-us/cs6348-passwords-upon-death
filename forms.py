import PySimpleGUI as sg

sg.theme('black')
size = (20, 1)
def passwordsForm(passwords):
	password_columns = []
	password_columns.append([
		sg.Text('Site:', size=size), 
        sg.Text('Username:', size=size),
        sg.Text('Password:', size=size)
	])
	for id in range(len(passwords)):
		data = passwords[id]
		site = data['site']
		username = data['username']
		password = data['password']
		password_columns.append([
			sg.InputText(key=('site', id), size=size, default_text=site),
			sg.InputText(key=('username', id), size=size, default_text=username),
			sg.InputText(key=('password', id), size=size, default_text=password),
			sg.Button('Delete', key=('delete', id))
		])

	layout = [
		[sg.Text('Edit Passwords')],
		[sg.Column(
			password_columns
		)],
		[sg.Button('Add', key=('add', None)), sg.Button('Save', key=('save', None))]
	]

	return sg.Window('PUD - Edit Passwords', layout, finalize=True)

def loginForm():
	layout = [
		[sg.Text('Login')],
		[sg.Text('Password'), sg.InputText(key='password')],
		[sg.Button('Submit', key=('login', None))],
	]
	return sg.Window('PUD - Login', layout, finalize=True)