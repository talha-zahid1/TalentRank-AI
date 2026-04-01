import smtplib
from email.message import EmailMessage
from schemas.appschema import *


setting = Settings()


def welcome_email( reciever_email):
    msg = EmailMessage()
    msg["Subject"]  = "Welcome to TalentRank AI Your Journey Starts Here"
    msg["From"] = setting.s_email
    msg["To"] = reciever_email
    msg.set_content(
        "Welcome to TalentRank AI! Your account has been successfully created. You are now ready to explore opportunities, apply for jobs, and showcase your skills. We’re excited to have you on board and wish you great success on your journey"
    )
    server(msg=msg)


def job_selection_email(reciever_email):
    msg = EmailMessage()
    msg["Subject"] = "Congratulations! You've Been Selected via TalentRank AI"
    msg["From"] = setting.s_email
    msg["To"] = reciever_email
    msg.set_content(
        "Congratulations! We are pleased to inform you that you have been selected by a recruiter through TalentRank AI for the applied position. This is a great step forward in your professional journey. Kindly stay connected and follow any further instructions provided by the recruiter. We wish you the very best for the next steps ahead."
    )
    server(msg=msg)


def server(msg):
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as serv:
        serv.starttls()
        serv.login(setting.s_email, setting.google_acc_password)
        serv.send_message(msg=msg)
