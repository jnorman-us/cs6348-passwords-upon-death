import json
import env

import aes
import oauth

from utils import emptyArrayOf

# not a real class, just organization
class PasswordsFormHandlers:
	@staticmethod
	def add(event, values):
		passwords = []

		for i in range(int(len(values) / 3)):
			passwords.append({
				'site': values[('site', i)],	
				'username': values[('username', i)],
				'password': values[('password', i)],
			})

		passwords.append({
			'site': '',	
			'username': '',
			'password': '',
		})
		aes.writePasswords(passwords)

	@staticmethod
	def delete(event, values):
		delete_id = event[1]
		passwords = []

		for i in range(int(len(values) / 3)):
			if i is not delete_id:
				passwords.append({
					'site': values[('site', i)],	
					'username': values[('username', i)],
					'password': values[('password', i)],
				})
		aes.writePasswords(passwords)

	@staticmethod
	def save(event, values):
		passwords = []

		for i in range(int(len(values) / 3)):
			passwords.append({
				'site': values[('site', i)],	
				'username': values[('username', i)],
				'password': values[('password', i)],
			})
		aes.writePasswords(passwords)
		aes.encryptFile()
		oauth.upload_file()	

class LoginFormHandlers:
	@staticmethod
	def login(event, values):
		password = values['password']
		aes.updateFilePassword(password)

		if oauth.download_file():
			try:
				aes.decryptFile()
			except Exception as e:
				print(e)
				raise Exception('Failed to decrypt!')
		else:
			success = oauth.create_folder()
			success = success and oauth.create_file()
			if success:
				aes.saltGen()
				env.set('DECF', 'outputs/download.dec')
				aes.writePasswords([])
			else:
				raise Exception('Failed to create Google Files')

class ShamirFormHandlers:
	@staticmethod
	def add(event, values):
		shares = []
		for key, value in values.items():
			if type(key) is tuple and key[0] == 'share':
				shares.append(value)

		shares.append('')
		env.set('INPUT_SHARES', json.dumps(shares))

	@staticmethod
	def delete(event, values):
		delete_id = event[1]
		shares = []
		for key, value in values.items():
			if type(key) is tuple and key[0] == 'share' and key[1] != delete_id:
				shares.append(value)
		env.set('INPUT_SHARES', json.dumps(shares))

	@staticmethod
	def combine(event, values):
		shares = []
		for key, value in values.items():
			if type(key) is tuple and key[0] == 'share':
				shares.append(value)
		env.set('INPUT_SHARES', json.dumps(shares))
		key = aes.shamirCombine(shares)

		if oauth.download_file():
			try:
				aes.decryptWithShamir(key)
			except:
				raise Exception('Failed to decrypt!')
		else:
			raise Exception('Google File does not exist')

class ShamirPageHandlers:
	@staticmethod
	def generate(event, values):
		k = values['k']
		n = values['n']
		env.set('K', k)
		env.set('N', n)
		aes.shamirCreate()
		env.set('RECEIVERS', json.dumps(emptyArrayOf(int(n))))

	@staticmethod
	def email(event, values):
		n = int(env.get('N'))
		recipients = []
		for i in range(n):
			share_i = i + 1
			recipients.append(values[('share', share_i)])
		print(recipients)
		env.set('RECEIVERS', json.dumps(recipients))
		oauth.share_gfile()
		oauth.send_shamir()
