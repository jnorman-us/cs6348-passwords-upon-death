'''

Module for AES, Shamir, and HMAC methods
Key generation, regeneration, file encryption
and decryption.

Individual methods outlined below.

'''


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Protocol.SecretSharing import Shamir
import json
from base64 import b64encode
from base64 import b64decode
from Crypto.Hash import HMAC, SHA256
from dotenv import dotenv_values, set_key, unset_key, get_key
import os


''' hmacGen creates an HMAC digest from the local encrypted
    file before storing to google drive.  The digest is
    stored in the local .env for verification. The HMAC
    function requires a "secret" which is a randomly generated
    byte-string each time we generate a new digest
'''


def hmacGen():
    encf = get_key("persist.env", "ENCF")
    f = open(encf, 'rb')
    msg = f.read()
    secret = get_random_bytes(16)
    set_key("persist.env", "SECRET", secret.hex())
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(msg)
    f.close()
    set_key("persist.env", "HMAC", h.hexdigest())
    return


''' hmacVerify loads a stored secret and hmac digest
    from the local .env file and verifies if a downloaded
    encrypted file is unmodified since last local use
'''

def hmacVerify():
    encf = get_key("persist.env", "ENCF")
    f = open(encf, 'rb')
    msg = f.read()
    secret = get_key("persist.env", "SECRET")
    hmac = get_key("persist.env", "HMAC")
    h = HMAC.new(bytes.fromhex(secret), digestmod=SHA256)
    h.update(msg)
    try:
        h.hexverify(hmac)
        unset_key("persist.env", "SECRET")
        unset_key("persist.env", "HMAC")
        return 1
    except ValueError:
        '''TODO - allow user to delete file on drive? and re-upload'''
        return 0


''' reGenKey(salt) takes the salt from the
    stored encrypted file and regenerates the
    AES key using the user provided file password
'''

def reGenKey(salt):
    passw = get_key("persist.env", "PWD")
    password = passw.encode()
    key = scrypt(password, salt, 32, N=2 ** 20, r=8, p=1)
    return key


''' keyGenWithSalt generates an 256-bit key
    from the user provided file password upon
    login, and the current session saved salt
    For use in current session only
'''


def keyGenWithSalt():
    passw = get_key("persist.env", "PWD")
    salt = get_key("persist.env", "SALT")
    password = passw.encode()
    key = scrypt(password, salt, 32, N=2 ** 20, r=8, p=1)
    return key


''' keyGen() generates a 256-bit key
    from the user provided file password
    and a randomly generated 32-byte salt
'''


def keyGen():
    password = bytes.fromhex(get_key("persist.env", "PWD"))
    salt = get_random_bytes(32).hex()
    set_key("persist.env", "SALT", salt)
    key = scrypt(password, salt, 32, N=2 ** 20, r=8, p=1)
    return


''' shamirCreate() generates N keys where
    K keys are necessary to fetch the AES key
    K, N from .env; shares saved in list in .env 
'''


def shamirCreate():
    k = int(get_key("persist.env", "K"))
    n = int(get_key("persist.env", "N"))

    # get key from password and salt
    key = keyGenWithSalt()
    key1 = key[:16]
    key2 = key[16:]

    # create n shamir keys, where k is needed to unlock
    shares1 = Shamir.split(k, n, key1)
    shares2 = Shamir.split(k, n, key2)
    shares = []
    for i, ((idx1, sh1), (idx2, sh2)) in enumerate(zip(shares1, shares2)):
        bytestring = idx1.to_bytes(2, 'big')
        bytestring += sh1[0:16]
        bytestring += idx2.to_bytes(2, 'big')
        bytestring += sh2[0:16]
        shares.append(bytestring.hex())

    shares_string = ''
    for x in range(len(shares)):
        shares_string += shares[x]
        shares_string += " "
    set_key("persist.env", "SHARES", shares_string)
    return


