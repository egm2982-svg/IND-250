import os
from PyPDF2 import PdfMerger

class PDFLibraryApp:
    def __init__(self):
        # Get the directory where THIS script is located
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Build path to pdf_library folder
        self.library_path = os.path.join(self.base_dir, "pdf_library")

        self.merger = PdfMerger()

    def list_pdfs(self):
        """List all PDF files in the library"""
        if not os.path.exists(self.library_path):
            print("❌ pdf_library folder not found!")
            return []

        files = os.listdir(self.library_path)
        pdfs = [f for f in files if f.endswith(".pdf")]

        print("\n📂 Available PDF Files:")
        for i, pdf in enumerate(pdfs, start=1):
            print(f"{i}. {pdf}")

        return pdfs

    def select_pdfs(self, pdfs):
        """Let user choose which PDFs to merge"""
        try:
            choices = input("\nEnter file numbers (comma-separated): ")
            indices = [int(x.strip()) - 1 for x in choices.split(",")]

            selected_files = [pdfs[i] for i in indices]
            return selected_files

        except (ValueError, IndexError):
            print("❌ Invalid selection.")
            return []

    def merge_pdfs(self, selected_files):
        """Merge selected PDFs"""
        if not selected_files:
            print("No files selected.")
            return

        output_name = input("Enter output file name: ")

        if not output_name.endswith(".pdf"):
            output_name += ".pdf"

        output_path = os.path.join(self.base_dir, output_name)

        for file in selected_files:
            full_path = os.path.join(self.library_path, file)
            print(f"Adding: {file}")
            self.merger.append(full_path)

        self.merger.write(output_path)
        self.merger.close()

        print(f"\n✅ Merged PDF saved as: {output_path}")

    def menu(self):
        """Main menu loop"""
        while True:
            print("\n===== PDF MERGER MENU =====")
            print("1. View PDF Library")
            print("2. Merge PDFs")
            print("3. Exit")

            choice = input("Select option: ")

            if choice == "1":
                self.list_pdfs()

            elif choice == "2":
                pdfs = self.list_pdfs()
                if pdfs:
                    selected = self.select_pdfs(pdfs)
                    self.merge_pdfs(selected)

            elif choice == "3":
                print("Exiting program.")
                break

            else:
                print("❌ Invalid choice.")


if __name__ == "__main__":
    app = PDFLibraryApp()
    app.menu()