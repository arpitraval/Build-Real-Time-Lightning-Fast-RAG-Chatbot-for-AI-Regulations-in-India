import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.core import SimpleDirectoryReader

load_dotenv()

# Load .env variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_CLUSTER_URL = os.getenv("QDRANT_CLUSTER_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

# Fetch required environment variables
def load_documents(input_directory):
   """
   Load all Markdown (.md) files from the specified directory and return the 
   extracted document data. If successful, the temporary .md files are deleted.
    
   Parameters:
   - input_directory (str): The path to the directory containing the .md files.

   Returns:
   - list: A list of document objects containing the loaded data.
   """

   # Check if there are any .md files in the input directory
   md_files_exist = any(file_name.endswith(".md") for file_name in os.listdir(input_directory))

   if md_files_exist:
      required_exts = [".md"]

      documents = SimpleDirectoryReader(input_directory, required_exts=required_exts).load_data()

      # Delete the temp .md file after successful loading
      os.remove(input_directory)

      return documents
   else:
      print("No .md files found in the input directory.")

def create_collection(documents):
   """
   Create a new collection in Qdrant using the provided documents. This involves
   setting up the Qdrant client, creating a vector store, and initializing a 
   vector-based index for document storage and retrieval.
    
   Parameters:
   - documents (list): A list of document objects to be added to the collection.

   Returns:
   - str: Returns "success" if the collection is created successfully.
   """
   
   qdrant_client = QdrantClient(
      url=QDRANT_CLUSTER_URL, 
      api_key=QDRANT_API_KEY,
   )

   vector_store = QdrantVectorStore(
      collection_name=QDRANT_COLLECTION_NAME, client=qdrant_client, enable_hybrid=True, batch_size=10
   )

   storage_context = StorageContext.from_defaults(vector_store=vector_store)
   
   index = VectorStoreIndex.from_documents(
      documents,
      storage_context=storage_context,
   )

   return "success"