from google_drive_file_downloads import *
from pdf_to_md import *
from markdown_to_vector_db import *
from gradio_chat_interface import *
from dotenv import load_dotenv
import subprocess

load_dotenv()

folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
output_dir = "data/downloads/temp/pdf/"

response = download_files_from_folder(folder_id,output_dir)

if response == "success":
    # Define the input and output directories
    input_directory = "data/downloads/temp/pdf/"
    output_directory = "data/downloads/temp/md/"
    
    response = convert_pdfs_to_md(input_directory, output_directory)
    if response:
        input_directory = "data/downloads/temp/md/"

        documents = load_documents(input_directory)
        response = create_collection(documents)

subprocess.run(["python", "gradio_chat_interface.py"])