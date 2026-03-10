import os
from merger_function import merge_files


# Folder where PDFs exist

def scan_for_pdfs():

    files = os.listdir(PDF_DIRCTORY)

    pdfs = [f for f in files if f.lower().endswith(".pdf")]

    pdfs.sort()

    print("\nPDF files found:", len(pdfs))

    for file in pdfs:
        print(file)

    return pdfs


def main():

    pdfs = scan_for_pdfs()

    if len(pdfs) < 2:
        print("Need at least two PDF files to merge.")
        return

    choice = input("\nMerge the first two files? (y/n): ")

    if choice.lower() == "y":

        files_to_merge = [pdfs[0], pdfs[1]]

        print("\nSelected files:")
        print(files_to_merge[0])
        print(files_to_merge[1])

        output_name = input("\nEnter merged file name: ")

        # Send files to merge function
        merge_files(files_to_merge, PDF_Directory, output_name)

    else:
        print("Merge cancelled.")


if __name__ == "__main__":
    main()