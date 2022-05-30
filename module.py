from pickle import TRUE
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json


def sendmail(sender: str, receiver: list, subject: str, text: str, smtp: str, port: int,
             receiver_cc: list = None, attachment_path: str = None, attachment_file: str = None,
             TLS: bool = False, username: str = None, password: str = None):
    """
    Function to send mail. 
    
    Parameters
    ----------
    sender : str
        The email of the sender
    receiver : list
        The email list of the receivers
    subject : str
        The subject of the message
    text : str
        The text of the message. HTML language is supported.
    smtp : str
        SMTP of the server
    port : int
        Port number of the server
    receiver_cc : list, optional
        The email list of the receivers (Carbon Copy)
    attachment_path : str, optional
        Path of attachment file
    attachment_file : str, optional
        Attachment file
    TLS : bool, optional
        Defaults to False. Use TRUE for setting TLS
    username : str, optional
        Set the username if the authentication is enabled
    password : str, optional
        Set the password if the authentication is enabled
    """
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ", ".join(receiver)
    if receiver_cc is not None:
        message['Cc'] = ", ".join(receiver_Cc)
    message['Subject'] = subject
    message.attach(MIMEText(text, 'html'))

    if (attachment_path is not None) and (attachment_file is not None):
        # open the file in bynary
        binary_pdf = open(attachment_path + attachment_file, 'rb')

        payload = MIMEBase('application', 'octate-stream', Name=f"{attachment_file}")

        payload.set_payload(binary_pdf.read())

        # enconding the binary into base64
        encoders.encode_base64(payload)

        # add header with pdf name
        payload.add_header('Content-Decomposition', 'attachment', filename=attachment_file)
        message.attach(payload)

    session = smtplib.SMTP(smtp, port)

    if TLS == TRUE:
        session.starttls()

    if (username is not None) and (password is not None):
        # login with mail_id and password
        session.login(username, password)

    # -- SEND MAIL ----------------------------------------------
    text = message.as_string()

    session.sendmail(sender, receiver, text)
    for i in receiver:
        print(f'Mail Sent to {i}')
    session.quit


if __name__ == '__main__':
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
                This is an automatically generated email - please do not reply to it. If you have any queries regarding the analysis please email
                </p>

                <p>Contact: <a href= "mailto:mail@hotmail.com">mail@hotmail.com</a></i></p>
                <hr>
                <br>
                <br>
                <br>

            </body>
        </html>
        '''

    sendmail(sender=sender,
             receiver=receiver,
             subject="questo è l'oggetto della mail",
             text=body,
             smtp=smtp,
             port=port,
             TLS=TRUE,
             username=username,
             password=password
             )
