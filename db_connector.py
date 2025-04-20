import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv() 

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),   
        password=os.getenv("DB_PASSWORD"),
        database="ai_content_db"
    )
    return conn
