import os
from PyPDF2 import PdfMerger, PdfReader

class PDFMergerApp:
    """
    Menu-driven PDF Merger Application

    Features:
    - Loads PDFs from a dedicated library folder
    - Merges files
    - Extracts text
    - Clean file handling with full paths
    """

    def __init__(self):
        self.pdf_files = []              # Stores FULL file paths
        self.output_name = "merged_output.pdf"

    def load_files(self):
        """
        Load PDF files from Project Two Library folder.
        """
        library_path = get_library_path()

        if not os.path.exists(library_path):
            print("\n❌ Library folder not found.")
            print("Expected folder: /pdf_library")
            return

        files = os.listdir(library_path)

        self.pdf_files = [
            os.path.join(library_path, f)
            for f in files
            if f.endswith(".pdf") and f != self.output_name
        ]

        print(f"\n✅ Found {len(self.pdf_files)} PDF file(s).")

    def display_files(self):
        """
        Display available PDF files (clean names only).
        """
        if not self.pdf_files:
            print("\n⚠️ No PDF files loaded.")
            return

        print("\n📄 Available PDF Files:")
        for i, file in enumerate(self.pdf_files, start=1):
            print(f"{i}. {os.path.basename(file)}")

    def set_output_name(self):
        """
        Set output file name.
        """
        name = input("Enter output file name (without .pdf): ").strip()

        if not name:
            print("⚠️ Invalid name.")
            return

        self.output_name = name + ".pdf"
        print(f"✅ Output file set to: {self.output_name}")

    def merge_pdfs(self):
        """
        Merge all loaded PDFs.
        """
        if not self.pdf_files:
            print("\n⚠️ No PDFs loaded. Use option 1 first.")
            return

        confirm = input("Merge all PDFs? (y/n): ").lower()
        if confirm != "y":
            print("❌ Merge cancelled.")
            return

        merger = PdfMerger()

        for pdf in self.pdf_files:
            print(f"Adding: {os.path.basename(pdf)}")
            merger.append(pdf)

        merger.write(self.output_name)
        merger.close()

        print(f"\n✅ Merged PDF created: {self.output_name}")

    def extract_text(self):
        """
        Extract text from merged PDF into a .txt file.
        """
        if not os.path.exists(self.output_name):
            print("\n⚠️ Merged file not found. Merge first.")
            return

        reader = PdfReader(self.output_name)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        txt_name = self.output_name.replace(".pdf", ".txt")

        with open(txt_name, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"\n📝 Text extracted to: {txt_name}")

    def show_system_info(self):
        """
        Display system information.
        """
        print("\n🖥️ System Info:")
        print("OS Name:", os.name)

    def menu(self):
        """
        Main menu loop.
        """
        while True:
            print("\n===== PDF MERGER MENU =====")
            print("1. Load PDF Files from Library")
            print("2. Show PDF Files")
            print("3. Set Output File Name")
            print("4. Merge PDFs")
            print("5. Extract Text (Bonus)")
            print("6. Show System Info")
            print("7. Exit")

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("❌ Invalid input. Enter a number.")
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
                print("👋 Exiting program.")
                break
            else:
                print("❌ Invalid selection.")


if __name__ == "__main__":
    app = PDFMergerApp()
    app.menu()