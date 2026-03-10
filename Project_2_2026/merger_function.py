from PyPDF2 import PdfMerger
import os


def merge_files(file_list, folder_path, output_name):
    """
    Merge a list of PDF files and return the saved file path
    """

    merger = PdfMerger()

    for file in file_list:
        full_path = os.path.join(folder_path, file)
        print("Adding:", file)
        merger.append(full_path)

    if not output_name.endswith(".pdf"):
        output_name += ".pdf"

    output_path = os.path.join(folder_path, output_name)

    merger.write(output_path)
    merger.close()

    print("\nMerged file saved as:", output_path)

    return output_path