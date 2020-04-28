### Project description
This project is a group project for the course backend web architecture at UC Berkeley's School of Information. The API is allows users to easily request their information from several websites and to request how the data is handled, e.g. that it should be deleted, not sold etc.

### Supported websites
- Acxiom (by email - they will ask you to send them a photo id by email)
- adColony
- Advantagesolutions (by email)
- ALC (by email)
- AnalyticsIQ
- ASL
- Best Buy
- Booking.com
- Chipotle
- Epsilon (by email)
- Infutor (by email)
- LinkedIn
- Petco
- Pipl

### Instructions on input
Here you can find instructions on finding your Advertising ID https://www.adcolony.com/privacy-policy/finding-advertising-id/

This is the way you need to input your data. You can leave any field blank that does not apply to you. However, this could lead to errors in requesting data from some websites.
email_pw is voluntary to be used and would allow us to send an email on your behalf to websites that do not have a data removal form.
```
r = requests.post('http://localhost:5000/data_remove', json={
    "title": "Mr",
    "firstname": "Max",
    "lastname": "Exampleperson",
    "suffix": "",
    "email": "max.exampleperson@hotmail.com",
    "phone_num": "8532197128",
    "street": "32 University Avenue",
    "apt": "",
    "city": "Berkeley",
    "state": "CA",
    "country": "United States",
    "zip_code": "94738",
    "cc_last4": "",
    "data_del_msg": "Delete my data please!",
    "deviceAdID": "5D935A52-79E1-420E-A814-DC75351CBA97",
    "privacyReg": "CCPA",
    "email_pw": "password"
    })
```
### Use following instructions to run everything in a Docker container:
Creating a new network for api container, mysql database container and selenium container

`docker network create privacy-network`

To set up Selenium container adjust the filepath and run this:

`docker run --name selenium-container -d -p 4444:4444 -p 5900:5900 -v PATH/ON/YOUR/HOST/COMPUTER/TO/data-privacy-api/selenium/dev/shm:/dev/shm --network privacy-network selenium/standalone-chrome-debug`

Example for Lara's computer using Windows command prompt:

`docker run --name selenium-container -d -p 4444:4444 -p 5900:5900 -v C:/Users/Lara/Documents/Berkeley/Back-End/data-privacy-api/selenium/dev/shm:/dev/shm --network privacy-network selenium/standalone-chrome-debug`

Use VNC to view what's going on inside the Selenium container. Open VNC viewer and enter 127.0.0.1:5900 in address bar, the password is `secret`.

To set up MySQL container, edit the filepath and run:

`docker run --name privacy-mysql -e MYSQL_ROOT_PASSWORD=DockerPasswort! -e MYSQL_DATABASE=privacy-database -v PATH/ON/YOUR/HOST/COMPUTER/TO/data-privacy-api/db/db_records:/var/lib/mysql -v PATH/ON/YOUR/HOST/COMPUTER/TO/data-privacy-api/db/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d --network privacy-network -dit -p 3306:3306 mysql:latest --default-authentication-plugin=mysql_native_password`

Example for Lara's computer using Windows command prompt:

`docker run --name privacy-mysql -e MYSQL_ROOT_PASSWORD=DockerPasswort! -e MYSQL_DATABASE=privacy-database -v C:/Users/Lara/Documents/Berkeley/Back-End/data-privacy-api/db/db_records:/var/lib/mysql -v C:/Users/Lara/Documents/Berkeley/Back-End/data-privacy-api/db/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d --network privacy-network -dit -p 3306:3306 mysql:latest --default-authentication-plugin=mysql_native_password`

If you want to query the database directly:

`docker exec -it privacy-mysql bash`

`mysql -uroot -p`

Enter password: `DockerPasswort!`

`use privacy-database;`

Voila, start running queries on the 'privacydb' table!

Such as: `show columns from privacydb;` (to see all the column names) or `select * from privacydb;` (to see all the entries in the table).

To set up Flask app container for the main api:

`cd main_api`

