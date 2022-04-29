class PasswordsFile:
	def __init__(self, salt, nonce, gcm_tag, encrypted_passwords):
		self.salt = salt
		self.nonce = nonce
		self.gcm_tag = gcm_tag
		self.encrypted_passwords = encrypted_passwords

	def __init__()





	def generateKey(): 

	# write the contents of the PasswordsFile instance
	# to the specified file
	def writeToFile(file_name):
		with open(file_name, 'r+') as file:
			file.seek(0)
			file.write(
				'test' 
			)
			file.truncate()

	def setPasswords(passwords):
		self.passwords = passwords

	def generateHmacPortion():
		pass

	def generateHmac(hmac_portion):

		pass



def loadFromFile(file_name, key):
	file = open(file_name, 'r')

	file.close()

