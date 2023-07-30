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
    LLMPredictor
)
from llama_index.indices.query.query_transform.base import StepDecomposeQueryTransform
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.llms import OpenAI
from llama_index.query_engine import FLAREInstructQueryEngine
from llama_index import VectorStoreIndex
from llama_index.objects import ObjectIndex, SimpleToolNodeMapping
from llama_index.query_engine import ToolRetrieverRouterQueryEngine
from llama_index.response_synthesizers import get_response_synthesizer



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
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4", temperature=0, chunk_size=512), embed_model=query_embed_model)

        storage_context = StorageContext.from_defaults(persist_dir="C:\\Users\\derek\\cs_projects\\bioML\\bioIDE\\interfacingLLMs\\stored_embeddings\\biorxiv\\")
        biorxiv_docs_index = load_index_from_storage(storage_context, service_context=service_context)   

        self.biorxiv_docs_engine = biorxiv_docs_index.as_query_engine(similarity_top_k=5, service_context=service_context)

        self.flare_query_engine = FLAREInstructQueryEngine(
            query_engine=self.biorxiv_docs_engine,
            service_context=service_context,
            verbose=True
        )

        query_engine_tools = [
            QueryEngineTool(
                query_engine=self.biorxiv_docs_engine,
                metadata=ToolMetadata(name="biorxiv_docs_engine", description="Provides information about the recent BioRxiv papers") 
            ), 
            QueryEngineTool(
                query_engine=self.flare_query_engine, 
                metadata=ToolMetadata(name="flare_engine", description="Provides information using FLARE instructions")
            ),
        ]

        self.sub_query_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools, 
                service_context=service_context, response_synthesizer=get_response_synthesizer(streaming=True), verbose=True, use_async=False)

        tool_mapping = SimpleToolNodeMapping.from_objects(query_engine_tools)
        object_index = ObjectIndex.from_objects(query_engine_tools, tool_mapping, GPTVectorStoreIndex)

        self.rag_router_query_engine = ToolRetrieverRouterQueryEngine(object_index.as_retriever())
    def query(self, engine: str, query: str):
        if engine == "biorxiv":
            response = self.biorxiv_docs_engine.query(query)
            return response
        elif engine == "flare":
            return self.flare_query_engine.query(query)
        elif engine == "rag-router":
            return self.rag_router_query_engine.query(query)
        elif engine == "subquestion":
            response =  self.sub_query_engine.query(query)
            source_nodes = response.source_nodes
            source_str = ""
            for i in range(len(source_nodes)):
                node = source_nodes[i]
                source_str += '\n'
                source_str += node.node.text
                source_str += "\n\n"
            return f"{str(response)} \n\n\n {source_str}\n"

qa_deployment = QADeployment()

st.title('QA System')
engine = st.selectbox(
    'Select Engine',
    ('biorxiv', 'flare', 'Retrieval-Augmented Router Query Engine', 'subquestion')
)

query = st.text_input('Enter your query', '')

if st.button('Search'):
    response = qa_deployment.query(engine, query)
    st.write('Response:', response)