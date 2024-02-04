##
# HackViolet
# Flask Endpoint Implementation
#
# First created: 3-FEB-2024
# Last updated:  3-FEB-2024
# Author: Aryan Agrawal, Ishaan Kalra, Parsh Goel
##

import os
import logging
import datetime
import sys
import json
import openai
import google.cloud.logging

from flask import Flask, request, jsonify
from flask_mail import Mail
from flask_mail import Message

from google.cloud import bigquery
# from google_auth_oauthlib.flow import Flow





# Global Variables
app = Flask(__name__)

THISDIR = os.path.dirname(os.path.realpath(__file__))

openai.api_type = "azure"
openai.api_base = "https://azu-sdg-eastus-openai-poc.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPEN_AI_API_KEY")


logging_client = google.cloud.logging.Client()
logging_client.setup_logging()

BQ_TABLE_ID = os.getenv('BQ_TABLE_ID')
BQ_DATASET_ID = os.getenv('BQ_DATASET_ID')




base_rate = 10
# multiplier = {5:1.5, 4:1.25, 3:1, 2:0.75, 1:0.5}
# is_cancellation = False
# is_emergency = False
# emergency_multiplier = 1.5 if is_emergency else 1

 
#configs
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



# Endpoints
# auth(input = username and password) -> true/false and hours
# match (input = username, date, start and end time in 24 hour format) -> return a list of lists based on best matches -> [['user1', 'name', 'reviews', 'hours', 'schedule', 'rating', 'contact']]


def send_email(message, to_email):
    msg = Message(
                  sender="goelparsh@gmail.com",body=str(message),subject="Your GoMama Booking is confirmed",
                  recipients=[str(to_email)])
    
    return str(mail.send(msg))

def calculate_credits(username):
    client = bigquery.Client()

    # Calculate initial credits without penalties
    query = f"""
        SELECT hours, rating
        FROM `gomama-413222.{BQ_TABLE_ID}.{BQ_DATASET_ID}` 
        WHERE username = "{username}"
    """

    query_job = client.query(query)
    results = query_job.result()

    for row in results:
        user_hours = row.hours
        user_rating = int(row.rating)

        break
    else:
        raise ValueError("User not found or hours not set.")

    total_credits = base_rate * user_hours 
    rating_multiplier = {
        1: 0.5,
        2: 0.75,
        3: 1,
        4: 1.25,
        5: 1.5
    }.get(user_rating, 1) 

    total_credits *= rating_multiplier

    
    # Deduct penalties for cancellations or no-shows
    # if is_cancellation:
    #     total_credits -= 10  # Deduct 10 credits for late cancellations or no-shows
    
    # Ensure total credits don't go negative due to penalties
    total_credits = max(total_credits, 0)

    update_query = f"""
        UPDATE `gomama-413222.{BQ_TABLE_ID}.{BQ_DATASET_ID}`
        SET credits = "{total_credits}"
        WHERE username = "{username}"
    """

    update_job = client.query(update_query)
    update_job.result() 
    
    return total_credits

def get_details(username):
    client = bigquery.Client()
    query = f"""
        SELECT username, password, phone, email, name, hours, location, schedule, bookings, ratings, reviews
        FROM `gomama-413222.{BQ_TABLE_ID}.{BQ_DATASET_ID}`
        WHERE username = "{username}"
    """

    query_job = client.query(query)
    results = query_job.result()

    details_dict = {}

    for row in results:
        # Split the location into street address and pincode
        location_parts = row.location.split(",")
        location_dict = {
            "street address": location_parts[0].strip(),
            "pincode": location_parts[1].strip()
        }

        # Split the schedule and convert it into a dictionary
        schedule_parts = row.schedule.split(",")
        schedule_dict = {day.split(":")[0].strip(): day.split(":")[1].strip() for day in schedule_parts}

        if row.bookings:  # Check if bookings is not empty
            bookings_list = [
                dict(zip(["requester_id", "provider_id", "date", "start_time", "end_time"], booking.split(":")))
                for booking in row.bookings.split(";")
            ]
        else:
            bookings_list = []

        details_dict = {
            "username": row.username,
            "password": row.password,
            "phone": row.phone,
            "email": row.email,
            "name": row.name,
            "hours": row.hours,
            "location": location_dict,
            "schedule": schedule_dict,
            "bookings": bookings_list,
            "ratings": row.ratings,
            "reviews": row.reviews,
            # "credits": calculate_credits(username)
        }

    return details_dict


@app.route("/user", methods=['GET', 'POST'])
def get_user_info():
    request_data = request.get_json()
    details = get_details(request_data['username'])
    if details:
         return jsonify(details), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route("/auth", methods=['GET','POST'])
def validate():
    logging.info("validate method started")
    request_data = request.get_json()
    logging.info(f"{request_data}")
    username = request_data['username']
    password = request_data['password']

    logging.info(f"{username} and {password}")
    client = bigquery.Client()

    query = f"""
        SELECT username, password
        FROM `gomama-413222.{BQ_TABLE_ID}.{BQ_DATASET_ID}` 
        WHERE username = "{username}"
    """

    logging.info(f"query: {query}")

    query_job = client.query(query)

    results = query_job.result()  # Waits for the query to finish

    logging.info(f"{results}")

    for row in results:
        stored_username, stored_password = row.username, row.password
        if username == stored_username and password == stored_password:
            return jsonify({"status": "success", "message": "Authentication successful"}), 200
    
    return jsonify({"status": "failure", "message": "Authentication failed"}), 404


