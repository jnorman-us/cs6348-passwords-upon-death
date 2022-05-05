import json
import env

import aes
import oauth

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



class ShamirPageHandlers:
	@staticmethod
	def generate(event, values):
		try:
			t = int(values['t'])
			n = int(values['n'])
		except:
			return (0, 0, [])

		print('GENERATING %d SHARES, %d to reconstruct' % (n, t))

		return (t, n, [
			'share 1',
			'share 2',
			'share 3',
		])

	@staticmethod
	def email(event, values, shares):
		print('Emailing...')
		print(shares)
