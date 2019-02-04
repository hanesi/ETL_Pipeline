import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_error_message(error):
  SENDER = 'Email'  
  SENDERNAME = 'Sender Name'
  RECIPIENT  = ['Recipients']
  USERNAME_SMTP = "STMP Username"
  PASSWORD_SMTP = "STMP Password"
  HOST = "host"
  PORT = 587
  SUBJECT = 'Exception in Pipeline Process'
  # The email body for recipients with non-HTML email clients.
  BODY_TEXT = ("There was an error collecting data. \
                Please see the following error message and report it the appropriate personnel.\r\n\n"
               "{}".format(error)
              )
  # The HTML body of the email.
  BODY_HTML = """<html>
  <head></head>
  <body>
    There was an exception collecting data. \
    Please see the following error message and report it the appropriate personnel.\r\n
    <p>{}</p>
  </body>
  </html>
              """.format(error)

  # Create message container - the correct MIME type is multipart/alternative.
  msg = MIMEMultipart('alternative')
  msg['Subject'] = SUBJECT
  msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
  msg['To'] = ", ".join(RECIPIENT)
  part1 = MIMEText(BODY_TEXT, 'plain')
  part2 = MIMEText(BODY_HTML, 'html')
  msg.attach(part1)
  msg.attach(part2)

  # Try to send the message.
  try:  
      server = smtplib.SMTP(HOST, PORT)
      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login(USERNAME_SMTP, PASSWORD_SMTP)
      server.sendmail(SENDER, RECIPIENT, msg.as_string())
      server.close()
  # Display an error message if something goes wrong.
  except Exception as e:
    pass
