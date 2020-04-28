import requests
import json

def test():
    r = requests.post('http://localhost:5000/data_remove', json={
        "title": "Mr",
        "firstname": "Max",
        "lastname": "Musterperson",
        "suffix": "",
        "email": "privacy_api@hotmail.com",
        "email_pw": "SecretPassword",
        "phone_num": "8572720151",
        "street": "11 University Avenue",
        "apt": "",
        "city": "Berkeley",
        "state": "CA",
        "country": "United States",
        "zip_code": "94709",
        "cc_last4": "",
        "data_del_msg": "Delete my data please",
        "deviceAdID": "5D575A52-77G9-230E-A814-DC34351CBA97",
        "privacyReg": "CCPA"
        })

    """
    r = requests.post('http://localhost:5001/email', json={
        "from_email": "privacy_api@hotmail.com",
        "password": "SecretPassword",
        "to_email": "privacy_api@hotmail.com",
        "subject": "Data deletion",
        "message": "Delete my data please"
        })
    """

if __name__ == "__main__":
    test()
