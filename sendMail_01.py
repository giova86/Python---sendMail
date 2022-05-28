# send mail with no authentication, no TLS
import smtplib

# server parameters
smtp = 'smtp.com'
port = 456

# message
sender = 'sender@gmail.com'
receiver = 'receiver@gmail.com'
text = 'text message'

# login
server = smtplib.SMTP(smtp, port)

server.sendmail(
    sender,
    receiver,
    text
)

server.quit()
