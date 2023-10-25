# import boto3
# import PyPDF2
# import io
# from dotenv import load_dotenv
# import os
# import pickle
# from langchain.chat_models import ChatOpenAI
# import re
#
# from langchain.schema import (
#     AIMessage,
#     HumanMessage,
#     SystemMessage
# )
# import leadsdb
#
# def read_pdf_from_s3(bucket_name, file_name):
#     try:
#         # Initialize an S3 client
#         s3 = boto3.client(
#             's3',
#             endpoint_url='https://pyspace1.blr1.digitaloceanspaces.com/',
#             aws_access_key_id='DO00WDADW6B9LENM4X4F',
#             aws_secret_access_key='X7nvNuCq7GM58SaOC9DzRAVYLzWvckoFQvBfeDjbcgQ',
#             region_name='blr1'
#         )
#
#         # Check if the file exists
#         s3.head_object(Bucket=bucket_name, Key=f'demo/{file_name}')
#
#         # Read file
#         obj = s3.get_object(Bucket=bucket_name, Key=f'demo/{file_name}')
#         file_data = obj['Body'].read()
#
#         # Wrap the bytes data in a BytesIO object and seek to the beginning
#         bytes_io = io.BytesIO(file_data)
#         bytes_io.seek(0)
#
#         # Use PyPDF2 to read the PDF content
#         pdf_reader = PyPDF2.PdfReader(bytes_io)
#         num_pages = len(pdf_reader.pages)
#         text = ""
#
#         for page_num in range(num_pages):
#             page = pdf_reader.pages[page_num]
#             text += page.extract_text()
#
#         return {"file_data": text}
#
#     except Exception as e:
#         print(e)
#         return {"error": "Something went wrong"}
#
# file_name = 'CV_w_ml.pdf'
# bucket_name = 'pyspace1'
#
# x = read_pdf_from_s3(bucket_name, file_name)
#
# print(x)
#
#
# def chirpent_no_search(user_message, session_id, org_url):
#     load_dotenv()
#     pdf_path = "Solvrz_webchat.pdf"
#     # pdf_path2 = "Classified.pdf"
#     text = user_message
#     numbers = re.findall(r'\d{9,}', text)
#
#     if numbers:
#         leadsdb.update_phone_no(session_id, numbers, org_url)
#
#     emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)
#
#     if emails:
#         leadsdb.update_email(session_id, emails, org_url)
#
#     user_data = leadsdb.get_msg_history(session_id, org_url)
#
#     chat = ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo-16k")
#
#
#     if user_data == None:
#         pdf_text = read_pdf_from_s3(bucket_name, file_name)
#         sys_msg = "Behave like that : " + ".And Follow these following texts as an external knowledge source " + pdf_text
#         msg = [SystemMessage(content=sys_msg), ]
#         msg.append(HumanMessage(content=user_message))
#         assistant_response = chat(msg)
#         msg.append(AIMessage(content=assistant_response.content))
#         pickled_str = pickle.dumps(msg)
#         leadsdb.insert_user_message(session_id, pickled_str)
#         return assistant_response.content
#     else:
#         if user_message == "cls":
#             leadsdb.delete_user_data(session_id, org_url)
#             return "Your Message History is cleared 😊"
#         else :
#             prev_msg = user_data["msg_history"]
#             msg = pickle.loads(prev_msg)
#             msg.append(HumanMessage(content=user_message))
#             assistant_response = chat(msg)
#             msg.append(AIMessage(content=assistant_response.content))
#             human_messages_content = [message.content for message in msg if isinstance(message, HumanMessage)]
#
#             leadsdb.update_user_msg(session_id, human_messages_content)
#
#             pickled_str = pickle.dumps(msg)
#             leadsdb.update_msg_history(session_id, pickled_str, org_url)
#             return assistant_response.content
knowledgebase = leadsdb.get_knowledgebase(org_url)