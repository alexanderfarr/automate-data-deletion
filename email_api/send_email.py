from flask import Flask, request, jsonify
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
app = Flask(__name__)

# send a new email
@app.route('/email', methods=['POST'])
def post():
    data = request.get_json()
    from_email=data["from_email"]
    password=data["password"]
    to_email=data["to_email"]
    subject=data["subject"]
    message=data["message"]
    msg=MIMEMultipart()
    msg['From']=from_email
    msg['Subject']=subject
    msg['To']=to_email
    msg.attach(MIMEText(message, 'plain'))
    try:
        #gmail: https://myaccount.google.com/lesssecureapps enable access
        #server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server = smtplib.SMTP('smtp.live.com', 587)
        server.starttls()
        server.ehlo()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close
    except Exception as e:
        print("ERROR")
        return "Error: "+str(e)

    return json.dumps({"email_sent": True}), 200
