# import necessary libaries
import os
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine.condense_plus_context import CondensePlusContextChatEngine
from llama_index.llms.groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variable keys
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_CLUSTER_URL = os.getenv('QDRANT_CLUSTER_URL')
QDRANT_COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME')

def get_chat_engine():
     """
     Creates and configures a Chat Engine for handling context-based queries.
    
     Returns:
     CondensePlusContextChatEngine: Configured chat engine for handling queries with context.
     """

     # creates a persistant index to disk
     qdrant_client = QdrantClient(
          url=QDRANT_CLUSTER_URL, 
          api_key=QDRANT_API_KEY
     )

     # Define a vector store with the given collection name and client
     vector_store = QdrantVectorStore(
          collection_name=QDRANT_COLLECTION_NAME, client=qdrant_client, 
          enable_hybrid=True,batch_size=20
     )

     # Create an index from the vector store
     index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

     # Initialize chat memory with a token limit
     memory = ChatMemoryBuffer.from_defaults(token_limit=10000)

     # Initialize the language model
     llm = Groq(model="mixtral-8x7b-32768",api_key=GROQ_API_KEY)

     # Create a chat engine with specific settings
     chat_engine = index.as_chat_engine(
          chat_mode="condense_plus_context",
          memory=memory,
          llm=llm,
          context_prompt=(
               "You are a chatbot. Your job is to find answer for users in the given context as fast as you can, answer should be specific context to the question"
               "If the question is out of context, then give the response, 'I'm sorry, I cannot provide an answer to that question as it is not related to the context information provided.'"
               "Here are the relevant documents for the context."
               "Do not reveal the document source or any data from where you are fetching the information"
               "{context_str}"
               "\nGiven the new context, refine the original answer to better understand."
               "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."),
               verbose=False,
               similarity_top_k=2,
               sparse_top_k=12,
               vector_store_query_mode="hybrid"
          )

     return chat_engine

def question_answer(query:str, chat_engine:CondensePlusContextChatEngine):
     """
     Queries the chat engine with a specific question and returns the response.

     Args:
     - query (str): The question to ask the chat engine.
     - chat_engine (CondensePlusContextChatEngine): The configured chat engine to interact with.

     Returns:
     - str: The chat engine's response to the given query.
     """
     return str(chat_engine.chat(query))