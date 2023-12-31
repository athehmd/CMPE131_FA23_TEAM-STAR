# City_Of_Williamston

Useful Documentation:

[MariaDB](https://www.mariadbtutorial.com/)

[HeidiSQL](https://www.heidisql.com/)

[BCrypt](https://github.com/pyca/bcrypt/)

[VirtualEnv](https://virtualenv.pypa.io/en/latest/index.html)

[Flask](https://flask.palletsprojects.com/en/3.0.x/)

# Usage
To create the database:

1. Download and install HeidiSQL from Above

2. Create a server using HeidiSQL.

3. Alter the credentials in db.py to reflect your HeidiSQL server credentials. For example:

```
user="root",
password="12345",
host="127.0.0.1",
port=3306,
database="City_Of_Williamston"
```

4. Run `db.py`.

```
python3 db.py
```

5. In `mariaDB`, do:

```
source PATH_TO_FILE
```

where PATH_TO_FILE is the path to `create_db.sql`


To use the application:

1. In cmd navigate to this directory

2. Create a virtual environment (where venv is your virtual environment name):

```
python -m virtualenv venv
```

```
venv\scripts\activate
```

3. Install the necessary packages

```
pip install -r requirements.txt
```

```
python3 app.py
```




