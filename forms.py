import PySimpleGUI as sg
import env
import aes
import json

from utils import emptyArrayOf

import titles

sg.theme('HotDogStand')
size = (20, 1)

def passwordsForm():
	passwords = aes.getPasswords()

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
			sg.Button('Shamir', key=('shamir', None)),
			sg.Button('Change Password', key=('changePassword', None)) #added here
		],
	]

	return sg.Window(titles.PASSWORD_FORM(), layout, finalize=True)

def passwordsPage():
	passwords = aes.getPasswords()
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
			sg.InputText(default_text=site, size=size, disabled=True),
			sg.InputText(default_text=username, size=size, disabled=True),
			sg.InputText(default_text=password, size=size, disabled=True),
		])

	layout = [
		[sg.Text('View the Deceased\'s Passwords')],
		[sg.Column(
			password_columns,
		)],
		[
			sg.Button('Press F'),
		],
	]
	return sg.Window(titles.PASSWORD_PAGE(), layout, finalize=True)

def changePwForm():
	layout = [
		[sg.Text('Change Password')],
		[sg.Text('New Password'), sg.InputText(key='password')],
		[
			sg.Button('Submit', key=('changePassword', None))	
		],
	]
	return sg.Window(titles.CHANGE_PW_FORM(), layout, finalize=True)


def loginForm():
	layout = [
		[sg.Text('Login')],
		[sg.Text('Password'), sg.InputText(key='password')],
		[
			sg.Button('Submit', key=('login', None)),
			sg.Button('Use Shamir Keys', key=('shamir', None))
		],
	]
	return sg.Window(titles.LOGIN_FORM(), layout, finalize=True)

def shamirForm():
	try:
		shares = json.loads(env.get('INPUT_SHARES'))
	except:
		shares = []
		env.set('INPUT_SHARES', json.dumps(shares))

	share_columns = []
	share_columns.append([
		sg.Text('Share', (45, 1)),
	])
	for i in range(len(shares)):
		share = shares[i]
		share_columns.append([
			sg.InputText(key=('share', i), size=(45, 1), default_text=share),
			sg.Button('Delete', key=('delete', i))
		])

	layout = [
		[sg.Text('Combine Shamir Shares')],
		[sg.Column(
			share_columns,
		)],
		[
			sg.Button('Back to Login', key=('login', None)),
			sg.Button('Add', key=('add', None)),
			sg.Button('Combine', key=('combine', None)),
		],
	]
	return sg.Window(titles.SHAMIR_FORM(), layout, finalize=True)


def shamirPage():
	if env.get('K') is not None and env.get('N') is not None:
		k = int(env.get('K'))
		n = int(env.get('N'))
	else:
		k = 0
		n = 0
		env.set('K', str(0))
		env.set('N', str(0))

	try:
		shares = json.loads(env.get('SHARES'))
		receivers = json.loads(env.get('RECEIVERS'))
		if len(shares) != len(receivers) and len(shares) != n:
			raise Exception('mismatched')
	except:
		shares = []
		receivers = []
		env.set('SHARES', json.dumps(shares))
		env.set('RECEIVERS', json.dumps(receivers))

	share_columns = []
	share_columns.append([
		sg.Text('Index', size=(5, 1)),
		sg.Text('Share', size=(45, 1)),
		sg.Text('Recipient Email', size=(25, 1))
	])
	for i in range(len(shares)):
		share = shares[i]
		receiver = receivers[i]
		share_i = i + 1
		share_columns.append([
			sg.Text(share_i, size=(5, 1)),
			sg.Text(share, size=(45, 1)),
			sg.InputText(key=('share', share_i), size=(25, 1), default_text=receiver)
		])
	layout = [
		[sg.Text('View Shamir Secrets')],
		[sg.Text('k'), sg.InputText(key='k', default_text=k)],
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
	return sg.Window(titles.SHAMIR_PAGE(), layout, finalize=True)

def errorPage(error):
	layout = [
		[sg.Text('ERROR!')],
		[sg.Text(error)],
	]
	return sg.Window(titles.ERROR_PAGE(), layout, finalize=True)