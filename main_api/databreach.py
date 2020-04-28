import requests
import time
import argparse
# Set terminal colors
green = '\033[92m'
warning = '\033[93m'
red = '\033[91m'
end = '\033[0m'

def request_answer(email):
    return_text=""
    breach_details=""
    sleep = 0.1
    #Watch out, API key in plain text here:
    check = requests.get("https://haveibeenpwned.com/api/v3/breachedaccount/"+email+"?truncateResponse=false",  headers={'hibp-api-key': "ebe0d675d1bb4afeb5ac33af2b92e86f"})
    if str(check.status_code) == "404": # The address has not been breached.
        #print( green + "[i] " + email + " has not been breached." + end)
        return_text=return_text + email + " has not been breached."
        time.sleep(sleep) # sleep so that we don't trigger the rate limit
        return return_text, breach_details
    elif str(check.status_code) == "200": # The address has been breached!
        output=check.json()
        #print( red + "[!] " + email + " has been breached!" + end)
        return_text=return_text+ email + " has been breached!          "
        #print(check.text) #Uncomment this line to see all details
        breach_details=check.text
        counter=0
        numberOfBreaches=0
        #print each breach separately:
        while(counter>=0):
            try:
                output[counter]
                counter=counter+1
                numberOfBreaches=numberOfBreaches+1
            except IndexError:
                counter=-1
        #print("Your email is part of following breaches: ")
        return_text=return_text+"Your email is part of following breaches: "
        counter2=0
        while counter2+1 <numberOfBreaches:
            #print(output[counter2]["Name"]+", ")
            return_text=return_text+output[counter2]["Name"]+", "
            counter2=counter2+1
        #print(output[counter2]["Name"]) #new line after loop
        return_text=return_text+output[counter2]["Name"]+"        "
        #print("You can find details at https://haveibeenpwned.com/")
        return_text=return_text+"You can find details at https://haveibeenpwned.com/"
        counter2=0
        firstOccurence=True
        while counter2+1 <numberOfBreaches:
            if(len(output[counter2]["Domain"])>0):
                if(firstOccurence):
                    #print(" and here:", output[counter2]["Domain"]+" ")
                    return_text=return_text+" and here:"+output[counter2]["Domain"]+", "
                else:
                    #print(output[counter2]["Domain"]+", ")
                    return_text=return_text+output[counter2]["Domain"]
                firstOccurence=False
            counter2=counter2+1
        if(len(output[counter2]["Domain"])>0):
            if(firstOccurence):
                #print(" and here:", output[counter2]["Domain"])
                return_text=return_text+" and here:", output[counter2]["Domain"]
            else:
                #print(output[counter2]["Domain"]) #new line after loop
                return_text=return_text+output[counter2]["Domain"]
        time.sleep(sleep) # sleep so that we don't trigger the rate limit
        return return_text, breach_details
    else:
        print( warning + "[!] Something went wrong while checking " + email + end)
        return_text=return_text + " Something went wrong while checking " + email
        time.sleep(sleep) # sleep so that we don't trigger the rate limit
        return return_text, breach_details
