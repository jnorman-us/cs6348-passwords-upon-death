# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Protocol.SecretSharing import Shamir
import json
from base64 import b64encode
from base64 import b64decode
from Crypto.Hash import HMAC, SHA256


PASSW = "PaSsWoRd"
SECRET = b'Swordfish'


def hmacGen(filename):
    f = open(filename, 'rb')
    msg = f.read()
    h = HMAC.new(SECRET, digestmod=SHA256)
    h.update(msg)
    f.close()
    return h.hexdigest()

def hmacVerify(filename, hmac):
    f = open(filename, 'rb')
    msg = f.read()
    h = HMAC.new(SECRET, digestmod=SHA256)
    h.update(msg)
    try:
        h.hexverify(hmac)
        return 1
    except ValueError:
        return 0

def keyGenWithSalt(salt):
    password = PASSW.encode()
    key = scrypt(password, salt, 32, N=2 ** 20, r=8, p=1)
    return key

def keyGen():
    password = PASSW.encode()
    salt = get_random_bytes(32)
    key = scrypt(password, salt, 32, N=2**20, r=8, p=1)
    return key, salt

def shamirCreate(salt, k, n):
    password = PASSW
    key = scrypt(password, salt, 32, N=2**20, r=8, p=1)
    key1 = key[:16]
    key2 = key[16:]
    print(key1.hex())
    print(key2.hex())

    shares1 = Shamir.split(k, n, key1)
    shares2 = Shamir.split(k, n, key2)
    shares = []
    for i, ((idx1, sh1), (idx2, sh2)) in enumerate(zip(shares1, shares2)):
        bytestring = idx1.to_bytes(2, 'big')
        bytestring += sh1[0:16]
        bytestring += idx2.to_bytes(2, 'big')
        bytestring += sh2[0:16]
        shares.append(bytestring.hex())

    return shares

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

    print(sh1)
    print(sh2)
    key1 = Shamir.combine(sh1)
    key2 = Shamir.combine(sh2)
    key = key1 + key2
    print(key1.hex())
    print(key2.hex())
    return key

def encryptFile(key, salt, infilename):

    outfilename = infilename + ".encrypted"
    infile = open(infilename, 'rb')
    outfile = open(outfilename, 'w')
    cipher = AES.new(key, AES.MODE_GCM)
    data = infile.read()
    cipher.update(salt)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [b64encode(x).decode('utf-8') for x in (cipher.nonce, salt, ciphertext, tag)]
    result = json.dumps(dict(zip(json_k, json_v)))
    outfile.write(result)
    infile.close()
    outfile.close()

    return outfilename

def decryptWithShamir(key, encfilename):
    encfile = open(encfilename, 'r')
    decfilename = encfilename + ".shared"
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
    return decfilename

def decryptFile(encfilename):

    encfile = open(encfilename, 'r')
    decfilename = encfilename + ".dec"
    decfile = open(decfilename, 'w')
    b64 = json.load(encfile)
    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = {k:b64decode(b64[k]) for k in json_k}

    key = keyGenWithSalt(json_v['header'])
    cipher = AES.new(key, AES.MODE_GCM, nonce=json_v['nonce'])
    cipher.update(json_v['header'])
    plaintext = cipher.decrypt_and_verify(json_v['ciphertext'], json_v['tag'])
    alist = json.loads(plaintext)
    json.dump(alist, decfile)
    decfile.close()
    encfile.close()
    return decfilename



def main():
    key, salt = keyGen()
    tempf = "localcopy.txt"
    f = open(tempf, "w")
    k = 3
    n = 5

    templist = []
    for x in range(25):
        url = "url" + str(x)
        user = "user" + str(x)
        passw = "pass" + str(x)
        templist.append({'site': url, 'username': user, 'password': passw})

    json.dump(templist, f)
    f.close()

    encfile = encryptFile(key, salt, tempf)
    hmac = hmacGen(encfile)
    flag = hmacVerify(encfile, hmac)
    print(flag)
    decfile = decryptFile(encfile)

    shamirs = shamirCreate(salt, k, n)

    newshares = []
    for x in range(k):
        newshares.append(shamirs[x])

    shamirKey = shamirCombine(newshares)
    sharefile = decryptWithShamir(shamirKey, encfile)



if __name__ == '__main__':
    main()


