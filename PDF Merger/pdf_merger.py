import glob
from PyPDF2 import PdfWriter


def pdf_merger(input_dir="input_pdfs", output_filename="merged_output.pdf"):
    """
    Merge all PDF files in a directory into a single PDF.
    
    Parameters:
    input_dir (str): Folder containing PDF files
    output_filename (str): Name of the merged output file
    """

    # 1. Get list of PDF files
    filepaths = glob.glob(f"{input_dir}/*.pdf")

    if not filepaths:
        print("No PDF files found.")
        return

    # 2. Create PdfWriter object
    pdf_writer = PdfWriter()

    for filepath in filepaths:
        print(f"Appending: {filepath}")
        pdf_writer.append(filepath)

    # 3. Write merged file
    with open(output_filename, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"\nPDFs merged successfully into '{output_filename}'")


# Allows the script to run independently if executed directly
if __name__ == "__main__":
    pdf_merger()