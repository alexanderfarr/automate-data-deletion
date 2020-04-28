# IMPORTS
import os
import time
import selenium
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


################## WEBSCRIPTS ######################

def get_driver():
    driver = webdriver.Remote(
        command_executor='http://selenium-container:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)

    return driver

## AdColony do not sell -> missing: validation check
def adColony_DoNotSSP(email, firstname, lastname, privacyReg, deviceAdID):
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://www.adcolony.com/privacy-policy/")
    time.sleep(1)  # need time for cookie btn to pop up
    driver.find_element_by_id("CybotCookiebotDialogBodyLevelButtonAccept"
                              ).click()  # cookie accept -> UGH
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight-1500);")
    select = Select(driver.find_element_by_name('form-options'))
    select.select_by_index(3)
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight-2200);")
    # email input
    driver.find_element_by_xpath(
        "(//span[@class='wpcf7-form-control-wrap email']/input[@id='field-email' and @name='email'])[3]"
    ).send_keys(email)
    # firstname input
    driver.find_element_by_xpath(
        "(//span[@class='wpcf7-form-control-wrap firstname']/input[@id='field-name' and @name='firstname'])[3]"
    ).send_keys(firstname)
    # lastname input
    driver.find_element_by_xpath(
        "(//span[@class='wpcf7-form-control-wrap lastname']/input[@id='field-lastname' and @name='lastname'])[3]"
    ).send_keys(lastname)

    # AdColony asks which under which privacy regulation are you choosing to excercise rights
    # radial button with options: GDPR (EU), CCPA (CA), or None
    if privacyReg == "GDPR":
        pass  # GDPR radial button is default
    elif privacyReg == "CCPA":
        driver.find_element_by_xpath(
            "(//span[@class='wpcf7-list-item']/input[@name='are-resident-eea' and @value='CCPA (California Resident)'])[3]"
        ).click()
    elif privacyReg == "OTHER":
        driver.find_element_by_xpath(
            "(//span[@class='wpcf7-list-item last']/input[@name='are-resident-eea' and @value='None of the Above'])[3]"
        ).click()
    else:  # default to GDPR ->
        pass  # GDPR radial button is default
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight-1715);")
    # deviceAdID input
    driver.find_element_by_xpath(
        "(//div[@class='row xs-bottom-spacing']/div[@class='col-md-12']/span[@class='wpcf7-form-control-wrap device-advertising-id']/input[@name='device-advertising-id'])[3]"
    ).send_keys(deviceAdID)
    # authorize -> click
    driver.find_element_by_xpath(
        "(//div[@class='row xs-bottom-spacing']/div[@class='col-md-12']/span[@class='wpcf7-form-control-wrap accurate-authorize']/span[@class='wpcf7-form-control wpcf7-acceptance'])[3]"
    ).click()
    # consent-for-this-request -> click
    driver.find_element_by_xpath(
        "(//div[@class='row xs-bottom-spacing']/div[@class='col-md-12']/span[@class='wpcf7-form-control-wrap consent-for-this-request']/span[@class='wpcf7-form-control wpcf7-acceptance'])[3]"
    ).click()
    # name -> signature -> first+ " " + last
    driver.find_element_by_xpath(
        "(//span[@class='wpcf7-form-control-wrap signature']/input[@name='signature'])[3]"
    ).send_keys(firstname + " " + lastname)
    # Submit Button -> KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    # driver.find_element_by_xpath(
    #     "(//div[@class='row']/div[@class='col-md-12']/p/input[@id='btn-submit'])[3]"
    # ).click()
    driver.quit()
    return True


