import PySimpleGUI as sg

from titles import PASSWORD_FORM_TITLE, LOGIN_FORM_TITLE, SHAMIR_PAGE_TITLE

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
		[
			sg.Button('Add', key=('add', None)), 
			sg.Button('Save', key=('save', None)), 
			sg.Button('Shamir', key=('shamir', None))
		],
	]

	return sg.Window(PASSWORD_FORM_TITLE(), layout, finalize=True)

def loginForm():
	layout = [
		[sg.Text('Login')],
		[sg.Text('Password'), sg.InputText(key='password')],
		[sg.Button('Submit', key=('login', None))],
	]
	return sg.Window(LOGIN_FORM_TITLE(), layout, finalize=True)

def shamirPage(t, n, shares):
	share_columns = []
	share_columns.append([
		sg.Text('Index', size=size),
		sg.Text('Share', size=size),
	])
	for i in range(len(shares)):
		share = shares[i]
		share_columns.append([
			sg.Text(i + 1, size=size),
			sg.Text(share, size=size),
		])
	layout = [
		[sg.Text('View Shamir Secrets')],
		[sg.Text('t'), sg.InputText(key='t', default_text=t)],
		[sg.Text('n'), sg.InputText(key='n', default_text=n)],
		[sg.Button('Generate', key=('generate', None))],
		[sg.Column(
			share_columns,
		)],
		[
			sg.Button('Edit Passwords', key=('passwords', None)),
			sg.Button('Email', key=('email', None)),
		],
	]
	return sg.Window(SHAMIR_PAGE_TITLE(), layout, finalize=True)