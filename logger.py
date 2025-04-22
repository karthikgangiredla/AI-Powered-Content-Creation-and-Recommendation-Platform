import logging
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv() 

class MySQLHandler(logging.Handler):
    def __init__(self, host, user, password, database):
        logging.Handler.__init__(self)
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def emit(self, record):
        try:
            msg = self.format(record)
            module = record.module
            level = record.levelname
            timestamp = datetime.now()

            query = "INSERT INTO logs (level, message, module, created_at) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (level, msg, module, timestamp))
            self.connection.commit()
        except Exception as e:
            print(f"Failed to log to DB: {e}")

logger = logging.getLogger("ai_content_platform")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

mysql_handler = MySQLHandler(
    host="localhost",
    user=os.getenv("DB_USER"),   
    password=os.getenv("DB_PASSWORD"),
    database="ai_content_db"
)
mysql_handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
console_handler.setFormatter(formatter)
mysql_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(mysql_handler)
