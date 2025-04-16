import smtplib

from app.config import settings

class EmailSender:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port: int = int(smtp_port) 
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, body, from_email=None):

        if from_email is None:
            from_email = self.username

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:

                server.login(self.username, self.password)

                message = f"From: {self.username}\nSubject: {subject}\n\n{body}"

                server.sendmail(self.username, to_email, message)

        except Exception as e:
            print(f"Failed to connect to the SMTP server: {e}")

email_sender = EmailSender(
    smtp_server = settings.SMTP_HOST,
    smtp_port = 465,
    username= settings.SMTP_USER,
    password= settings.SMTP_PASSWORD
)



