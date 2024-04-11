#!/usr/bin/env python3
"""
Task 0 to 4.
Handeling persenal Data.
"""
import logging
import mysql.connector
from os import environ
import re
from typing import List


# Create a tuple PII_FIELDS constant at the root of the module
# containing the fields from user_data.csv
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Task 0: Regex-ing. returns the log message obfuscated.

    Args:
        fields (List[str]):  of strings representing all fields to obfuscate.
        redaction (str): representing by what the field will be obfuscated.
        message (str): a string representing the log line.
        separator (str): a string representing by which character is separating
        all fields in the log line (message).

    Returns:
        str: the log message obfuscated.
    """
    for field in fields:
        pattern_ = '{}=.*?{}'.format(field, separator)
        replace_ = '{}={}{}'.format(field, redaction, separator)
        message = re.sub(pattern_, replace_, message)
    return message


def get_logger() -> logging.Logger:
    """
    takes no arguments and returns a logging.Logger object.
    choose the right list of fields that can are considered
    as “important” PIIs or information that you must hide
    in your logs. Use it to parameterize the formatter.
    Returns:
        logging.Logger: _description_
    """
    info = logging.getLogger("user_data")
    stream = logging.StreamHandler()
    info.setLevel(logging.INFO)
    info.propagate = False
    stream.setFormatter(
        RedactingFormatter(list(PII_FIELDS))
        )
    info.addHandler(stream)
    return info


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Task 3: Connect to secure database.

    Returns:
        mysql.connector.connection.MySQLConnection: connector to the database.
    """
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    cnx = mysql.connector.connection.MySQLConnection(
        host=host,
        port=3306,
        user=username,
        password=password,
        database=db_name,
    )
    return cnx


def main():
    """
    Task 4: Read and filter data.
    The function will obtain a database connection using
    get_db and retrieve all rows in the users table
    and display each row under a filtered format.
    Only your main function should run when the module is executed.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field = [fields[0] for fields in cursor.description]
    info = get_logger()
    for line in cursor:
        for t in zip(line, field):
            msg = ''.join('{}={str()};'.format(t[0], t[1]))
        info.info(msg)
    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """
    Task 1: Log formatter.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records using filter_datum.
        Values for fields in fields should be filtered.
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
