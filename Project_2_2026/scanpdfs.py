import os

# Directory containing the PDFs
PDF_DIRECTORY = "scanpdfs.py"
def get_pdf_list():
    """
    Scan the directory and return a sorted list of PDF files
    """

    try:
        files = os.listdir(PDF_DIRECTORY)

        pdf_files = [file for file in files if file.lower().endswith(".pdf")]

        pdf_files.sort()

        return pdf_files

    except FileNotFoundError:
        print("Directory not found.")
        return []