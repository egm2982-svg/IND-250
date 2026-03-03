import sys
import os
from PyPDF2 import PdfMerger, PdfReader


class PDFMergerApp:
    def __init__(self):
        """Initialize merger object"""
        self.merger = PdfMerger()
        self.pdf_files = []
        self.output_name = ""

    def validate_args(self):
        """Step 1 & 2: Read command-line argument"""
        if len(sys.argv) < 2:
            print("❌ Error: Merge file name not specified.")
            print("Usage: python pdfmerger.py filename")
            sys.exit(1)

        self.output_name = sys.argv[1] + ".pdf"

    def get_pdf_files(self):
        """Step 4, 5, 6: Retrieve, Filter, Sort"""
        files = os.listdir(".")

        # Filter only PDFs
        self.pdf_files = [f for f in files if f.endswith(".pdf")]

        # Remove output file if it already exists
        self.pdf_files = [f for f in self.pdf_files if f != self.output_name]

        # Sort alphabetically
        self.pdf_files.sort()

    def report_files(self):
        """Step 7: Report files found"""
        print(f"\n📄 PDF files found: {len(self.pdf_files)}")
        print("List:\n")

        for file in self.pdf_files:
            print(file)

    def confirm_continue(self):
        """Step 8: Prompt user"""
        choice = input("\nContinue (y/n): ").lower()
        return choice == "y"

    def merge_files(self):
        """Step 9: Append files"""
        for pdf in self.pdf_files:
            print(f"Adding: {pdf}")
            self.merger.append(pdf)

    def save_output(self):
        """Step 10: Export merged PDF"""
        self.merger.write(self.output_name)
        self.merger.close()

        print(f"\n✅ Merged file saved as: {self.output_name}")

    def extract_text_bonus(self):
        """Bonus: Extract text to .txt file"""
        choice = input("\nExtract text to .txt file? (y/n): ").lower()

        if choice != "y":
            return

        txt_filename = self.output_name.replace(".pdf", ".txt")

        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            reader = PdfReader(self.output_name)

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    txt_file.write(text + "\n")

        print(f"📝 Text extracted to: {txt_filename}")

    def run(self):
        """Main application flow"""
        self.validate_args()
        self.get_pdf_files()

        if not self.pdf_files:
            print("❌ No PDF files found in current directory.")
            return

        self.report_files()

        if not self.confirm_continue():
            print("Operation cancelled.")
            return

        self.merge_files()
        self.save_output()
        self.extract_text_bonus()


if __name__ == "__main__":
    app = PDFMergerApp()
    app.run()