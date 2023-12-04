# City_Of_Williamston

Useful Documentation:

[Click](https://click.palletsprojects.com/en/8.1.x/quickstart/)

[MariaDB](https://www.mariadbtutorial.com/)

[HeidiSQL](https://www.heidisql.com/)

[BCrypt](https://github.com/pyca/bcrypt/)


# Usage
1. Download and install HeidiSQL from Above
2. Install the necessary packages

```
pip install -r requirements.txt
```

3. Create a server using HeidiSQL.

4. Alter the credentials in db.py to reflect your HeidiSQL server credentials. For example:

```
user="root",
password="12345",
host="127.0.0.1",
port=3306,
database="City_Of_Williamston"
```

5. Run `db.py`.

```
python3 db.py
```

To create the database:

1. In `mariaDB`, do:

```
source PATH_TO_FILE
```

where PATH_TO_FILE is the path to `create_db.sql`


To use the application:

```
python3 main.py
```
.  
.  
.  
To run the backend, we do it locally now for testing. We run the flask server flask_server.py locally. Since it is local, however, we need CORS to give permission so that websites can access our local server.
In the command line, run
```
pip install Flask-CORS
```
Then, to start the server, go to the correct directory in the command line and run
```
python flask_server.py
```
to start the server. Make sure that db.py is in the same folder as flask_server.py.
Then when using the cms community page with it make sure to change the server url to the url of the flask server you just started. it should say the url in the command line after you wrote python flask_server.py.
