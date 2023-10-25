import orgdb
import chirpent_no_search
import QNA
import redis
from datetime import datetime


# Connect to a Redis server
redis_host = 'localhost'  # Change this to your Redis server's host
redis_port = 6379        # Change this to your Redis server's port
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def is_active(org_url, new_org_api):
    result = orgdb.get_msg_limit(org_url)
    org_msg_limit = result["msg_limit"]
    org_msg_count = result["msg_count"]

    # r.set(f'{new_org_api}', org_msg_count)
    # r.incr(f'{new_org_api}')
    r.set(f'{new_org_api}', org_msg_count)
    r.incr(f'{new_org_api}')
    counter_value = r.get(f'{new_org_api}')

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

    expired_db_date = result["expiration_date"]

    # c = 2023-11-02 19:03:05.052816

    print(expired_db_date)
    print(current_datetime)
    print(type(expired_db_date))
    print(type(current_datetime))
    print(formatted_datetime)
    print(type(formatted_datetime))
    # print(f'{new_org_api}')
    # print(counter_value)
    # print(type(counter_value))
    # print(type(org_msg_limit))
    # print(type(int(counter_value)))
    # new_org_msg_count = org_msg_count + 1

    print(formatted_datetime < str(expired_db_date))

    if (int(counter_value) > (org_msg_limit)) or (formatted_datetime > str(expired_db_date)):
        orgdb.update_msg_count(org_url, counter_value)
        return "expired"
    else:
        orgdb.update_msg_count(org_url, int(counter_value))
        return
        # return "GOOD"
        # return "Your message limit of {f} messages is over", org_msg_limit


def check_categories(session_id, org_url, user_question):
    result = orgdb.get_msg_limit(org_url)
    org_leads_categories = result["leads_categories"]

    if(org_leads_categories == 0 or org_leads_categories == 1) :
        response = QNA.Only_QNA(user_question, session_id, org_url)
        return response
    if(org_leads_categories == 2) :
        response = QNA.QNA_with_Product_Search(user_question, session_id, org_url)
        return response
    if(org_leads_categories == 3) :
        response = QNA.Flow_Management(user_question, session_id, org_url)

    chirpent_no_search.chirpent_no_search(user_question, session_id, org_url)