import os
from llama_parse import LlamaParse
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()

load_dotenv()

# Load .env variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LLAMAPARSE_API_KEY = os.environ.get("LLAMAPARSE_API_KEY")
    
def convert_pdfs_to_md(input_directory, output_directory):
    """
    Converts all PDF files in the specified input directory to Markdown format
    and writes the converted content to the specified output directory. If a
    PDF file is successfully converted, the original PDF file is deleted.

    Parameters:
    - input_directory (str): The path to the directory containing the PDF files.
    - output_directory (str): The path to the directory where the Markdown files should be saved.

    Returns:
    - str: Returns "success" if the conversion was successful, otherwise indicates if no PDF files were found.
    """

    # Check if there are any PDF files in the input directory
    pdf_files_exist = any(file_name.endswith(".pdf") for file_name in os.listdir(input_directory))

    if pdf_files_exist:

        # Initialize LlamaParse parser
        parser = LlamaParse(
            api_key=LLAMAPARSE_API_KEY, 
            result_type="markdown",
            max_timeout=300,
            parsing_instruction='''
            TASK: Convert the provided document to a markdown format. Should the document contain any tables, please convert them to sentence form without altering the content structure. The information in the table needs to be extracted by you. Showcase the information covered in the table. Avoid creating any new tables as well.
            STEPS: 1) Read the entire document.
                2) Assume that a multi-page document consists of a single, scrollable page, similar to a web page that contains all of the document's pages.
                3) Convert the single page document into markdown format.
                4) When converting, make sure you only use heading syntax where it is appropriate and avoid using any particular markdown format grammar.

            RULES: 1) Avoid saying things like, "You're asking for a table to be converted," or "The knowledge in the provided table is."
                2) Verify that the answer contains the information from every row.
                3) Confirm the document's hierarchy when it is converted to markdown format.
            '''
        )

        # Iterate over PDF files in the directory
        for file_name in os.listdir(input_directory):
            if file_name.endswith(".pdf"):
                pdf_file_path = os.path.join(input_directory, file_name)
                md_file_path = os.path.join(output_directory, file_name.replace(".pdf", ".md"))

                # Load PDF data and convert to Markdown
                documents = parser.load_data(pdf_file_path)
                content = documents[0].text

                # Write the converted Markdown content to the output file
                with open(md_file_path, 'w', encoding="utf-8") as output_file:
                    output_file.write(content)
            
                print(".md created successfully")
            
                # Delete the original PDF file after successful conversion
                os.remove(pdf_file_path)

                return "success"
    else:
        print("No PDF files found in the input directory.")