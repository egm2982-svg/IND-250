import os
import sys
from PyPDF2 import PdfMerger, PdfReader


class PDFMergerApp:
    """
    A menu-driven PDF Merger application.

    Teaches:
    - Object-Oriented Programming (OOP)
    - File handling
    - User interaction
    - Program state management
    """

    def __init__(self):
        # 🔵 Store list of PDF files
        self.pdf_files = []

        # 🔵 Default output file name
        self.output_name = "merged_output.pdf"

    def load_files(self):
        """
        Scan current directory and store PDF files.
        """
        files = os.listdir('.')

        # Filter only PDF files
        self.pdf_files = [f for f in files if f.endswith('.pdf') and f != self.output_name]

        print(f"\nFound {len(self.pdf_files)} PDF file(s).")

    def display_files(self):
        """
        Display available PDF files.
        """
        if not self.pdf_files:
            print("\nNo PDF files found.")
            return

        print("\nAvailable PDF Files:")
        for i, file in enumerate(self.pdf_files, start=1):
            print(f"{i}. {file}")

    def set_output_name(self):
        """
        Allow user to define output file name.
        """
        name = input("Enter output file name (without .pdf): ")
        self.output_name = name + ".pdf"
        print(f"Output file set to: {self.output_name}")

    def merge_pdfs(self):
        """
        Merge all PDF files into one output file.
        """
        if not self.pdf_files:
            print("\nNo PDFs to merge.")
            return

        confirm = input("Merge all PDFs? (y/n): ").lower()
        if confirm != 'y':
            print("Merge cancelled.")
            return

        merger = PdfMerger()

        for pdf in self.pdf_files:
            print(f"Adding: {pdf}")
            merger.append(pdf)

        merger.write(self.output_name)
        merger.close()

        print(f"\n✅ Merged PDF created: {self.output_name}")

    def extract_text(self):
        """
        BONUS: Extract text from merged PDF into a .txt file.
        """
        if not os.path.exists(self.output_name):
            print("\nMerged file not found. Merge PDFs first.")
            return

        reader = PdfReader(self.output_name)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        txt_name = self.output_name.replace(".pdf", ".txt")

        with open(txt_name, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"\n📄 Text extracted to: {txt_name}")

    def show_system_info(self):
        """
        Display operating system info.
        """
        print("\nSystem Info:")
        print("OS Name:", os.name)

    def menu(self):
        """
        Main menu loop (user interface).
        """
        while True:
            print("\n===== PDF MERGER MENU =====")
            print("1. Load PDF Files")
            print("2. Show PDF Files")
            print("3. Set Output File Name")
            print("4. Merge PDFs")
            print("5. Extract Text (Bonus)")
            print("6. Show System Info")
            print("7. Exit")

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("Invalid input. Enter a number.")
                continue

            if choice == 1:
                self.load_files()
            elif choice == 2:
                self.display_files()
            elif choice == 3:
                self.set_output_name()
            elif choice == 4:
                self.merge_pdfs()
            elif choice == 5:
                self.extract_text()
            elif choice == 6:
                self.show_system_info()
            elif choice == 7:
                print("Exiting program.")
                break
            else:
                print("Invalid selection.")


# 🔵 Entry point of program
if __name__ == "__main__":
    app = PDFMergerApp()
    app.menu()
    