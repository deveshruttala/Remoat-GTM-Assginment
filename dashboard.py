import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST')
)
cur = conn.cursor()
cur.execute("SELECT * FROM stories ORDER BY id DESC LIMIT 10;")
stories = cur.fetchall()

st.title("AI Newsletter Dashboard")
for s in stories:
    st.write(f"{s[0]}: {s[1]}")
