from dotenv import set_key, unset_key, get_key

file_name = 'persist.env'

def get(key):
	return get_key(file_name, key)

def set(key, value):
	return set_key(file_name, key, value)

def unset(key):
	return unset_key(file_name, key)