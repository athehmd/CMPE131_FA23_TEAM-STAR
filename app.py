import mariadb
from bcrypt import hashpw, checkpw, gensalt
import os
import logging
import requests
from db import get_db
from flask import Flask, request, render_template, redirect, url_for, jsonify

#Initialize Flask app
app = Flask(__name__)

#Create log file
logger = logging.getLogger("mylog")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logfile.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Connector to the database
conn = get_db()

# Constants
FAILURE = 1
EXIT = 2
SUCCESS = 0
serverUrl = 'http://127.0.0.1:5000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news')
def news():
    weather_data = get_weather("Williamston,Michigan")  
    return render_template('news.html', weather_data=weather_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        status = login_check(username, password)
        if status == SUCCESS:
            #user = request.form['nm']
            return redirect('/community')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')  # Create an HTML template for the login page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        status = signup_check(username, password)
        
        if status != 'FAILURE':
            # Successful signup, you can redirect the user to the login page or any other page
            return redirect('/login')
        
    # If the request method is GET or signup was not successful, render the signup page
    return render_template('signup.html')

@app.route('/permits_and_forms')
def permits_and_forms():
    return render_template('permits_and_forms.html')

@app.route('/city_calendar')
def city_calendar():
    return render_template('city_calendar.html')

def get_weather(city):
    api_key = "f6e4fee65fd681cfca40c3c5f6127f16"  # Replace with your API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'imperial'  # You can use 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx status codes)

        print("API Request URL:", response.url)
        print("API Response Status Code:", response.status_code)
        print("API Response Text:", response.text)

        data = response.json()

        weather_info = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }

        return weather_info

    except requests.RequestException as e:
        print("Error making API request:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None
    
@app.route('/community', methods=['GET', 'POST'])
def community():
    if request.method == 'POST':
        number = 1  # Change this to the desired page number
        content = request.form.get('editContent')

        # Make a POST request to the server to edit the content
        edit_response = requests.post(f'{serverUrl}/edit_community_page_text',
                                      json={'number': number, 'content': content})

        if edit_response.status_code == 200:
            # Optionally, you can fetch and display the updated content after editing
            get_response = requests.get(f'{serverUrl}/get_community_page_text')
            community_data = get_response.json().get('data', [])

            return render_template('community.html')

    # If it's a GET request or editing failed, render the page with the current content
    get_response = requests.get(f'{serverUrl}/get_community_page_text')
    community_data = get_response.json().get('data', [])
    try:
        # Check if the response contains JSON data
        community_data = get_response.json().get('data', [])
    except requests.exceptions.JSONDecodeError:
        # Handle the case when the response is not JSON or empty
        community_data = []
    return render_template('community.html')

#Checks given login information with stored database user login information
def login_check(username, password) -> int:
    """System login.

    Returns:
        0 for successful.
        1 for failure.
    """
    logger.info("Login. Getting user input")

    try:
        cursor = conn.cursor()
        # collect usernames and passwords
        user_search = "SELECT username, pwHash FROM userinfo"

        logger.info("Collect usernames and passwords")
        cursor.execute(user_search)

        users = cursor.fetchall()

        logger.info(f"Searching correct pw/username combination for {username}")
        
        for stored_username, stored_pw in users:
            
            if (username == stored_username) and checkpw(bytes(password, 'utf-8'), bytes(stored_pw)):
                cursor.close()
                logger.info(f"{username} is a member.")
                logger.info("User logged in.")

                return SUCCESS

        #click.echo("Wrong pw/username combination.")
        logger.error("Pw/Username doesn't exist. Execution halt.")
        cursor.close()
        return FAILURE
    
    except mariadb.Error as err:
        #click.echo(f"Execution halt {err}")
        logger.error(f"Execution halt {err}")

        return FAILURE
    
#Creates new user in database with given login information
def signup_check(username, password) -> str:
    logger.info("Gathering username.")
    
    logger.info("Gathering cursor.")
    cursor = conn.cursor()

    # first, hash the password for the user before storing
    logger.info("Hashing user password.")
    hashed_pw = hashpw(password.encode('utf-8'), gensalt())
    insert_user = "INSERT INTO userinfo VALUES (%s, %s, NOW())"
    user_data = (username, hashed_pw)

    # execute and commit
    try:
        logger.info("Insert new user into the database.")

        cursor.execute(insert_user, user_data)
        cursor.close()
        conn.commit()
        
    except mariadb.Error as err:
        logger.error(f"Failed to insert: {err}")
        return 'FAILURE'
    
    logger.info("User created.")
    return 'SUCCESS'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    logger.info("Close database connection.")
    conn.close()