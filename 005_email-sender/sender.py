"""
Task: create a python program that sends an email to a list of emails that the user provides. 
ask the user for the subject and body. send the email through my personal gmail.

Example Output:
Enter email subject: Hello from Python
Enter email body: This is a test email sent from the new tool.
Enter recipient emails (comma-separated): recipient1@example.com, recipient2@example.com
Connecting to Gmail SMTP server as your-email@gmail.com...
Sending email to recipient1@example.com...
Sending email to recipient2@example.com...
Success: Email(s) sent successfully!
"""
import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_emails():
    # Credentials
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("Error: EMAIL_ADDRESS or EMAIL_PASSWORD not found in environment.")
        print("Please create a .env file based on .env.template.")
        return

    # User input
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    recipients_input = input("Enter recipient emails (comma-separated): ")
    recipients = [email.strip() for email in recipients_input.split(",") if email.strip()]

    if not recipients:
        print("Error: No valid recipients provided.")
        return

    # Email setup
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)

    # Sending
    context = ssl.create_default_context()
    try:
        print(f"Connecting to Gmail SMTP server as {sender_email}...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            for recipient in recipients:
                print(f"Sending email to {recipient}...")
                # Update "To" for each recipient if sending individually, 
                # but here we follow the prompt to send to a list.
                # If the user wants a single email with everyone cc'd, the above is fine.
                # If they want individual emails, we should loop and set 'To' each time.
                # Given the wording "sends an email to a list", a single email with multiple recipients is standard,
                # but often "sending to a list" implies individual delivery. 
                # Let's stick to a single send for now as it matches "an email to a list".
            server.send_message(msg)
        print("Success: Email(s) sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_emails()
