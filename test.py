from aes import *
from oauth import *
from dotenv import set_key, unset_key, get_key
import os


def helper():
    tempf = "original.txt"
    f = open(tempf, "w")

    templist = []
    for x in range(25):
        url = "url" + str(x)
        user = "user" + str(x)
        passw = "pass" + str(x)
        templist.append({'site': url, 'username': user, 'password': passw})

    json.dump(templist, f)
    set_key("persist.env", "DECF", tempf)
    f.close()

def test():

    # create an arbitrary plaintext file for testing
    helper()

    # set the user's first file password
    #would normally come from gui
    updateFilePassword("firstPassword")

    # get oauth token.json
    getAuth()

    # generate an aes key with a random salt and the provided password
    # salt is stored in .env
    keyGen()

    #encrypt the file locally
    encryptFile()

    #generate local hmac
    hmacGen()

    # for user's first time create folder
    # folder id in .env
    create_folder()

    # for user's first time create/upload file in one go
    # file id in .env
    create_file()

    #processing competition
    remove_file_encf()

    # download file
    download_file()

    #verify local hmac
    hmacVerify()
    # decrypt file with user password
    # would normally get from gui
    decryptFile()

    # update user password & generate new salt
    updateFilePassword("secondPassword")

    #encrypt the file with new password
    encryptFile()

    # create 2/3 shamir keys
    set_key("persist.env", "K", "2")
    set_key("persist.env", "N", "3")
    shamirCreate()

    # get gmail addresses for sharing, testing only right now
    #set_key("persist.env", "RECEIVERS", "mbaileyking@gmail.com, mbaileyking@gmail.com, mbaileyking@gmail.com")

    #add your own emails for testing
    set_key("persist.env", "RECEIVERS", "")

    #email shamir keys
    send_shamir()

    #get shares from gui (temp hardcode)
    newshares = get_key("persist.env", "SHARES").split(" ", 2)

    #combine k shares
    shamirKey = shamirCombine(newshares)

    # check if shamir decrypt works (just using local enc file rn)
    sharefile = decryptWithShamir(shamirKey, get_key("persist.env", "ENCF"))

    print(sharefile)

    # remove non-persistent info from .env
    unset_key("persist.env", "SALT")
    unset_key("persist.env", "PWD")
    #unset_key("persist.env", "DECF")
    #unset_key("persist.env", "ENCF")

    return


test()