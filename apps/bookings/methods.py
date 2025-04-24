from django.core.mail import  EmailMultiAlternatives
from .models import Booking
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_booking_email(id: str):
    mail_subjects = "Your Booking Details."
    
    booking = Booking.objects.get(id=id)

    html_message = render_to_string("email.html", context={"booking": booking})
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = mail_subjects, 
        body = plain_message,
        from_email = None ,
        to= [booking.passenger_email]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
