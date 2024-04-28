# import necessary documents
import os
import io
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Path to your service account JSON key
SERVICE_ACCOUNT_FILE = 'data/service_account/key.json'

# Define the necessary Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

downloaded_files_list_path = "data/downloads/downloaded_files_path.txt"

def download_files_from_folder(folder_id,output_dir):
    """
    Lists all files in a specified Google Drive folder and downloads each file to a local directory.

    Parameters:
    - folder_id (str): The ID of the Google Drive folder to list files from.
    - output_dir (str): The directory where downloaded files will be saved.

    Returns:
    - None
    """
    # Create a credentials object from the service account file
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    
    # Load previously downloaded files from the text file
    if os.path.exists(downloaded_files_list_path):
        with open(downloaded_files_list_path, 'r') as f:
            downloaded_files = set(f.read().splitlines())
    else:
        downloaded_files = set()

    # Search query to find all files within the specified folder
    query = f"'{folder_id}' in parents"

    # Use the Google Drive API to list files in the folder
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    newly_downloaded_files = []

    # Display the names of the files and download them
    if not files:
        print("No files found in the folder.")
        return "not success"
    else:
        print("Files in the folder:")
        for file in files:
            file_name = file['name']
            if file_name in downloaded_files:
                print(f"Skipping '{file_name}', already downloaded.")
                continue

            file_id = file['id']

            # Get file metadata to retrieve the file name
            file_metadata = service.files().get(fileId=file_id, fields="id, name").execute()
            file_name = file_metadata['name']
            print(f"Downloading '{file_name}'...")

            # Prepare to download the file content
            request = service.files().get_media(fileId=file_id)
            file_stream = io.BytesIO()  # Use a BytesIO stream for in-memory download

            downloader = MediaIoBaseDownload(file_stream, request)

            # Download the file content in chunks
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% complete.")

            # Create a local directory to save the file if needed
            os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

            # Define the output file path
            file_path = os.path.join(output_dir, file_name)

            # Save the downloaded file to the local system
            with open(file_path, 'wb') as output_file:
                # Write the downloaded bytes to the file
                output_file.write(file_stream.getvalue())

            print(f"File '{file_name}' downloaded successfully to '{file_path}'.")
            
            # Update the downloaded files set
            downloaded_files.add(file_name)
            newly_downloaded_files.append(file_name)

            # Save the updated list of downloaded files back to the text file
            with open(downloaded_files_list_path, 'w') as f:
                f.write('\n'.join(sorted(downloaded_files)))

            return "success"