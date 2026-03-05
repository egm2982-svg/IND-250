import glob
import os
from PyPDF2 import PdfWriter

class PDFManager:
    def __init__(self):
        self.input_dir = "."
        self.pdf_files = []
        self.selected_files = []
        self.output_name = "merged_document.pdf"

    def scan_directory(self):
        """Finds all PDF files in the current directory."""
        self.pdf_files = glob.glob(f'{self.input_dir}/*.pdf')
        if not self.pdf_files:
            print(f"\n[!] No PDF files found in {os.path.abspath(self.input_dir)}")
        else:
            print(f"\n--- Found {len(self.pdf_files)} Files ---")
            for i, file in enumerate(self.pdf_files, 1):
                print(f"{i}. {os.path.basename(file)}")
        return self.pdf_files

    def select_files(self):
        """Allows the user to pick which files to merge."""
        if not self.pdf_files:
            print("\n[!] Please scan the directory first (Option 1).")
            return

        print("\nEnter file numbers separated by commas (e.g., 1,3) or type 'all':")
        choice = input("Selection: ").strip().lower()

        if choice == 'all':
            self.selected_files = self.pdf_files
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]
                self.selected_files = [self.pdf_files[i] for i in indices]
            except (ValueError, IndexError):
                print("[!] Invalid selection. Please try again.")
                return

        print(f"\nReady to merge {len(self.selected_files)} files.")

    def set_output_name(self):
        """Sets the name for the final merged file."""
        name = input("\nEnter the desired output filename (e.g., final_report): ").strip()
        if not name.endswith(".pdf"):
            name += ".pdf"
        self.output_name = name
        print(f"Output name set to: {self.output_name}")

    def run_merge(self):
        """Executes the actual PDF merging process."""
        if not self.selected_files:
            print("\n[!] No files selected for merging. Use Option 2.")
            return

        writer = PdfWriter()
        try:
            for filename in self.selected_files:
                writer.append(filename)
                print(f"Adding: {os.path.basename(filename)}")

            with open(self.output_name, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"\n✅ Success! Created: {self.output_name}")
            # Reset selection after successful merge
            self.selected_files = []
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        finally:
            writer.close()

    def menu(self):
        """Main control loop."""
        while True:
            print("\n" + "="*30)
            print("      PDF MERGER MENU")
            print("="*30)
            print("1. Scan for PDF Files")
            print("2. Select Files to Merge")
            print("3. Name Output File")
            print("4. Execute Merge")
            print("5. Quit")
            
            choice = input("\nChoose an option: ")

            if choice == "1":
                self.scan_directory()
            elif choice == "2":
                self.select_files()
            elif choice == "3":
                self.set_output_name()
            elif choice == "4":
                self.run_merge()
            elif choice == "5":
                print("Exiting program...")
                break
            else:
                print("[!] Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    manager = PDFManager()
    manager.menu()