## Petco data delete -> Complete
def petco_delete(firstname, lastname, email, phone_num):
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://dsar.oncentrl.com/petco_rightsrequest.html"
               )  # link to data delete
    # use Xpath finder chrome extension,
    # delete data radio button
    driver.find_element_by_xpath(
        "//label[@for='requestType2' and @class='custom-control-label']"
    ).click()
    # ? - filling out request on behalf of someone else
    #driver.find_element_by_xpath("//label[@for='authorizedParty' and @class='custom-control-label']").click()
    driver.find_element_by_id("firstName").send_keys(firstname)
    driver.find_element_by_id("lastName").send_keys(lastname)
    driver.find_element_by_id("userEmail").send_keys(email)
    driver.find_element_by_id("phoneNumber").send_keys(phone_num)
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight-200);")
    time.sleep(1)
    driver.find_element_by_xpath(
        "//select[@id='vmAttribute3']/option[text()='California']").click()
    driver.find_element_by_xpath(
        "//label[@for='not_applicable' and @class='custom-control-label']"
    ).click()
    driver.find_element_by_xpath(
        "//label[@for='acknowledgement' and @class='custom-control-label']"
    ).click()

    # Submit Button -> KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    # driver.find_element_by_xpath("//button[@type='submit' and @class='btn btn-primary btn-block w-25 mr-auto']").click()
    # Check if the submission was successful
    tar_elem = driver.find_element_by_id("dsar_success_message")
    is_active = "visibility: visible; display: block;" in tar_elem.get_attribute(
        "style")
    if is_active == True:
        print("Petco: Submitted deletion request successfully")
        driver.quit()
        return True
    else:
        print("Deletion request unsuccessful")
        driver.quit()
        return False


## LinkedIn data delete -> Complete
def linkedIn_DataDelete(firstname, lastname, email, data_del_msg):
    # make sure to install chrome driver exe in /usr/local/bin or else
    # you will need to do funky things with PATH to get driver to work
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://www.linkedin.com/help/linkedin/ask/TS-DDF"
               )  # link to data delete form
    driver.find_element_by_id("dyna-firstname").send_keys(
        firstname)  # firstname textfield
    driver.find_element_by_id("dyna-lastname").send_keys(
        lastname)  # lastname textfield
    driver.find_element_by_id("dyna-email").send_keys(email)  # email textfield
    driver.find_element_by_id("dyna-delete_details").send_keys(
        data_del_msg)  # details input textfield
    time.sleep(4)
    # Submit Button -> KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    # driver.find_element_by_id("dynaform-submit").send_keys(Keys.ENTER) # submit button
    # Check if the submission was successful
    # if works, it takes you -> success page: https://www.linkedin.com/help/linkedin/thankyou
    time.sleep(5)  # wait to load the success page
    if driver.current_url == "https://www.linkedin.com/help/linkedin/thankyou":
        print("Submitted deletion request successfully")
        driver.quit()
        return True
    print("Deletion request unsuccessful")
    driver.quit()
    return False


## Chipotle data delete -> Missing: validation check
def chipotle_delete(firstname, lastname, email, phone_num, cc_last4):
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://www.chipotle.com/datarequest")  # link to data delete
    driver.find_element_by_xpath(
        "//select[@id='00N0P000007SHkz']/option[text()='Delete the personal information you store about me']"
    ).click()
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight-1500);")
    driver.find_element_by_xpath(
        "//input[@id='00NU0000002OMYL' and @name='00NU0000002OMYL']"
    ).send_keys(firstname)
    driver.find_element_by_xpath(
        "//input[@id='00NU0000002OMYN' and @name='00NU0000002OMYN']"
    ).send_keys(lastname)
    driver.find_element_by_xpath(
        "//input[@id='00NU0000002OMYK' and @name='00NU0000002OMYK']"
    ).send_keys(email)
    driver.find_element_by_xpath(
        "//input[@id='00NU0000002OMYO' and @name='00NU0000002OMYO']"
    ).send_keys(phone_num)
    driver.find_element_by_xpath(
        "//input[@id='00N2D000003C9J2' and @name='00N2D000003C9J2']"
    ).send_keys(cc_last4)
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight-1000);")
    driver.find_element_by_xpath(
        "//input[@type='checkbox' and @id='caliResident']").click()
    driver.find_element_by_xpath(
        "//input[@type='checkbox' and @id='verificationEmail']").click()
    # Submit Button -> KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    #driver.execute_script("document.getElementsByClassName('c-button')[0].click()")
    ## if no errors raised return True -> no conifrmation screen....
    time.sleep(7)
    driver.quit()
    return True


