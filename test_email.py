from flask import Flask
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'goelparsh@gmail.com',
    MAIL_PASSWORD = 'iqhn rhzh btoa nlrb',
))

mail = Mail(app)

@app.route("/")
def index():

    msg = Message("Hello",
                  sender="goelparsh@gmail.com",
                  recipients=["pgoel8aug@gmail.com"])
    mail.send(msg)
    return "Success"

if __name__=='__main__':
    app.run(debug=True, port=8082)

    



h = {
'recommended_matches': [
{'bookings': [{'requester_id': '[]'}], 
'email': 'rjohnson@example.com', 
'hours': '9 AM to 12 PM', 
'location': {'pincode': '"pincode": "45678"}', 'street address': '{"street address": "1012 Maple St"'}, 'name': 'Robert Johnson', 'password': 'Johnson77', 'phone': '4567890123', 'ratings': '4', 'reviews': 'Good', 'schedule': {'"Friday"': '"9 AM - 12 PM"', '"Saturday"': '"Closed"', '"Sunday"': '"Closed"}', '"Thursday"': '"1 PM - 4 PM"', '"Tuesday"': '"10 AM - 1 PM"', '"Wednesday"': '"9 AM - 11 AM"', '{"Monday"': '"9 AM - 12 PM"'}, 'username': 'rjohnson'}, {'bookings': [{'requester_id': '[]'}], 'email': 'msmith@example.com', 'hours': '9 AM to 12 PM', 'location': {'pincode': '"pincode": "23456"}', 'street address': '{"street address": "456 Oak St"'}, 'name': 'Mary Smith', 'password': 'AlphaChar2', 'phone': '2345678901', 'ratings': '5', 'reviews': 'Good', 'schedule': {'"Friday"': '"9 AM - 12 PM"', '"Saturday"': '"Closed"', '"Sunday"': '"Closed"}', '"Thursday"': '"1 PM - 4 PM"', '"Tuesday"': '"10 AM - 1 PM"', '"Wednesday"': '"9 AM - 11 AM"', '{"Monday"': '"9 AM - 12 PM"'}, 'username': 'msmith'}, {'bookings': [{'requester_id': '[]'}], 'email': 'ishaankalra2004@gmail.com', 'hours': '9 AM to 12 PM', 'location': {'pincode': '"pincode": "34567"}', 'street address': '{"street address": "789 Pine St"'}, 'name': 'Alice White', 'password': 'Pass1234', 'phone': '3456789012', 'ratings': '3', 'reviews': 'Good', 'schedule': {'"Friday"': '"9 AM - 12 PM"', '"Saturday"': '"Closed"', '"Sunday"': '"Closed"}', '"Thursday"': '"1 PM - 4 PM"', '"Tuesday"': '"10 AM - 1 PM"', '"Wednesday"': '"9 AM - 11 AM"', '{"Monday"': '"9 AM - 12 PM"'}, 'username': 'awhite'}]}