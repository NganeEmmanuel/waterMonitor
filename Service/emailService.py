import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_to_recipient(recipient_email, subject, body):
    # Email configuration
    sender_email = "emmanuelngane06@gmail.com"
    sender_password = "duas mrcc aujg vsym"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Create SMTP session for sending the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(
            sender_email, recipient_email, message.as_string()
        )

    print("Email sent successfully.")