''' shamirCombine(kshares) takes a list of shamir keys
    and regenerates the AES key.  The shared shamir keys
    contain a single hex string comprise of index1, share1, index2, 
    share2 for a mapping to the original AES key. 
'''


def shamirCombine(kshares):
    sh1 = []
    sh2 = []
    for y in range(len(kshares)):
        x = bytes.fromhex(kshares[y])
        idx1 = x[0:2]
        ksh1 = x[2:18]
        idx2 = x[18:20]
        ksh2 = x[20:36]
        sh1.append((int.from_bytes(idx1, 'big'), ksh1))
        sh2.append((int.from_bytes(idx2, 'big'), ksh2))
    key1 = Shamir.combine(sh1)
    key2 = Shamir.combine(sh2)
    key = key1 + key2
    return key


''' encryptFile() takes the plaintext filename from .env
    and encrypts it using AES-GCM with tags.  output file is 
    formatted in json. DECF (decrypted file) is removed from .env
    when done, and plaintext file is deleted from system.
'''


def encryptFile():
    infilename = str(get_key("persist.env", "DECF"))
    key = keyGenWithSalt()
    outfilename = infilename.split(".")[0] + ".enc"
    infile = open(infilename, 'rb')
    outfile = open(outfilename, 'w')
    cipher = AES.new(key, AES.MODE_GCM)
    data = infile.read()
    salt = bytes.fromhex(get_key("persist.env", "SALT"))
    cipher.update(salt)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [b64encode(x).decode('utf-8') for x in (cipher.nonce, salt, ciphertext, tag)]
    result = json.dumps(dict(zip(json_k, json_v)))
    outfile.write(result)
    infile.close()
    outfile.close()
    os.remove(infilename)
    unset_key("persist.env", "DECF")
    set_key("persist.env", "ENCF", outfilename)

    return


''' decryptWithShamir(key, encfilename) takes the regenerated AES key
    and decrypts a local file, with user provided filename
    returns the plaintext file name, and deletes the encrypted local file
'''


def decryptWithShamir(key, encfilename):
    encfile = open(encfilename, 'r')
    decfilename = encfilename.split(".")[0] + ".shared"
    decfile = open(decfilename, 'w')
    b64 = json.load(encfile)
    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = {k: b64decode(b64[k]) for k in json_k}

    cipher = AES.new(key, AES.MODE_GCM, nonce=json_v['nonce'])
    cipher.update(json_v['header'])
    plaintext = cipher.decrypt_and_verify(json_v['ciphertext'], json_v['tag'])
    alist = json.loads(plaintext)
    json.dump(alist, decfile)
    decfile.close()
    encfile.close()
    os.remove(encfilename)
    return decfilename


''' decryptFile() decrypts the locally downloaded file
    encrypted file name taken from .env
    user provides file password, and salt is read from the 
    encrypted download; encrypted file is deleted after processing
    and plaintext filename is stored in .env    
'''


def decryptFile():
    encfilename = get_key("persist.env", "ENCF")
    encfile = open(encfilename, 'r')
    decfilename = encfilename.split(".")[0] + ".dec"
    decfile = open(decfilename, 'w')
    b64 = json.load(encfile)
    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = {k: b64decode(b64[k]) for k in json_k}
    key = reGenKey(json_v['header'].hex())
    cipher = AES.new(key, AES.MODE_GCM, nonce=json_v['nonce'])
    cipher.update(json_v['header'])
    plaintext = cipher.decrypt_and_verify(json_v['ciphertext'], json_v['tag'])
    alist = json.loads(plaintext)
    json.dump(alist, decfile)
    decfile.close()
    encfile.close()
    os.remove(encfilename)
    unset_key("persist.env", "ENCF")
    set_key("persist.env", "DECF", decfilename)


''' Update the file password temporarily stored in .env
    for encrypting the file
'''


def updateFilePassword(pwd):
    passw = pwd.encode()
    set_key("persist.env", "PWD", passw.hex())
    # generate new salt
    keyGen()
    return







