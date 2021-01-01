import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(weekend, the_date):

    port = 465  # for ssl

    sender_email = "sragets@gmail.com"
    receiver_email = 'dickdickerson@juno.com'
    if weekend == 0:
        subject = 'Midweek Meeting Attendance Report: ' + the_date
    else:
        subject = 'Weekend Meeting Attendance Report: ' + the_date
    password = input('Password: ')
    body = ''
    # create multipart message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # add body to email
    message.attach(MIMEText(body, 'plain'))

    filename = 'report.txt'
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # encode the file in ASCII characters to send by email
    encoders.encode_base64(part)

    # add header as key/value pair to attachment part
    part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
            )

    # add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # log in to server using secure context and send email
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
