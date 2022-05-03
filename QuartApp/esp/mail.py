import imaplib
from email.header import decode_header
from email.parser import BytesHeaderParser

from dotenv import load_dotenv
import os

load_dotenv()

# account credentials
username = os.getenv('MAIL_Password')
password = os.getenv('MAIL_Username')

def getMails():

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")

    # authenticate
    imap.login(username, password)
    status, messages = imap.select("INBOX",readonly=True) # enlever readonly pour mettre tout en lu

    prioTitle = ["insa","dofus","ankama","important","urgent","re:"]
    nbMailsPrio = 0

    res, data = imap.uid('SEARCH', None, '(UNSEEN)')
    uids = data[0].split()
    for uid in uids:
        result, data = imap.uid('fetch', uid, '(RFC822)') 
        mail = data[0]

        parser = BytesHeaderParser()
        h = parser.parsebytes(mail[1])

        mailFrom = h["From"]
        mailDate = h["Date"]
        mailSubject = h["Subject"]

        subjects = decode_header(mailSubject)
        mailSubject = ""

        for subject,encoding in subjects :
            if isinstance(subject, bytes):
                if encoding : 
                    mailSubject += subject.decode(encoding)
                else :
                    mailSubject += subject.decode()
            else :
                mailSubject += subject

        # print(mailDate,mailFrom,mailSubject)
        header = mailFrom + mailSubject
        for title in prioTitle : 
            if title in header.lower() : 
                nbMailsPrio += 1
                break

    # close the connection and logout
    imap.close()
    imap.logout()

    print("Nombres mails prio :", nbMailsPrio)
    print("Nombres mails non lus :", len(uids))

    return [len(uids),nbMailsPrio]