import random
import re
from twilio.rest import Client
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

load_dotenv()

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to verify mobile number
def verify_mobile_number(mobile_number):
    pattern = re.compile(r'^(\+\d{1,3})?\d{10}$')
    return pattern.match(mobile_number)

# Function to verify email
def verify_email(email):
    pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    return pattern.match(email)

# Function to send otp via email
def send_otp_via_mail(otp, email):
    # Get the sender's email address and password
    sender_email = "dhanashrimahade@gmail.com"
    password = "Dhanashri@2004"
    
    # Create a message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = "OTP BY DM"

    # Add the message body
    message_text = "Your OTP is: {otp}"
    message.attach(MIMEText(message_text, 'plain'))

    # Connect to the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()

    # Login to the email account
    try:
        smtp_server.login(sender_email, password)
    except smtplib.SMTPAuthenticationError:
        print("Login failed. Please check your email address and password.")
        smtp_server.quit()
    else:
        # Send the email
        smtp_server.sendmail(sender_email, message['To'], message.as_string())
        print("Email sent successfully!")

    # Quit the SMTP server
    smtp_server.quit()

# Function to send OTP via Twilio SMS
def send_otp_via_mobile(otp, mobile_number):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=f"Your OTP is: {otp}", from_="+15856011208", to=mobile_number)

    print("OTP sent successfully via Twilio.")
    print(message)

def main():
    while True:
        mobile_number = input("Enter your mobile number: ")

        if not verify_mobile_number(mobile_number):
            print("Invalid mobile number. Please enter a valid mobile number.")
            continue

        break

    email = input("Enter your email address: ")

    while not verify_email(email):
        print("Invalid email address. Please enter a valid email address.")
        email = input("Enter your email address: ")

    otp = generate_otp()
    send_otp_via_mobile(otp, mobile_number)
    send_otp_via_mail(otp, email)
    print("OTP sent successfully!")
    print(f"Your OTP is: {otp}")

if __name__ == "__main__":
    main()
