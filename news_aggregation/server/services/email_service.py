import smtplib
from email.message import EmailMessage

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.from_email = "your_email@gmail.com"
        self.password = "your_app_password"  # Use App Password if using Gmail

    def send_email(self, to_email, subject, content):
        msg = EmailMessage()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.set_content(content)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.send_message(msg)
                print(f"[EMAIL SENT] -> {to_email}")
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
