"""ItsMail.py - Send Email
NAME:
    ItsMail.py - Send Email
"""

import smtplib, socket
from email.mime.text import MIMEText

class ItsMail ( object ):
    
    def __init__ ( self ):
        self.smtpHost = 'localhost'
        #self.smtpHost = 'smtp.gmail.com'
        self.mailFrom = 'todd.shoenfelt@hgst.com'
        self.mailTo = ''
        self.subject = ''
        self.text = ''
        
    def send ( self ):
        
        socket.setdefaulttimeout( 300 )
        s = smtplib.SMTP( self.smtpHost )
        
        #s = smtplib.SMTP( self.smtpHost, 587 )
        #s.starttls()
        #s.set_debuglevel( 1 )
        
        msg = MIMEText( self.text )
        msg['Subject'] = self.subject
        msg['From'] = self.mailFrom
        msg['To'] = self.mailTo
        #print msg
        try:
            s.sendmail( self.mailFrom, self.mailTo, msg.as_string() )
        except Exception as e:
            print "Exception caught"
        s.quit()
        

