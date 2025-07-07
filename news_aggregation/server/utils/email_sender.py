import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    from_email = "shashilearnandcode@gmail.com"
    password = "Sk@0791632"  
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(from_email, password)
            smtp.send_message(msg)
        print(f" Email sent to {to_email}")
    except Exception as e:
        print(f" Email failed: {e}")
