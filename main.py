import mariadb
from bcrypt import hashpw, checkpw, gensalt
import os
import click
import logging
from db import get_db

#creating log file
logger = logging.getLogger("mylog")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logfile.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

conn = get_db() #connector to database

logger.info("Initiated application")

FAILURE = 1
EXIT = 2
SUCCESS = 0

def signup() -> str:
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
    return username

def login() -> int:
    """System login.

    Returns:
        0 for successful.
        1 for failure.
    """
    logger.info("Login. Getting user input")
    username = click.prompt("Enter your username: ", str)
    password = click.prompt("Enter your password: ", str, hide_input=True)

    global USERNAME

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

                USERNAME = username
                return SUCCESS

        click.echo("Wrong pw/username combination.")
        logger.error("Pw/Username doesn't exist. Execution halt.")
        cursor.close()
        return FAILURE
    
    except mariadb.Error as err:
        click.echo(f"Execution halt {err}")
        logger.error(f"Execution halt {err}")

        return FAILURE
    
def user_actions() -> int:
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
    
def City_Of_Williamston():
    while True:
        
        prompt = '''
        What are you trying to do? \n\
        [1] Signup
        [2] Login.
        [3] Exit.
        '''
        
        click.echo(prompt, nl=False)

        c = click.getchar()

        if c == '1':
            click.echo("Signing you up.")
            status = signup()
            click.echo("Successfully signed up.")
            c = 2
            
        elif c == '2':
            click.echo("Logging you in.")
            status = login()
            click.echo("Successfully logged in.")
            action = user_actions()
            
            while action != FAILURE:
                action = user_actions()
        
        elif c == '3':
            click.echo("Bye!")
            break
        
        else:
            return City_Of_Williamston()
    

# main application loop
if __name__ == "__main__":
    City_Of_Williamston()
    logger.info("Close database connection.")
    conn.close()