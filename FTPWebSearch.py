__author__ = 'derog'

import ftplib
def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
        print '[*] Searching for Web Pages'
    except:
        dirList =[]
        print '[-] Could not list directory contents.'
        print '[-] Skipping To Next Target.'
        return
    retList = []
    for filename in dirList:
        fn=filename.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print '[+] Found default page: ' + filename
            retList.append(filename)

if __name__=="__main__":
    host = 'localhost'
    userName= 'root'
    password = 'toor'
    ftp =ftplib.FTP(host)
    ftp.login(userName,password)
    returnDefault(ftp)