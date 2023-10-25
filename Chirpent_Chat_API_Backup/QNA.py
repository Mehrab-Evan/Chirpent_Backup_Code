import leadsdb
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
from langchain import PromptTemplate
import openai
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def Only_QNA(user_question, session_id, org_url):
    knowledgebase = leadsdb.get_knowledgebase(org_url)
    # print(knowledgebase)
    is_session_id = leadsdb.if_QNA_msg_history_exists(session_id, org_url)

    user_provided_prompt = "You are a helpful assistant of One Bank. Speak professionally with the users "
    prompt_template = """


    {context} 
    Question: {question}

    """

    last_prompt = user_provided_prompt + prompt_template
    prompt = PromptTemplate(template=last_prompt, input_variables=["context", "question"])
    llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-16k")

    qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=knowledgebase.as_retriever(),
                                               combine_docs_chain_kwargs={"prompt": prompt})

    if is_session_id == None:
        chat_history = []
        chat_history_json = []
        # eita database theke asbe user_provided prompt ta
        # user_provided_prompt = "You are a helpful assistant of One Bank. Speak professionally with the users "
        # prompt_template = """
        #
        #
        # {context}
        # Question: {question}
        #
        # """
        # last_prompt = user_provided_prompt + prompt_template
        # prompt = PromptTemplate(template=last_prompt, input_variables=["context", "question"])
        # llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-16k")
        #
        # qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=knowledgebase.as_retriever(),
        #                                            combine_docs_chain_kwargs={"prompt": prompt})
        # qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.9), knowledgebase.as_retriever())
        # docs = knowledgebase.similarity_search(user_question)
        # x = chain.run(input_documents=docs, question=query)
        # docs = knowledgebase.similarity_search(user_question)

        result = qa({"question": user_question, "chat_history": chat_history})
        message = {
            "user": user_question,
            "assistant": result
        }
        chat_history_json.append(message)
        chat_history.append((user_question, result))
        leadsdb.update_QNA_msg_history(session_id, chat_history, org_url)
        leadsdb.update_user_msg_json(session_id, chat_history_json, org_url)
        return result["answer"]
    else:
        chat_history = is_session_id
        chat_history_json = leadsdb.get_user_msg_json(session_id, org_url)
        # qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.9), knowledgebase.as_retriever())
        # docs = knowledgebase.similarity_search(user_question)
        # x = chain.run(input_documents=docs, question=query)
        result = qa({"question": user_question, "chat_history": chat_history})
        chat_history.append((user_question, result['answer']))

        leadsdb.update_QNA_msg_history(session_id, chat_history, org_url)
        return result["answer"]


def QNA_with_Product_Search(user_question, session_id, org_url):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate chat model
        messages=[
            {"role": "system",
             "content": "If and only if the user is looking for any service like he wants to order or purchase something just reply 'search', else otherwise if he wants to know anything or ask anything simple only response 'normal' don't reply anything else at all."},
            {"role": "user", "content": user_question}
        ],
        api_key=api_key,
    )
    model_response = response.choices[0].message["content"]

    if model_response == "normal":
        answer = Only_QNA(user_question, session_id, org_url)
        return answer

    if model_response == "search":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate chat model
            messages=[
                {"role": "system",
                 "content": "Just type the name of the products user search for Don't reply that yes what are you looking for etc etc. Just reply the product again"},
                {"role": "user", "content": user_question}
            ],
            api_key=api_key,
        )
        product_name = response.choices[0].message["content"]

    #
    #     try:
    #         is_id = leadsdb.if_session_id_exists(session_id, org_url)
    #         if is_id == "OK":
    #             leadsdb.update_user_request(session_id, product_name, org_url)
    #         else:
    #             leadsdb.insert_user_request(session_id, product_name, org_url)
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #
    #     now_response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",  # Use the appropriate chat model
    #         messages=[
    #             {"role": "system",
    #              "content": "Ask the user only for his/her name only"},
    #             {"role": "user", "content": user_question}
    #         ],
    #         api_key=api_key,
    #     )
    #     answer = now_response.choices[0].message["content"]
    #     return answer
    #
    # if model_response == "name":
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",  # Use the appropriate chat model
    #         messages=[
    #             {"role": "system",
    #              "content": "Just type the name of the user nothing more. nothing more at all not even hi hello etc "},
    #             {"role": "user", "content": user_question}
    #         ],
    #         api_key=api_key,
    #     )
    #     user_name = response.choices[0].message["content"]
    #
    #     try:
    #         leadsdb.update_user_name(session_id, user_name, org_url)
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #
    #     now_response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",  # Use the appropriate chat model
    #         messages=[
    #             {"role": "system",
    #              "content": "Thank the user for his name then Ask the user only for his/her email id"},
    #             {"role": "user", "content": user_question}
    #         ],
    #         api_key=api_key,
    #     )
    #     answer = now_response.choices[0].message["content"]
    #     return answer
    #
    # if model_response == "email":
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",  # Use the appropriate chat model
    #         messages=[
    #             {"role": "system",
    #              "content": "Just type the email of the user provided nothing more. nothing more at all. Just type the email"},
    #             {"role": "user", "content": user_question}
    #         ],
    #         api_key=api_key,
    #     )
    #     user_email = response.choices[0].message["content"]
    #
    #     try:
    #         leadsdb.update_user_email(session_id, user_email, org_url)
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #
    #     now_response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",  # Use the appropriate chat model
    #         messages=[
    #             {"role": "system",
    #              "content": "Reply a Thanks and say we will reach you."},
    #             {"role": "user", "content": user_question}
    #         ],
    #         api_key=api_key,
    #     )
    #     answer = now_response.choices[0].message["content"]
    #     return answer



def Flow_Management(user_question, session_id, org_url):
    print('x')