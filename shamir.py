import re
import random

from binascii import hexlify, unhexlify
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
	
# DECONSTRUCT splits the key into n shares, allowing it to 
# be rebuilt with just t out of n shares. Returns the printable
# contents rather than byte arrays
def deconstruct(key, t, n):
	shares = Shamir.split(t, n, key)
	return shares


def construct(shares):
	key = Shamir.combine(shares)
	return key

def printShares(shares):
	print("--- %d Shamir Shares ---" % len(shares))	
	for idx, share in shares:
		print("Share %d: %s" % (idx, hexlify(share)))

def sanitizeShareInput(line):
	pass


def testCreateShares():
	print('I am going to give you the shamir shares!!!')

	t = 3
	n = 5
	key = get_random_bytes(16)
	print('The key is', hexlify(key))

	shares = deconstruct(key, t, n)
	printShares(shares)

	shares_subset = random.sample(shares, t)
	shares_subset.sort(key=lambda x: x[0])
	print('Random t=%d shares' % (t))
	printShares(shares_subset)

def testUseShares():
	print('Enter the split key as user input! When done, type "done"')

	shares = []
	while True:
		line = input('Enter <index>,<share>: ')
		if line == 'done':
			break
		idx, share = re.split(r'\s*\,\s*', line)
		shares.append((int(idx), unhexlify(share)))
	printShares(shares)
	key = construct(shares)
	print('Here\'s the key! %s' % hexlify(key))


if __name__ == '__main__':
	testCreateShares()
	testUseShares()
