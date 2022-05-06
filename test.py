from aes import *
from oauth import *
import env
import os


def helper():
    tempf = "outputs/original.txt"
    f = open(tempf, "w")

    templist = []
    for x in range(25):
        url = "url" + str(x)
        user = "user" + str(x)
        passw = "pass" + str(x)
        templist.append({'site': url, 'username': user, 'password': passw})

    json.dump(templist, f)
    env.set("DECF", tempf)
    f.close()

def test():

    # create an arbitrary plaintext file for testing
    helper()

    # set the user's first file password
    #would normally come from gui
    saltGen()
    updateFilePassword("firstPassword")

    # get oauth token.json
    getAuth()

    #check file permissions if needed
    #get_gfile_permissions()

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
    env.set("K", "2")
    env.set("N", "3")
    shamirCreate()

    # get gmail addresses for sharing, testing only right now
    #env.set("RECEIVERS", "mbaileyking@gmail.com") #, mbaileyking@gmail.com, mbaileyking@gmail.com")


    #add your own emails for testing
    env.set("RECEIVERS", "")
    #share the google file
    share_gfile()
    #email shamir keys
    send_shamir()

    #delete secrets.txt file from drive
    destroy_gfile()
    #get shares from gui (temp hardcode)
    #newshares = env.get("SHARES").split(" ", 2)

    #combine k shares
    #shamirKey = shamirCombine(newshares)

    # check if shamir decrypt works (just using local enc file rn)
    #sharefile = decryptWithShamir(shamirKey, env.get("ENCF"))

    #print(sharefile)

    # remove non-persistent info from .env
    env.unset("SALT")
    env.unset("PWD")
    #unset_key("persist.env", "DECF")
    #unset_key("persist.env", "ENCF")
    '''
    return

#if __name__ == '__main__':
test()