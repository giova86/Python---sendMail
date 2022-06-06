from pickle import TRUE
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json

# -- READ SETTINGS ------------------------------------------
with open('config/server_settings.json', 'r') as f:
    data = json.load(f)

with open('config/contacts_settings.json', 'r') as f:
    contacts = json.load(f)

# -- SERVER PARAMETERS --------------------------------------
smtp = data['smtp']
port = data['port']
username = data['username']
password = data['password']

# -- MESSAGE PARAMETERS -------------------------------------
sender = contacts['sender']
receiver = contacts['receiver']
receiver_Cc = contacts['receiver_Cc']

# -- ATTACHMENT ---------------------------------------------
attachment_bool = contacts['attachment']['include']
attachment_path = contacts['attachment']['path_folder']
attachment_file = contacts['attachment']['path_file']

# -- BODY ---------------------------------------------------
body = f'''
    <html>
        <body>
            <h2>TITLE</h2>
            Dear User,<br>
            this is your mail...<br>

            <p>Write HTML text...</p>
            <br>
            <br>
            <hr>
            <p><i>
            This is an automatically generated email – please do not reply to it. If you have any queries regarding the analysis please email
            </p>

            <p>Contact: <a href= "mailto:mail@hotmail.com">mail@hotmail.com</a></i></p>
            <hr>
            <br>
            <br>
            <br>

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

if attachment_bool == "TRUE":
    # open the file in bynary
    binary_pdf = open(attachment_path + attachment_file, 'rb')

    payload = MIMEBase('application', 'octate-stream', Name=f"{attachment_file}")

    payload.set_payload((binary_pdf).read())

    # enconding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition', 'attachment', filename=attachment_file)
    message.attach(payload)

# -- LOGIN --------------------------------------------------
session = smtplib.SMTP(smtp, port)

session.starttls()

#login with mail_id and password
session.login(username, password)

# -- SEND MAIL ----------------------------------------------
text = message.as_string()

session.sendmail(sender, receiver+receiver_Cc, text)
for i in receiver:
    print(f'Mail Sent to {i}')
session.quit
