import psycopg2
from psycopg2 import sql
import pickle

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    database="chirpent_dashboard",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# Knowledgebase processing er kaaaj
def insert_knowledge(org_url, knowledgebase):
    try:
        with conn.cursor() as cursor:
            # Serialize the embedded_txt to bytes using pickle
            knowledgebase_bytes = pickle.dumps(knowledgebase)
            cursor.execute("""
                INSERT INTO knowledgesource (org_url, knowledge_base)
                VALUES (%s, %s)
            """, (org_url, psycopg2.Binary(knowledgebase_bytes)))
            conn.commit()
            return "OK"
    except psycopg2.Error as e:
        # Handle any database errors here
        print(f"Error inserting user message: {e}")
        return "Error"

def update_knowledge(org_url, knowledgebase):
    with conn.cursor() as cursor:
        knowledgebase_bytes = pickle.dumps(knowledgebase)
        cursor.execute("""
            UPDATE knowledgesource
            SET knowledge_base = %s
            WHERE org_url = %s
        """, (psycopg2.Binary(knowledgebase_bytes), org_url))
        conn.commit()

def if_knowledge_exists(org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT knowledge_base
            FROM knowledgesource
            WHERE org_url = %s
        """, (org_url,))
        user_data = cursor.fetchone()
        if user_data:
            return "exists"
        else:
            return None

def get_knowledgebase(org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT knowledge_base
            FROM knowledgesource
            WHERE org_url = %s
        """, (org_url,))
        user_data = cursor.fetchone()
        if user_data:
            knowledge_bytes = user_data[0]
            knowledge = pickle.loads(knowledge_bytes)
            return knowledge
            # return {
            #     "knowledge_base": knowledge
            # }
        else:
            return None
# Knowledge base er kaaj shesh apatoto


# QNA_MSG_HISTORY
def if_QNA_msg_history_exists(session_id, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT msg_history1
            FROM chat
            WHERE session_id = %s AND org_url = %s
        """, (session_id, org_url))
        user_data = cursor.fetchone()
        if user_data:
            msg_history1_byte = user_data
            msg_history1 = pickle.loads(msg_history1_byte)
            return msg_history1
            # return {
            #     "msg_history1": msg_history1
            # }
        else:
            return None

def update_QNA_msg_history(session_id, msg_history1, org_url):
    with conn.cursor() as cursor:
        msg_history1_byte = pickle.dumps(msg_history1)
        cursor.execute("""
            UPDATE chat
            SET msg_history1 = %s
            WHERE session_id = %s AND org_url = %s
        """, (psycopg2.Binary(msg_history1_byte), session_id, org_url))
        conn.commit()
# QNA Msg_history1


# GET ORG_URL
def fetch_knowledge_org_url(org_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT org_url, text_bytes
            FROM org
            WHERE org_id = %s
        """, (org_id,))
        user_data = cursor.fetchone()
        if user_data:
            org_url, text_bytes = user_data
            return org_url, text_bytes
        else:
            return None

# If Session_ID Exists
def if_session_id_exists(session_id, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT session_id
            FROM chat
            WHERE session_id = %s AND org_url = %s
        """, (session_id, org_url))
        user_data = cursor.fetchone()
        if user_data:
            return "OK"
        else:
            return None

def update_user_request(session_id, product_name, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chat
            SET user_request = %s
            WHERE session_id = %s AND org_url = %s
        """, (product_name, session_id, org_url))
        conn.commit()

def update_user_name(session_id, user_name, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chat
            SET user_name = %s
            WHERE session_id = %s AND org_url = %s
        """, (user_name, session_id, org_url))
        conn.commit()

def update_user_email(session_id, user_email, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chat
            SET user_email = %s
            WHERE session_id = %s AND org_url = %s
        """, (user_email, session_id, org_url))
        conn.commit()

def insert_user_request(session_id, product_name, org_url):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO chat (session_id, org_url, user_request)
                VALUES (%s, %s, %s)
            """, (session_id, org_url, product_name))
            conn.commit()
            return "OK"
    except psycopg2.Error as e:
        # Handle any database errors here
        print(f"Error inserting user message: {e}")
        return "Error"




def insert_user_message(session_id, msg_history, org_url):
    try:
        with conn.cursor() as cursor:
            # Email and password combination does not exist, insert the new user
            cursor.execute("""
                INSERT INTO chirpent_user_messages_leads (session_id, msg_history, org_url)
                VALUES (%s, %s, %s)
            """, (session_id, msg_history, org_url))
            conn.commit()
            return "OK"
    except psycopg2.Error as e:
        # Handle any database errors here
        print(f"Error inserting user message: {e}")
        return "Error"


# Function to update the msg_history
def update_msg_history(session_id, new_msg_history, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET msg_history = %s
            WHERE session_id = %s AND org_url = %s
        """, (new_msg_history, session_id, org_url))
        conn.commit()


def update_email(session_id, email, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET user_email = %s
            WHERE session_id = %s AND org_url = %s
        """, (email, session_id, org_url))
        conn.commit()

def update_phone_no(session_id, phone, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET user_phone = %s
            WHERE session_id = %s AND org_url = %s
        """, (phone, session_id, org_url))
        conn.commit()

def update_user_msg(session_id, user_msg, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE chirpent_user_messages_leads
            SET user_msg = %s
            WHERE session_id = %s AND org_url = %s
        """, (user_msg, session_id, org_url))
        conn.commit()

import json
def update_user_msg_json(session_id, user_msg, org_url):
    with conn.cursor() as cursor:
        user_msg_json = json.dumps(user_msg)
        cursor.execute("""
            UPDATE chat
            SET user_msg_json = %s
            WHERE session_id = %s AND org_url = %s 
        """, (user_msg_json, session_id, org_url))
        conn.commit()

def get_user_msg_json(session_id, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT user_msg_json
            FROM lead
            WHERE session_id = %s AND org_url = %s
        """, (session_id, org_url))
        user_data = cursor.fetchone()
        if user_data:
            user_msg = user_data[0]
            return user_msg
        else:
            return None



def get_msg_history(session_id, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT session_id, msg_history
            FROM chirpent_user_messages_leads
            WHERE session_id = %s AND org_url = %s
        """, (session_id, org_url))
        user_data = cursor.fetchone()
        if user_data:
            session_id, msg_history = user_data
            return {
                "user_id": session_id,
                "msg_history": msg_history
            }
        else:
            return None

# Function to delete a row for a specific user_id
def delete_user_data(session_id, org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM chirpent_user_messages_leads
            WHERE session_id = %s AND org_url = %s
        """, (session_id, org_url))
        conn.commit()

# # Example usage
# if __name__ == "__main__":
#     Create_table_User_Messages_Leads()


# Lagtese na cause Arthi create kore felse eida
# def Create_table_User_Messages_Leads():
#     with conn.cursor() as cursor:
#         cursor.execute("""
#             CREATE TABLE chirpent_user_messages_leads (
#                 session_id TEXT PRIMARY KEY,
#                 org_url TEXT,
#                 msg_history BYTEA,
#                 embedded_txt BYTEA,
#                 embedded_msg_history BYTEA,
#                 user_msg TEXT,
#                 user_name TEXT,
#                 user_need TEXT,
#                 user_email TEXT,
#                 user_phone TEXT,
#                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         conn.commit()