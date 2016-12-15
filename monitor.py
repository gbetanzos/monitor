#!/usr/bin/python
import smtplib
import sys
import MySQLdb
from os import listdir
from os.path import isfile,isdir, join
from datetime import datetime, date,time
from email.mime.text import MIMEText
from smtplib import SMTP  


baseurl='https://server.org/sec1231234567890/'
emails=['guillermo@server.org','server@gmail.com']
videos=[]
conn = MySQLdb.connect(host="localhost", user="videosu", 
   passwd="123", db="videosdb")

def notify(videos,emails):
    global baseurl
    global mypath
    SMTPserver = 'mail.server.org'
    sender =     'guillermo@server.org'
    destination = ['guillermo@server.org',]

    USERNAME = "guillermo@server.org"
    PASSWORD = "123"

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    content="""\
Hi, there are new videos:
    
    """
    subject='New activity at bzlair'

    for v in videos:
		 v=v.replace(mypath,'')
		 log('Including '+v+' in the notification')
		 content+=baseurl+v+'\n'
    
    content+='\n '+str(len(videos))+ ' videos found.\n\nThanks'
    
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']= subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        smptConn = SMTP(SMTPserver)
        smptConn.set_debuglevel(False)
        smptConn.login(USERNAME, PASSWORD)
        try:
            smptConn.sendmail(sender, destination, msg.as_string())
        finally:
            smptConn.quit()
    except Exception, exc:
        sys.exit( "mail failed; %s" % str(exc) ) # give a error message
        log("mail failed; %s" % str(exc))
    
def log(entry):
    f=open('/tmp/debug.txt','a')
    now=datetime.now()
    now=now.strftime("%d/%m/%Y %H:%M:%S%p")
    f.write(now+" - "+entry+"\n")
    f.close()

def insertVideo(f):
    global videos
    global conn
    x=conn.cursor()
    print f
    entries=[f,'now()']
    try:
        add_video=("INSERT INTO files(file,timestamp) VALUES (%s,%s)")
        x.execute(add_video,entries)
        conn.commit()
        log("Inserting: "+f)
        videos.append(f)
    except BaseException as e:
        print str(e)
        conn.rollback();
        #log("Insert failed: "+f+ " - " +str(e))
    x.close()
        
def getfiles(path):
    files=[]
    dirs=[]
    
    for f in listdir(path):
        if isfile(join(path,f)) and f!='monitor.py' and f!='monitor.pyc':
            files.append(join(path, f))
            
        if isdir(join(path,f)):
            dirs.append(join(path,f+'/'))
    
    for f in files:
        insertVideo(str(f))
        
    for d in dirs:
        getfiles(d)
        print d


mypath="/videos/"
getfiles(mypath)
conn.close()

if len(videos)>0:
    notify(videos,emails)
    

