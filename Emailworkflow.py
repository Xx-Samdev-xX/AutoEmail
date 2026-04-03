import os
import smtplib, ssl
import logging as lg
from email.message import EmailMessage
import pycountry
from openai import OpenAI
import random
import pycountry

#getting  random country and loggind
countries = [country.name for country in pycountry.countries]
country = random.choice(countries)
lg.info(f'Country chosen: {country}')

client = OpenAI(
    api_key = os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1" 
)

def generate_message(country):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are confident, funny, slightly sarcastic Gen Z"},
            {"role": "user", "content": f"Send me the latest new in {country}"}
        ]
    )

    return response.choices[0].message.content


#0 logging file 
lg.basicConfig(
    filename="Auto Email.log",
    level=lg.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


#1 sender and receiver credentials
sender_email = os.environ.get('SENDER_EMAIL')
password = os.environ.get('APP_PASSWORD')
receiver_email = sender_email

#2 message block
msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "DailyNews"
msg.set_content (generate_message(country))

content = ssl.create_default_context() # secure connection and send
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())as smtp:
        smtp.login(sender_email, password)
        lg.info(f"Loggin to{sender_email} successful")
        smtp.send_message(msg)
    lg.info(f"Message sent successfully to {receiver_email}")
except smtplib.SMTPAuthenticationError:
    lg.critical("Authorisation not successful")
except Exception as e:
    lg.critical(f"An error occurred {e}")




