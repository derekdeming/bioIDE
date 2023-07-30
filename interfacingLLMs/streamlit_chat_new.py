import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from llama_index import GPTVectorStoreIndex
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from biorxiv_manager import BioRxivManager  
from llama_index import (
    load_index_from_storage, 
    ServiceContext, 
    StorageContext, 
    LangchainEmbedding,
)
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

st.set_page_config(page_title="Chat with Documents Using LlamaIndex and LangChain")
st.title("Chat with Documents with LangChain")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

@st.cache_resource
class QADeployment:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = openai_api_key
        query_embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))
        service_context = ServiceContext.from_defaults(embed_model=query_embed_model)

        storage_context = StorageContext.from_defaults(persist_dir="C:\\Users\\derek\\cs_projects\\bioML\\bioIDE\\interfacingLLMs\\stored_embeddings\\biorxiv\\")
        biorxiv_docs_index = load_index_from_storage(storage_context, service_context=service_context)   

        self.biorxiv_docs_engine = biorxiv_docs_index.as_query_engine(similarity_top_k=5, service_context=service_context)

        query_engine_tools = [
            QueryEngineTool(
                query_engine=self.biorxiv_docs_engine,
                metadata=ToolMetadata(name="biorxiv_docs_engine", description="Provides information about the recent BioRxiv papers")
            )
        ]

        self.sub_query_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools, service_context=service_context, use_async=False)

    def query(self, engine: str, query: str):
        if engine == "biorxiv":
            return self.biorxiv_docs_engine.query(query)
        elif engine == "subquestion":
            response =  self.sub_query_engine.query(query)
            source_nodes = response.source_nodes
            source_str = ""
            for i in range(len(source_nodes)):
                node = source_nodes[i]
                source_str += f"Sub-question {i+1}:\n"
                source_str += node.node.text
                source_str += "\n\n"
            return f"Response: {str(response)} \n\n\n {source_str}\n"

qa_deployment = QADeployment()

st.title('QA System')
engine = st.selectbox(
    'Select Engine',
    ('biorxiv', 'subquestion')
)

query = st.text_input('Enter your query', '')

if st.button('Search'):
    response = qa_deployment.query(engine, query)
    st.write('Response:', response)