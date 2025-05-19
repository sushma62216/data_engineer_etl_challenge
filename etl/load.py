import psycopg2
import pyodbc
import logging
from dotenv import load_dotenv
import os

load_dotenv()

def get_pg_conn():
    return psycopg2.connect(
        host='localhost',
        port=5432,
        database='staging_db',
        user='postgres',
        password='postgres'
    )

def load_users(users):
    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS staging_users;""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS staging_users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT,
            email TEXT,
            phone TEXT,
            website TEXT,
            street TEXT,
            suite TEXT,
            city TEXT,
            zipcode TEXT,
            geo_lat TEXT,
            geo_lng TEXT,
            company_name TEXT,
            company_catch_phrase TEXT,
            company_bs TEXT
        );
    """)
    cur.execute("TRUNCATE TABLE staging_users")
    for user in users:
        cur.execute("""
            INSERT INTO staging_users (
                id, name, username, email, phone, website,
                street, suite, city, zipcode, geo_lat, geo_lng,
                company_name, company_catch_phrase, company_bs
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            user['id'],
            user['name'],
            user['username'],
            user['email'],
            user['phone'],
            user['website'],
            user['address']['street'],
            user['address']['suite'],
            user['address']['city'],
            user['address']['zipcode'],
            user['address']['geo']['lat'],
            user['address']['geo']['lng'],
            user['company']['name'],
            user['company']['catchPhrase'],
            user['company']['bs']
        ))

    conn.commit()
    cur.close()
    conn.close()



def load_posts(posts):
    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS staging_posts;""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS staging_posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        );
    """)
    cur.execute("TRUNCATE TABLE staging_posts")

    for post in posts:
        cur.execute("""
            INSERT INTO staging_posts (id, user_id, title, body)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            post['id'],
            post['userId'],
            post['title'],
            post['body']
        ))

    conn.commit()
    cur.close()
    conn.close()


def get_sqlserver_conn():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost,1433;'
        'DATABASE=master;'
        'UID=sa;'
        'PWD=Sqlserver@2025'
    )

def load_to_sqlserver(records):
    conn = get_sqlserver_conn()
    cur = conn.cursor()

    # Create the target table if it doesn't exist
    cur.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects WHERE name='FactUserPosts' AND xtype='U'
        )
        CREATE TABLE FactUserPosts (
            PostID INT PRIMARY KEY,
            PostTitle NVARCHAR(MAX),
            PostBody NVARCHAR(MAX),
            UserName NVARCHAR(100),
            UserEmail NVARCHAR(100)
        )
    """)

    for record in records:
        cur.execute("""
            MERGE FactUserPosts AS target
            USING (SELECT ? AS PostID) AS source
            ON target.PostID = source.PostID
            WHEN NOT MATCHED THEN
                INSERT (PostID, PostTitle, PostBody, UserName, UserEmail)
                VALUES (?, ?, ?, ?, ?);
        """, (
            record['post_id'],
            record['post_id'], record['post_title'],
            record['post_body'], record['user_name'],
            record['user_email']
        ))

    conn.commit()
    conn.close()