## PIPL data delete -> Complete
def pipl_delete(firstname, lastname, email, phone_num, data_del_msg):
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://pipl.com/personal-information-removal-request"
               )  # link to data delete
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    driver.find_element_by_xpath(
        "//div[@data-reactid='.hbspt-forms-0.1:$0.$firstname']/input[@id='firstname-844a13ea-6091-4d83-a2bd-7d8fb9fed744' and @name='firstname']"
    ).click()
    driver.find_element_by_xpath(
        "//div[@data-reactid='.hbspt-forms-0.1:$0.$firstname']/input[@id='firstname-844a13ea-6091-4d83-a2bd-7d8fb9fed744' and @name='firstname']"
    ).send_keys(firstname)
    driver.find_element_by_id(
        "lastname-844a13ea-6091-4d83-a2bd-7d8fb9fed744").send_keys(lastname)
    driver.find_element_by_id(
        "email-844a13ea-6091-4d83-a2bd-7d8fb9fed744").send_keys(email)
    driver.find_element_by_id(
        "message-844a13ea-6091-4d83-a2bd-7d8fb9fed744").send_keys(data_del_msg)
    # Submit Button -> KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    # driver.find_element_by_xpath(
    #     "//input[@type='submit' and @value='Submit']").click()
    # Check if the submission was successful
    time.sleep(3)
    success_text = "Thank you! Your request is being processed by our Customer Support team. They may need to reach out to you via email for additional details. Please, check your email for correspondence over the next few days."
    if (success_text in driver.page_source):
        return True
    else:
        return False


## ASL data delete -> Missing: validation check
def asl_DD_formfill(firstname, lastname, street, city, state, zip_code,
                    phone_num, email):
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://aslmarketing.com/opt-out/")  # link to data delete form
    driver.find_element_by_id("et_pb_contact_first_0").send_keys(
        firstname)  # firstname textfield
    driver.find_element_by_id("et_pb_contact_last_0").send_keys(
        lastname)  # lastname textfield
    driver.find_element_by_id("et_pb_contact_address_0").send_keys(
        street)  # street address textfield
    driver.find_element_by_id("et_pb_contact_city_0").send_keys(
        city)  # city textfield
    driver.find_element_by_id("et_pb_contact_state_0").send_keys(
        state)  # state textfield
    driver.find_element_by_id("et_pb_contact_zip_0").send_keys(
        zip_code)  # zipcode textfield
    driver.find_element_by_id("et_pb_contact_phone_0").send_keys(
        phone_num)  # phone textfield
    driver.find_element_by_id("et_pb_contact_email_0").send_keys(
        email)  # email textfield
    # Submit Button -> KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    #driver.find_element_by_id("et_builder_submit_button").send_keys(Keys.ENTER) # submit button - NEED TO CONFIRM FUNCTIONALITY
    time.sleep(4)
    driver.quit()
    return True


## BestBuy data delete -> Complete
def bestBuy_DD_formfill(firstname, lastname, country, street, city, zip_code,
                        phone_num, email):
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://www.bestbuy.com/sentry/intake?context=ca&type=delete"
               )  # link to data deletion form
    driver.find_element_by_id("firstName").send_keys(
        firstname)  # firstname textfield
    driver.find_element_by_id("lastName").send_keys(
        lastname)  # lastname textfield
    driver.find_element_by_id("addressLine1").send_keys(
        street)  # address textfield
    driver.find_element_by_id("city").send_keys(city)  # city textfield
    driver.find_element_by_id("zipCode").send_keys(
        zip_code)  # zipcode textfield
    driver.find_element_by_id("phone").send_keys(phone_num)  # phone textfield
    driver.find_element_by_id("email").send_keys(email)  # email textfield
    driver.find_element_by_xpath(
        "//*[@id='app']/div/div[2]/div/div/div[1]/div/div/div/form/div[13]/div"
    ).click()  #Residency checkbox
    select = Select(driver.find_element_by_id("state"))  #state dropdown choice
    select.select_by_visible_text("CA - California")  #state dropdown choice
    # Submit Button -> KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    # driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div/div[1]/div/div/div/form/div[14]/button[1]").click() #submit button
    time.sleep(4)
    #try & except block to see if deletion request was successful
    try:
        assert driver.page_source.find(
            "You've completed the first step to delete your personal information."
        )
        print("BestBuy request completed!")
        return True

    except:
        print("BestBuy request failed. Please try again.")
        return False
    driver.quit()
    return False


