from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import organization_handle
import vector_embeddings
from dotenv import load_dotenv
import leadsdb
import pickle
load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "<h1>Chirpent Chat is Doing great</h1>"

# REDIS CACHE TESTING:
@app.route("/chirpent_web_chat_redis", methods=["POST"])
def redis_test():
    org_url = request.headers.get('ORG-URL', '')
    org_api = request.headers.get('ORG-API', '')
    new_org_api = "a"+org_api

    user_question = request.json["user_question"]

    if_activate = organization_handle.is_active(org_url, new_org_api)
    if if_activate == "expired":
        return jsonify({"answer": "Your Organization's Message limit is over"})

    return jsonify({"answer": "Your Organization's Message is good"})


@app.route("/chirpent_web_chat", methods=["POST"])
def get_answer_for_chirpent():
    session_id = request.headers.get('SESSION-ID', '')
    org_url = request.headers.get('ORG-URL', '')
    org_api = request.headers.get('ORG-API', '')
    new_org_api = "a"+org_api

    user_question = request.json["user_question"]

    if_activate = organization_handle.is_active(org_url, new_org_api)

    if if_activate == "expired":
        return jsonify({"answer": "Your Organization's Message limit is over"})

    response = organization_handle.check_categories(session_id, org_url, new_org_api, user_question)
    return jsonify({"answer": response})


# TEXT PROCESSING FINISHED.
@app.route("/text_process", methods=["POST"])
def embeddings():
    org_id = request.headers.get('ORG-ID', '')
    result = leadsdb.fetch_knowledge_org_url(org_id)

    if result:
        org_url, text_bytes = result
        real_text = pickle.loads(text_bytes)
        # print(real_text)
        respond = vector_embeddings.vector_embeddings(real_text, org_url)

        if respond == "OK":
            return "OK"


if __name__ == '__main__':
    app.run(debug=True)


 