`docker build -t privacy_api_image .`

`docker run -dit --name=privacy_api -e FLASK_APP=api.py -p 5000:5000 -v PATH/ON/YOUR/HOST/COMPUTER/TO/data-privacy-api/main_api:/app --network privacy-network privacy_api_image`

Example for Lara's computer using Windows command prompt:

`docker run -dit --name=privacy_api -e FLASK_APP=api.py -p 5000:5000 -v C:/Users/Lara/Documents/Berkeley/Back-End/data-privacy-api/main_api:/app --network privacy-network privacy_api_image`

To see what's going on inside the container:

`docker logs -f privacy_api`

To set up Flask app container for the e-mail api:

`cd email_api`

`docker build -t email_api_image .`

`docker run -dit --name=email_api -e FLASK_APP=send_email.py -p 5001:5000 -v PATH/ON/YOUR/HOST/COMPUTER/TO/data-privacy-api/email_api:/app --network privacy-network email_api_image`

Example for Lara's computer using Windows command prompt:

`docker run -dit --name=email_api -e FLASK_APP=send_email.py -p 5001:5000 -v C:/Users/Lara/Documents/Berkeley/Back-End/data-privacy-api/email_api:/app --network privacy-network email_api_image`

To see what's going on inside the container:

`docker logs -f email_api`

### If you need to start from scratch

Stop all running Docker containers.

`docker system prune`

Choose 'y', when asked if you want to continue.

Delete everything in db/db_records.

Delete everything in your trash can/recycling bin if you're fancy.

Start again.

-------------------
### Example how it worked for Alexander Farr with Command prompt with Windows:
```
docker network create privacy-network
docker run --name selenium-container -d -p 4444:4444 -p 5900:5900 -v Folder:/dev/shm selenium/standalone-chrome-debug
docker run -d --name privacy-mysql -e MYSQL_ROOT_PASSWORD=DockerPasswort! -e MYSQL_DATABASE=privacy-database -v C:\Users\Alexa\OneDrive\Backend_web_architecture\github_repos\data-privacy-api\db\db_records:/var/lib/mysql -v C:\Users\Alexa\OneDrive\Backend_web_architecture\github_repos\data-privacy-api\db\docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d --network privacy-network -dit -p 3306:3306 mysql:latest --default-authentication-plugin=mysql_native_password
docker exec -it privacy-mysql bash
cd main_api
docker build -t privacy_api_image .
docker run -dit --name=privacy_api -e FLASK_APP=api.py -p 5000:5000 -v main_api:/app --network privacy-network privacy_api_image
docker logs -f privacy_api
```
-------------------
## Use following instructions to run the database locally to be able to debug faster (does not include taskrunner and redis):

Open another terminal

`export FLASK_APP=api.py`

`flask run --host=0.0.0.0`

### Set up SQL:

```
CREATE DATABASE privacydatabase;
use privacydatabase;
CREATE TABLE privacydb (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    timestamp TIME,
    adcolony JSON NOT NULL,
    asl JSON NOT NULL,
    bestbuy JSON NOT NULL,
    booking JSON NOT NULL,
    chipotle JSON NOT NULL,
    instantcheckmate JSON NOT NULL,
    intelius JSON NOT NULL,
    linkedin JSON NOT NULL,
    petco JSON NOT NULL,
    pipl JSON NOT NULL,
    atlantic JSON NOT NULL,
    databreach JSON NOT NULL
);
```
### Recommendations on error:
Please note that to access the API of https://haveibeenpwned.com a valid API key needs to be purchased which is $3 for one month. Update this in the `databreach.py` file.

### Recommendations when you want to include other pages
Websites that do not have a ReCaptcha code are easier to be automated. For some websites you can avoid the ReCaptcha by acccessing it in the incognito mode.

### Steps to improve the program
- Automatically look at supported website's DOM (e.g. every week) and compare it with the stored website's DOM. If there is a change in the DOM, a notification could be sent so that the admin can look into the changes and potentially update the Selenium so that it still works after the changes.
