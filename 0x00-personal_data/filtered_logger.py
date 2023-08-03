#!/usr/bin/env python3
"""A module containing functions that filter log messages"""

import re
from typing import List
import logging
import mysql.connector 
import os
import sys
import csv
import datetime
import uuid
import hashlib
from typing import Union
from os import getenv

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function that returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message

"""A class that inherits from logging.Formatter and filters values in incoming log records using filter_datum"""
class RedactingFormatter(logging.Formatter):
    """A custom log formatter that redacts sensitive information from log messages"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize a RedactingFormatter object"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Override the format method to apply redaction to the log message"""
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)

PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']

def get_logger() -> logging.Logger:
    """A function that returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """A function that returns a connector to a database"""
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(user=username,
                                   password=password,
                                   host=host,
                                   database=db_name)

def main():
    """A function that obtains a database connection using get_db and
    retrieves all rows in the users table and display each row under a
    filtered format
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]
    logger = get_logger()
    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
