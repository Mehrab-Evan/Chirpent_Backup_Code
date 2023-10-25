from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
import leadsdb

load_dotenv()
def vector_embeddings(text, org_url):
    updated_text = text + "You will act as an AI assistant of the following organization it is your organization. When user will ask you will response from these texts providing below. If user ask any out of contexts question you shall tell him that you can only talk about these following text mentioning. Ask user questions all the time if he needs anything else to know. and response if user thanks you or show gratitude Take these as prompts : "

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(updated_text)
    embeddings = OpenAIEmbeddings()

    knowledgebase = FAISS.from_texts(texts=chunks, embedding=embeddings)

    flag = leadsdb.if_knowledge_exists(org_url)

    print(flag)

    if flag == "exists":
        leadsdb.update_knowledge(org_url, knowledgebase)
        return "OK"
    else:
        leadsdb.insert_knowledge(org_url, knowledgebase)
        return "OK"
