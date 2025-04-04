from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

def initiate_call(phone_number):
    call = client.calls.create(
        url=f"http://localhost:8000/voice",
        to=phone_number,
        from_=twilio_number,
        record=True
    )
    return call

def handle_incoming_call(call_sid, speech_text):
    # Process speech input and return response
    pass