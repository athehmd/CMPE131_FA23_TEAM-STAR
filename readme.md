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