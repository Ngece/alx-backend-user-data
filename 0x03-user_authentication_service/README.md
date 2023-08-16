user.py             an SQLAlchemy model named User for a database table named users.
    Attributes:
        id, the integer primary key
        email, a non-nullable string
        hashed_password, a non-nullable string
        session_id, a nullable string
        reset_token, a nullable string




db.py               
    Implements the add_user method, which has two required string arguments: email and hashed_password, and returns a User object. The method saves the user to the database.

    Implements the DB.find_user_by method. This method takes in arbitrary keyword arguments and returns the first row found in the users table as filtered by the method’s input arguments. 
    SQLAlchemy’s NoResultFound and InvalidRequestError are raised when no results are found, or when wrong query arguments are passed, respectively.

    Implements the DB.update_user method that takes as argument a required user_id integer and arbitrary keyword arguments, and returns None.
    The method uses find_user_by to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.




auth.py             
    Contains a _hash_password method that takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password, hashed with bcrypt.hashpw.

    Implement the Auth.register_user in the Auth class. The method takes mandatory email and password string arguments and returns a User object.
    f a user already exist with the passed email, raise a ValueError with the message User <user's email> already exists.
    If not, hash the password with _hash_password, save the user to the database using self._db and return the User object.

    Implement the Auth.valid_login method. It expects email and password required arguments and returns a boolean.
    Locates the user by email. If it exists, checks the password with bcrypt.checkpw. If it matches returns True. In any other case, returns False.

    Implements a _generate_uuid function in the auth module. The function returns a string representation of a new UUID. Uses the uuid module.

    Implements the Auth.create_session method. It takes an email string argument and returns the session ID as a string.
    Finds the user corresponding to the email, generate a new UUID and stores it in the database as the user’s session_id, then returns the session ID.

    Implements the Auth.get_user_from_session_id method. It takes a single session_id string argument and returns the corresponding User or None.
    If the session ID is None or no user is found, return None. Otherwise return the corresponding user.

    Implements Auth.destroy_session. The method takes a single user_id integer argument and returns None.
    Updates the corresponding user’s session ID to None.

    Implements the Auth.get_reset_password_token method. It takes an email string argument and returns a string.
    Find the user corresponding to the email. If the user does not exist, raise a ValueError exception. If it exists, generate a UUID and update the user’s reset_token database field. Return the token.

    Implements the Auth.update_password method. It takes reset_token string argument and a password string argument and returns None.
    Uses the reset_token to find the corresponding user. If it does not exist, it raises a ValueError exception.
    Otherwise, hash the password and update the user’s hashed_password field with the new hashed password and the reset_token field to None.





app.py              
    a Flask app that has a single GET route ("/") and use flask.jsonify to return a JSON payload of the form:
    {"message": "Bienvenue"}

    Implement the end-point to register a user. Defines a users function that implements the POST /users route.
    Expects two form data fields: "email" and "password"
    If the user does not exist, the end-point should register it and respond with the following JSON payload:
        {"email": "<registered email>", "message": "user created"}
    If the user is already registered, catches the exception and return a JSON payload of the form
        {"message": "email already registered"} and return a 400 status code.

    Implements a login function to respond to the POST /sessions route.
    Contain form data with "email" and a "password" fields.
    If the login information is incorrect, uses flask.abort to respond with a 401 HTTP status. Otherwise, creates a new session for the user, stores it the session ID as a cookie with key "session_id" on the response and return a JSON payload of the form:
        {"email": "<user email>", "message": "logged in"}

    Implements a logout function to respond to the DELETE /sessions route.
    The request is expected to contain the session ID as a cookie with key "session_id".
    Finds the user with the requested session ID. If the user exists destroy the session and redirect the user to GET /. If the user does not exist, respond with a 403 HTTP status.

    Implements a profile function to respond to the GET /profile route.
    The request is expected to contain a session_id cookie. If the user exists, responds with a 200 HTTP status and the following JSON payload:
        {"email": "<user email>"}
    If the session ID is invalid or the user does not exist, respond with a 403 HTTP status.

    Implements a get_reset_password_token function to respond to the POST /reset_password route.
    The request is expected to contain form data with the "email" field.
    If the email is not registered, responds with a 403 status code. Otherwise, it generates a token and responds with a 200 HTTP status and the following JSON payload:
        {"email": "<user email>", "reset_token": "<reset token>"}

    Implements the update_password function in the app module to respond to the PUT /reset_password route.
    The request is expected to contain form data with fields "email", "reset_token" and "new_password".
    If the token is invalid, it catches the exception and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 HTTP code and the following JSON payload:
        {"email": "<user email>", "message": "Password updated"}
    




main.py
    Contains one function for each of the following tasks. Uses the requests module to query the web server for corresponding end-points. Uses assert to validate the response’s expected status code and payload (if any) for each task.

    register_user(email: str, password: str) -> None
    log_in_wrong_password(email: str, password: str) -> None
    log_in(email: str, password: str) -> str
    profile_unlogged() -> None
    profile_logged(session_id: str) -> None
    log_out(session_id: str) -> None
    reset_password_token(email: str) -> str
    update_password(email: str, reset_token: str, new_password: str) -> None
