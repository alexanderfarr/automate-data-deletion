from flask import Flask, request, Response, jsonify
import MySQLdb
import json
import logging
import formscripts as priv
import databreach as breach
from datetime import datetime
import pytz #needs to be added to Docker!

app = Flask(__name__)

# terminal commands to run flask app:
# export FLASK_APP=api.py
# flask run --host=0.0.0.0

def get_db_connection():
    #Use following line when running the webserver (this file) in a Docker container:
    connection = MySQLdb.connect("privacy-mysql", "root", "DockerPasswort!", "privacy-database")
    #Use following line when running the webserver (this file) locally:
    #connection = MySQLdb.connect("127.0.0.1", "root", "DockerPasswort!", "privacydatabase", port=3306)
    cursor = connection.cursor()
    return cursor, connection

@app.route('/data_remove', methods=["POST"])
def data_takedown():
    cursor, connection = get_db_connection()
    data = request.get_json()
    email_login = False
    email_pw = {}
    email_acxiom = {}
    email_infutor = {}
    email_advantagesolutions = {}
    email_alc = {}
    email_epsilon = {}
    email_databreach = {}
    title = data["title"]
    firstname = data["firstname"]
    lastname = data["lastname"]
    suffix = data["suffix"]
    email = data["email"]
    phone_num = data["phone_num"]
    street = data["street"]
    apt = data["apt"]
    city = data["city"]
    state = data["state"]
    country = data["country"]
    zip_code = data["zip_code"]
    cc_last4 = data["cc_last4"]
    data_del_msg = data["data_del_msg"]
    deviceAdID = data["deviceAdID"]
    privacyReg = data["privacyReg"]

    ####### Check for data breach  #######
    databreach = breach.request_answer(email)

    ####### Send emails for data breach and opt out  #######
    if "email_pw" in data:
        email_login = True
        email_pw = data["email_pw"]
        email_acxiom = priv.email_acxiom(email, email_pw, firstname, lastname, suffix, street, apt,  city, state, zip_code).content.decode('utf-8')
        email_infutor = priv.email_infutor(email, email_pw,street, apt,  city, state, zip_code).content.decode('utf-8')
        email_advantagesolutions = priv.email_advantagesolutions(email, email_pw, firstname, lastname, suffix).content.decode('utf-8')
        email_alc = priv.email_alc(email, email_pw, firstname, lastname, suffix, street, apt,  city, state, zip_code).content.decode('utf-8')
        email_epsilon = priv.email_epsilon(email, email_pw, firstname, lastname, suffix).content.decode('utf-8')
        email_databreach = priv.email_databreach(email, email_pw, databreach[0]).content.decode('utf-8')

    #############################################
    ####### privacy form script functions #######
    #############################################

    """ If you want to skip Selenium use these instead
    adColony = {}
    petco = {}
    chipotle = {}
    pipl = {}
    asl = {}
    bestBuy = {}
    """
    petco = json.dumps({"complete": priv.petco_delete(firstname, lastname, email, phone_num)})
    adColony = json.dumps({"complete": priv.adColony_DoNotSSP(email, firstname, lastname, privacyReg,
                                      deviceAdID)})
    chipotle = json.dumps({"complete": priv.chipotle_delete(firstname, lastname, email, phone_num,
                                    cc_last4)})
    pipl = json.dumps({"complete": priv.pipl_delete(firstname, lastname, email, phone_num,
                            data_del_msg)})
    asl = json.dumps({"complete": priv.asl_DD_formfill(firstname, lastname, street, city, state,
                               zip_code, phone_num, email)})
    bestBuy = json.dumps({"complete": priv.bestBuy_DD_formfill(firstname, lastname, country, street,
                                       city, zip_code, phone_num, email)})

    ####### Insert into database   #######
    tz_LA = pytz.timezone('America/Los_Angeles')
    datetime_LA = datetime.now(tz_LA)
    timestamp=datetime_LA.strftime("%H:%M:%S")

    sql = f"INSERT INTO privacydb (timestamp, adcolony, asl, bestbuy, chipotle, petco, pipl, email_acxiom, email_infutor, email_advantagesolutions, email_alc, email_epsilon, databreach) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, [timestamp, adColony, asl, bestBuy, chipotle, petco, pipl, email_acxiom, email_infutor, email_advantagesolutions, email_alc, email_epsilon, email_databreach])
    connection.commit()
    cursor.close()
    connection.close()

    return json.dumps({
        "adColony": adColony,
        "asl": asl,
        "best buy": bestBuy,
        "chipotle": chipotle,
        "petco": petco,
        "pipl": pipl,
        "databreach": email_databreach,
        "email_acxiom": email_acxiom,
        "email_infutor": email_infutor,
        "email_advantagesolutions": email_advantagesolutions,
        "email_alc": email_alc,
        "email_epsilon": email_epsilon
    }), 200
