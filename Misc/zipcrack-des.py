import crypt

#DES Password Cracker. DES encryption leaves the salt in the first two chars
#Requires a dictionary file and list of encrypted passwords
#Using Python3 allows for stronger versions of "crypt" library
#https://docs.python.org/3/library/crypt.html
#author: nxkennedy

def testPass(cryptPass):
    #identifies salt as first two chars
    salt = cryptPass[0:2]
    #plaintext words to iterate over
    wordList = open('dictionary.txt', 'r')
    for word in wordList.readlines():
        word = word.strip('\n')
        cryptWord = crypt.crypt(word, salt)
        if (cryptWord == cryptPass):
            print("[+] Found Password: {0}\n".format(word))
            return
    print("[-] Password Not Found\n")
    return

def main():
    passFile = open('passwords.txt')
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            print("[*] Cracking Password For: {0}".format(user))
            testPass(cryptPass)
        else:
            cryptPass = line.strip('\n')
            print("\n[*] Cracking Password: {0}".format(line))
            testPass(cryptPass)

if __name__ == "__main__":
    main()