## Booking data deletion form
def booking_DD_formfill(email):
    # make sure to install chrome driver exe in /usr/local/bin or else
    # you will need to do funky things with PATH to get driver to work
    driver = get_driver()
    #driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    driver.get("https://www.booking.com/content/ccpa.html"
               )  # link to data deletion form
    driver.find_element_by_id("email").send_keys(email)  # email textfield
    driver.find_element_by_xpath(
        "//*[@id='b2contentPage']/div[4]/div/div/form/div[1]/label[1]").click(
        )  # checkbox
    # KEEP THIS DISABLED BC IT ACTUALLY SUBMITS
    # driver.find_element_by_xpath("//*[@id='b2contentPage']/div[4]/div/div/form/p[7]/button").click() #submit button
    time.sleep(4)
    #try & except block to see if deletion request was successful
    try:
        assert driver.page_source.find(
            "You've completed the first step to delete your personal information."
        )
        print("booking.com request completed!")
        return True
    except:
        print("booking.com request failed. Please try again.")
        return False
    driver.quit()
    return False

def email_acxiom(email, email_pw, firstname, lastname, suffix, street, apt,  city, state, zip_code):
    email_result = requests.post('http://email_api:5000/email', json={
        "from_email": email,
        "password": email_pw,
        "to_email": "consumeradvo@acxiom.com",
        "subject": "Acxiom Opt out request for: "+firstname+" "+lastname+" ("+email+")",
        "message": "Dear Acxiom Team, I would like you to remove my information. This is my name: "+firstname+" "+lastname+" "+suffix+". This is my email: "+email+ ". This is my address: Street: "+street+", Apartment: "+apt+", City: "+city+", State: "+state+", Zip: "+zip_code
        })
    return email_result

def email_infutor(email, email_pw, street, apt,  city, state, zip_code):
    email_result = requests.post('http://email_api:5000/email', json={
        "from_email": email,
        "password": email_pw,
        "to_email": "Compliance@Infutor.com",
        "subject": "Infutor Opt out request for: "+email,
        "message": "Dear Infutor Team, I would like you to remove my information. This is my email: "+email+ ". This is my address: Street: "+street+", Apartment: "+apt+", City: "+city+", State: "+state+", Zip: "+zip_code
        })
    return email_result

def email_advantagesolutions(email, email_pw, firstname, lastname, suffix):
    email_result = requests.post('http://email_api:5000/email', json={
        "from_email": email,
        "password": email_pw,
        "to_email": "privacy@advantagesolutions.net",
        "subject": "AdvantageSolutions Opt out request for: "+firstname+" "+lastname+" ("+email+")",
        "message": "Dear AdvantageSolutions Team, I would like you to remove my information. This is my name: "+firstname+" "+lastname+" "+suffix+". This is my email: "+email+ ". Thank you."
        })
    return email_result

def email_alc(email, email_pw, firstname, lastname, suffix,street, apt, city, state, zip_code):
    email_result = requests.post('http://email_api:5000/email', json={
        "from_email": email,
        "password": email_pw,
        "to_email": "privacy.officer@alc.com",
        "subject": "Alc Opt out request for: "+firstname+" "+lastname+" ("+email+")",
        "message": "Dear Alc Team, I would like you to remove my information. This is my name: "+firstname+" "+lastname+" "+suffix+". This is my email: "+email+ ". This is my address: Street: "+street+", Apartment: "+apt+", City: "+city+", State: "+state+", Zip: "+zip_code
        })
    return email_result

def email_epsilon(email, email_pw, firstname, lastname, suffix):
    email_result = requests.post('http://email_api:5000/email', json={
        "from_email": email,
        "password": email_pw,
        "to_email": "privacy@epsilon.com",
        "subject": "Epsilon Opt out request for: "+email,
        "message": "Dear Epsilon Team, I would like you to remove my information. This is my email: "+email+". Thank you, "+firstname+" "+lastname+" "+suffix
        })
    return email_result

def email_databreach(email, email_pw, databreach_text):
    email_result = requests.post('http://email_api:5000/email', json={
        "from_email": email,
        "password": email_pw,
        "to_email": email,
        "subject": "Results from Databreach check for your email: "+email,
        "message": databreach_text
        })
    return email_result
