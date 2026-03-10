import glob
from pdf_merger import output_pdf


def scan_pdfs(folder):
    """Scan the folder and return a list of PDF files."""
    filepaths = glob.glob(f"{folder}/*.pdf")
    return filepaths


def main():
    input_dir = "input_pdfs"

    # Step 1: Scan for PDFs
    pdf_files = scan_pdfs(input_dir)

    if not pdf_files:
        print("No PDF files found.")
        return

    print("\nPDF files found:")
    for file in pdf_files:
        print(f"- {file}")

    # Step 2: Ask user to merge
    choice = input("\nMerge these files? (y/n): ").lower()

    if choice == "y":
        merge_pdfs(pdf_files)
    else:
        print("Merge cancelled.")


if __name__ == "__main__":
    main()