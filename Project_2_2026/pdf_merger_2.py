import os
from PyPDF2 import PdfMerger, PdfReader


class PDFMergerApp:

    def __init__(self):
        # Get the folder where THIS script lives
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # PDFs are in the SAME folder as the script (based on your screenshot)
        self.library_folder = self.base_dir

        # Output file name
        self.output_filename = "PDF_Merger_2.pdf"
        self.output_path = os.path.join(self.library_folder, self.output_filename)

    # --------------------------------------------------
    # Retrieve, Filter, Sort
    # --------------------------------------------------
    def get_pdf_files(self):

        files = os.listdir(self.library_folder)

        pdfs = [
            f for f in files
            if f.lower().endswith(".pdf")
            and f != self.output_filename  # prevent merging output file
        ]

        pdfs.sort()
        return pdfs

    # --------------------------------------------------
    # Report Files
    # --------------------------------------------------
    def report_files(self, pdfs):
        print(f"\nPDF files found: {len(pdfs)}")
        print("List:\n")

        for file in pdfs:
            print(file)

    # --------------------------------------------------
    # Merge Logic
    # --------------------------------------------------
    def merge_pdfs(self, extract_text=False):

        pdf_files = self.get_pdf_files()

        if not pdf_files:
            print("No PDF files found.")
            return

        self.report_files(pdf_files)

        confirm = input("\nContinue (y/n): ").lower()
        if confirm != "y":
            print("Operation cancelled.")
            return

        merger = PdfMerger()

        for pdf in pdf_files:
            full_path = os.path.join(self.library_folder, pdf)
            print(f"Adding: {pdf}")
            merger.append(full_path)

        merger.write(self.output_path)
        merger.close()

        print(f"\nMerged file created: {self.output_path}")

        if extract_text:
            self.extract_text()

    # --------------------------------------------------
    # Bonus Text Extraction
    # --------------------------------------------------
    def extract_text(self):

        print("\nExtracting text...")

        reader = PdfReader(self.output_path)
        text_content = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content += text + "\n"

        text_filename = self.output_filename.replace(".pdf", ".txt")
        text_path = os.path.join(self.library_folder, text_filename)

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text_content)

        print(f"Text saved as: {text_path}")

    # --------------------------------------------------
    # Menu Interface
    # --------------------------------------------------
    def menu(self):

        while True:
            print("\n===== PDF MERGER MENU =====")
            print("1. Scan Current Project Folder")
            print("2. Merge PDFs into PDF_Merger_2.pdf")
            print("3. Merge + Extract Text")
            print("4. Exit")

            choice = input("Select option: ")

            if choice == "1":
                pdfs = self.get_pdf_files()
                self.report_files(pdfs)

            elif choice == "2":
                self.merge_pdfs()

            elif choice == "3":
                self.merge_pdfs(extract_text=True)

            elif choice == "4":
                print("Exiting program.")
                break

            else:
                print("Invalid selection.")


# --------------------------------------------------
# Program Entry
# --------------------------------------------------
if __name__ == "__main__":
    app = PDFMergerApp()
    app.menu()