import mariadb
from bcrypt import hashpw, checkpw, gensalt
import os
import click
import logging
from db import get_db
from flask import Flask, request, render_template, redirect, url_for

# ... (your existing imports)

# Initialize Flask app
app = Flask(__name__)

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

'''def signup_check() -> str:
    logger.info("Gathering username.")
    username = click.prompt("Enter your username: ", str)

    password = click.prompt("Enter your password: ", str, hide_input=True)
    
    logger.info("Gathering cursor.")
    cursor = conn.cursor()

    # first, hash the password for member before storing
    logger.info("Hashing user password.")
    hashed_pw = hashpw(bytes(password, 'utf-8'), gensalt())
    insert_user = "INSERT INTO userinfo VALUES (%s, %s, NOW())"
    user_data = (username, hashed_pw)

    # execute and commit
    try:
        logger.info("Insert new user into database,")

        cursor.execute(insert_user, user_data)
        cursor.close()
        conn.commit()
        
    except mariadb.Error as err:
        logger.error(f"Failed to insert: {err}")
        click.echo(f"Execution halt: {err}")
        return FAILURE
    
    logger.info("Member created.")
    return username'''


def user_actions_route() -> int:
    prompt = '''
        Here's what you can do:
        [1] function name here
        [2] function name here
        [3] function name here
        [4] function name here
        [5] Exit
    '''

    click.echo(prompt)

    c = click.getchar()

    if c == '1':
        print('function call here')
    elif c == '2':
        print('function call here')
    elif c == '3':
        print('function call here')
    elif c == '4':
        print('function call here')
    else:
        return FAILURE
    
# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Create an HTML template for the home page

# Route for signup
'''@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        status = signup_check()
        return render_template('login.html')
    else:
        return render_template('signup.html')  # Create an HTML template for the signup page'''
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        status = signup_check(username, password)
        
        if status != 'FAILURE':
            # Successful signup, you can redirect the user to the login page or any other page
            return render_template('login.html')
        
    # If the request method is GET or signup was not successful, render the signup page
    return render_template('signup.html')


def signup_check(username, password) -> str:
    logger.info("Gathering username.")

    # You can remove this line as we're getting username from the form directly
    # username = click.prompt("Enter your username: ", str)

    # You can remove this line as well, as we're getting the password from the form directly
    # password = click.prompt("Enter your password: ", str, hide_input=True)
    
    logger.info("Gathering cursor.")
    cursor = conn.cursor()

    # first, hash the password for the member before storing
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
        click.echo(f"Execution halt: {err}")
        return 'FAILURE'
    
    logger.info("Member created.")
    return 'SUCCESS'

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    print('salam1')
    if request.method == 'POST':
        #click.echo("\nLogging you in.\n")
        username = request.form['username']
        password = request.form['password']
        print('salam2')
        status = login_check(username, password)
        if status == SUCCESS:
            #user = request.form['nm']
            return redirect('/cms_community_page.html')
            #return render_template('user_actions.html')
        else:
            return render_template('login_failure.html')
    else:
        return render_template('login.html')  # Create an HTML template for the login page
    
def login_check(username, password) -> int:
    """System login.

    Returns:
        0 for successful.
        1 for failure.
    """
    logger.info("Login. Getting user input")
    #username = click.prompt("Enter your username: ", str)
    #password = click.prompt("Enter your password: ", str, hide_input=True)

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

# Route for user actions
@app.route('/user_actions', methods=['POST'])
def user_actions():
    action = user_actions_route()
    if action == FAILURE:
        return render_template('user_actions_failure.html')
    else:
        return render_template('user_actions.html')

# ... (other routes as needed)

@app.route('/edit_community_page_text', methods=['POST'])
def edit_community_page_text():
    db = get_db()
    cursor = db.cursor()

    number = request.json.get('number')
    content = request.json.get('content')

    if number is not None and content is not None:
        # Update statement
        update_query = "UPDATE cmsCommunityPage SET content = %s WHERE number = %s"

        # Execute the update query
        cursor.execute(update_query, (content, number))
        db.commit()

        cursor.close()
        return jsonify({"message": "Data updated successfully"})
    else:
        cursor.close()
        return jsonify({"error": "Invalid request data"})

#endpoint to get cms community page text from database
@app.route('/get_community_page_text', methods=['GET'])
def get_community_page_text():
    db = get_db()  # Use the function from database.py to connect to the database
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM cmsCommunityPage")
        data = cursor.fetchall()
        return jsonify({'data': data})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        #db.close()

# Main application loop
if __name__ == "__main__":
    app.run(debug=True)
    logger.info("Close database connection.")
    conn.close()