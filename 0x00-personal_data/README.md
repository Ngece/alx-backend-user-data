filtered_logger.py              Contains functions that filter sensitive data.
    function called filter_datum that returns the log message obfuscated:
    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all fields in the log line (message)
    The function uses a regex to replace occurrences of certain field values.
    Uses re.sub to perform the substitution with a single regex.

    Implements the format method to filter values in incoming log records using filter_datum.

    Implements a get_logger function that takes no arguments and returns a logging.Logger object.
    The logger is named "user_data" and only logs up to logging.INFO level. It does not propagate messages to other loggers. It has a StreamHandler with RedactingFormatter as formatter.

    Connects to a secure holberton database to read a users table. 
    Implements a get_db function that returns a connector to the database (mysql.connector.connection.MySQLConnection object).
    Uses the os module to obtain credentials from the environment
    Uses the module mysql-connector-python to connect to the MySQL database (pip3 install mysql-connector-python)

    Implements a main function that takes no arguments and returns nothing.
    The function obtains a database connection using get_db and retrieves all rows in the users table and display each row under a filtered format. 






encrypt_password.py             Contains functions that encrypt passwords.
    Implement a hash_password function that expects one string argument name password and returns a salted, hashed password, which is a byte string.
    Use the bcrypt package to perform the hashing (with hashpw).

    Implements an is_valid function that expects 2 arguments and returns a boolean.
    Arguments:
        hashed_password: bytes type
        password: string type
    Uses bcrypt to validate that the provided password matches the hashed password.