@app.route("/match", methods=['GET', 'POST'])
def get_matches():
    request_data = request.get_json()
    username = request_data['username']
    user_hours = request_data['hours']
    logging.info(f"{username} {user_hours}")

    # Initialize BigQuery client
    client = bigquery.Client()

    # Update your query to also select the location
    query = f"""
        SELECT username, name, hours, location, schedule
        FROM `gomama-413222.{BQ_DATASET_ID}.{BQ_TABLE_ID}`
    """

    query_job = client.query(query)
    results = query_job.result()

    user_info = ""
    user_location = ""
    for row in results:
        if row.username != username:
            user_info += f"Name: {row.username}, Available Hours: {row.schedule}, Location: {json.loads(row.location)}\n"
        else:
            user_location = str(json.loads(row.location))
        
    
    prompt = f"""Given a user who requested these hours for childcare: {user_hours} and their location: {user_location}, 
    find top three matches from the following other users based on their availability hours and location:\n{user_info}. \n\n
    Give a top 3 ranking in this list format. Give the username, name, location and a description of how good of a match they are. Note that only return the list and nothing else. It is essential that only a list is returned. If you dont find a match or anything unexpected happens, return an empty list.
    
    Output Format:
    ```
    [
        ['username1', 'name1', 'location1', 'description1'],
        ['username2', 'name2', 'location2', 'description2'],
        ['username3', 'name3', 'location3', 'description3']
    ]
    ```
    
    Sample Output: [
        ['alex23', 'alex', '7839 whie street', 'this user is available during the requested hours and is also near the person requesting the service'],
        ['oran57', 'oran', '536 denton lane', 'this is a fair match since user is only available for certain hours and is also not close to the requested location']
        ]
    """

    logging.info(f"{prompt}")
    # Use OpenAI API to get recommendations
    message_text = [
        {"role":"system", "content":"You are an AI recommender assistant that helps people match customers looking for childcare service for certain hours with other suitable people who are available at that time and a nearby location."},
        {"role":"user", "content":prompt}
        ]


    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages = message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    logging.info(str(response))
    recommended_matches = response['choices'][0]['message']['content']

    logging.info(f"{recommended_matches}")

    match_list = []

    recommended_matches = recommended_matches[recommended_matches.index("```"):]
    recommended_matches = recommended_matches[recommended_matches.index("["):]
    while recommended_matches[-1] != "]":
        recommended_matches = recommended_matches[:-1]
    for match in list(eval(recommended_matches)):
        user = match[0]
        match_list.append(get_details(str(user)))
        
        

    if match_list != []:
        return jsonify({"recommended_matches": match_list}), 200
    else:
        return jsonify({"recommended_matches": []}), 500


  
def get_user_email(username):
    query = f"""
        SELECT email 
        FROM `gomama-413222.{BQ_TABLE_ID}.{BQ_DATASET_ID}` 
        WHERE username = '{username}'
    """
    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()

    for row in results:
        return row.email
    return None



@app.route("/book", methods=['GET','POST'])
def confirm_book():
    data = request.get_json()
    username = data['username']
    booking_details = {
            'provider_id': data['provider_id'],
            'date': data['date'],
            'start_time': data['start_time'],
            'end_time': data['end_time']
        }

    success = add_booking_to_user(username, booking_details)

    requester_email = get_user_email(username) 
    provider_email = get_user_email(data['provider_id'])
    send_email(f"Booking Confirmation: {booking_details}", requester_email)
    send_email(f"Booking Confirmation: {booking_details}", provider_email)

    # table_id = f"gomama-413222.{BQ_TABLE_ID}.{BQ_DATASET_ID}"
    # query = f"""
    #     SELECT credits
    #     FROM `{table_id}`
    #     WHERE username = '{username}'
    #     """
    

    if success:
        return jsonify({'message': 'Booking added successfully'}), 200
    else:
        return jsonify({'message': 'Failed to add booking'}), 500
    
def add_booking_to_user(username, booking_details):
    table_id = f"gomama-413222.{BQ_TABLE_ID}.{BQ_DATASET_ID}"
    query = f"""
        SELECT bookings
        FROM `{table_id}`
        WHERE username = '{username}'
        """
    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()

    updated_bookings = []
    for row in results:
        updated_bookings = list(eval(row.bookings))

    # Add the new booking
    updated_bookings.append(booking_details)

    logging.info(str(updated_bookings))

    # Update the user record with the new bookings list
    update_query = f"""
    UPDATE `{table_id}`
    SET bookings = "{str(updated_bookings)}"
    WHERE username = '{username}'
    """
    logging.info(update_query)
    update_job = client.query(update_query)
    update_job.result()  # Wait for the query to finish

    return update_job.state == "DONE"

# @app.route("/transfer", methods=['GET','POST'])
# def monetize():
#     return None




    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))