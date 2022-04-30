import json

from aes import keyGen

file_name = "localcopy.json"
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

		return passwords

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
		return passwords

	@staticmethod
	def save(event, values):
		passwords = []

		for i in range(int(len(values) / 3)):
			passwords.append({
				'site': values[('site', i)],	
				'username': values[('username', i)],
				'password': values[('password', i)],
			})

		with open(file_name, 'w+') as file:
			file.seek(0)
			json.dump(passwords, file)
			file.truncate()

		return passwords

class LoginFormHandlers:
	@staticmethod
	def login(event, values):
		password = values['password']
		key, salt = keyGen(password)
		return password, key, salt

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
