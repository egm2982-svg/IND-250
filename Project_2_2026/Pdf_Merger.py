import sys
import os

def main():
    # 1. Check command-line argument
    if len(sys.argv) < 2:
        print("Error: Merge file name not specified.")
        print("Usage: python pdfmerger.py filename")
        return

    output_name = sys.argv[1] + ".pdf"

    # 3. Create merger object
    merger = PdfMerger()

    # 4–6. Get, filter, sort PDF files
    files = [f for f in os.listdir() if f.endswith(".pdf")]

    files.sort()

    # Remove output file if it exists
    files = [f for f in files if f != output_name]

    # 7. Report
    print(f"\nPDF files found: {len(files)}")
    print("List:")
    for file in files:
        print(file)

    # 8. Confirm
    choice = input("\nContinue (y/n): ").lower()
    if choice != 'y':
        print("Operation cancelled.")
        return

    # 9. Append files
    for file in files:
        merger.append(file)

    # 10. Save output
    merger.write(output_name)
    merger.close()

    print(f"\nMerged file created: {output_name}")

    # BONUS: Extract text
    bonus = input("Extract text to .txt file? (y/n): ").lower()
    if bonus == 'y':
        extract_text(output_name)

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    txt_name = pdf_file.replace(".pdf", ".txt")
    with open(txt_name, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Text extracted to {txt_name}")

if __name__ == "__main__":
    main()
