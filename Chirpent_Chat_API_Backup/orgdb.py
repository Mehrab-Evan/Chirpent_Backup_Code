import psycopg2
from psycopg2 import sql

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    database="chirpent_dashboard",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

def get_msg_limit(org_url):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT msg_limit, msg_count, lead_categories, subscription_date, expiration_date
            FROM org
            WHERE org_url = %s
        """, (org_url,))
        org_data = cursor.fetchone()
        if org_data:
            msg_limit, msg_count, lead_categories, subscription_date, expiration_date = org_data
            return {
                "org_url": org_url,
                "msg_limit": msg_limit,
                "msg_count": msg_count,
                "lead_categories": lead_categories,
                "subscription_date": subscription_date,
                "expiration_date": expiration_date,
            }
        else:
            return None

def update_msg_count(org_url, new_msg_count):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE org
            SET msg_count = %s
            WHERE org_url = %s
        """, (new_msg_count, org_url))
        conn.commit()
