from twilio.rest import Client
from django.conf import settings

def send_appointment_sms(phone_number, name, appointment_date):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message = f"Hello {name}, your appointment is scheduled for {appointment_date}."
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )