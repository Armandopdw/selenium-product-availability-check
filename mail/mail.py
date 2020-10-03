import os
import re
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger as lg


class Mail():
    SMTP_CONF_MAPPING = {"gmail": {"server": "smtp.gmail.com",
                                   "port": 465},
                         "gmx": {"server": "mail.gmx.com",
                                 "port": 587}}

    PASS_PATH = os.getcwd() + '/pw/pw.txt'

    def __init__(self, sender_email, receiver_email):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = ""
        self.email_provider = self.get_email_provider(sender_email)
        self.smtp_server = self.SMTP_CONF_MAPPING[self.email_provider]['server']
        self.smtp_port = self.SMTP_CONF_MAPPING[self.email_provider]['port']

    def get_email_provider(self, sender_email):
        # Retrieves the SMTP url (e.g. smtp.gmail.com) based on the domain name (e.g. gmail.com)
        regex_match = re.search('@(.+)\..+', sender_email, re.IGNORECASE)
        if regex_match:
            return regex_match.group(1)
        else:
            raise ValueError("Sender email did not match expected format: [email]@[email_provider].[domain] (e.g. email@gmail.com")

    def create_ssl_connection(self):
        # Create a secure SSL context
        self.context = ssl.create_default_context()

    def load_password(self):
        # self.password = getpass.getpass(prompt='Type your email password here: ')
        with open(self.PASS_PATH) as f:
            self.password = f.readline()

    def send_email(self, subject, plain_text, html):
        if not self.password:
            raise AttributeError("Password was not yet set. Please set password in :%s" % self.PASS_PATH)

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

        # Get server
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)

        # Port 587 requires ttls
        if self.smtp_port == 587:
            starttls = server.starttls()
        login = server.login(self.sender_email, self.password)
        lg.debug("Logged into mail: %s" % login[1])

        server.sendmail(self.sender_email, self.receiver_email, message.as_string())
        lg.debug("Sent mail")

        server.quit()
        del server
