import smtplib
import ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pathlib

cwd = str(pathlib.Path(__file__).parent.absolute())


class Mail ():
    def __init__(self, sender_email, receiver_email):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = ""

    def create_ssl_connection(self):
        # Create a secure SSL context
        self.port = 465  # For SSL
        self.context = ssl.create_default_context()

    def load_password(self):
        #self.password = getpass.getpass(prompt='Type your email password here: ')
        with open(cwd + '/pw/pw.txt') as f:
            self.password = f.readline()

    def send_email(self, subject, plain_text, html):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(plain_text, "plain")
        part2 = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, self.receiver_email, message.as_string()
            )

