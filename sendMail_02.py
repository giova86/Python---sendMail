import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# -- SERVER PARAMETERS --------------------------------------
smtp = 'smtp.com'
port = 456

# -- MESSAGE PARAMETERS -------------------------------------
sender = 'sender@gmail.com'
receiver = ['receiver1@gmail.com', 'receiver2@gmail.com']
receiver_Cc = ['receiver1_Cc@gmail.com', 'receiver2_Cc@gmail.com']

# -- ATTACHMENT ---------------------------------------------
attachment_path = 'folder_path'
attachment_file = 'file_name'

# -- BODY ---------------------------------------------------
body = f'''
    <html>
        <body>
            <h2>TITLE</h2>
            Dear User,<br>
            this is your mail...<br>

            <p>Write HTML text...</p>
            <br>

            <p><i>
            This is an automatically generated email – please do not reply to it. If you have any queries regarding the analysis please email
            </i></p>

            <i>Contact: <a href= "mailto:mail@hotmail.com">mail@hotmail.com</a></i>

        </body>
    </html>
    '''

# -- BUILD MAIL ---------------------------------------------

#Setup the MIME
message = MIMEMultipart()
message['From'] = sender
message['To'] = ", ".join(receiver)
message['Cc'] = ", ".join(receiver_Cc)
message['Subject'] = "Subject of the Mail"
message.attach(MIMEText(body, 'html'))

# open the file in bynary
binary_pdf = open(attachment_path + attachment_file, 'rb')

payload = MIMEBase('application', 'octate-stream', Name=f"{attachment_file}")

payload.set_payload((binary_pdf).read())

# enconding the binary into base64
encoders.encode_base64(payload)

# add header with pdf name
payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
message.attach(payload)

# -- LOGIN --------------------------------------------------
session = smtplib.SMTP(smtp, port)

# -- SEND MAIL ----------------------------------------------
text = message.as_string()
session.sendmail(sender, receiver, text)
for i in receiver:
    print(f'Mail Sent to {i}')
session.quit
