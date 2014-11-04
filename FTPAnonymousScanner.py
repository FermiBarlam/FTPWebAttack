__author__ = 'derog'

import ftplib
def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous','such@fake.com')
        print '\n[*] ' + str(hostname) + ' FTP Anonymous Login Succeeded.'
        ftp.quit()
        return True
    except Exception, e:
        print '\n [-] ' + str(hostname) + ' FTP Anonymous Login Failed'
        return False

if __name__=="__main__":
    host = 'localhost'
    anonLogin(host)