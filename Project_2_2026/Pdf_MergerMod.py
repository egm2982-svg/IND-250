import os
from PyPDF2 import PdfMerger

class PDFLibraryApp:
    def __init__(self, library_path="pdf_library"):
        # Folder where your PDFs live
        self.library_path = library_path
        self.merger = PdfMerger()

    def list_pdfs(self):
        """List all PDF files in the library"""
        files = os.listdir(self.library_path)
        pdfs = [f for f in files if f.endswith(".pdf")]

        print("\nAvailable PDF Files:")
        for i, pdf in enumerate(pdfs, start=1):
            print(f"{i}. {pdf}")

        return pdfs

    def select_pdfs(self, pdfs):
        """Let user choose which PDFs to merge"""
        choices = input("\nEnter file numbers to merge (comma-separated): ")
        indices = [int(x.strip()) - 1 for x in choices.split(",")]

        selected_files = [pdfs[i] for i in indices]
        return selected_files

    def merge_pdfs(self, selected_files, output_name="merged_output.pdf"):
        """Merge selected PDFs"""
        for file in selected_files:
            full_path = os.path.join(self.library_path, file)
            print(f"Adding: {file}")
            self.merger.append(full_path)

        self.merger.write(output_name)
        self.merger.close()

        print(f"\nMerged PDF saved as: {output_name}")

    def run(self):
        """Main app flow"""
        pdfs = self.list_pdfs()

        if not pdfs:
            print("No PDF files found in library.")
            return

        selected = self.select_pdfs(pdfs)
        self.merge_pdfs(selected)


if __name__ == "__main__":
    app = PDFLibraryApp()
    app.run()