import os
import sys
from PyPDF2 import PdfMerger

def merge(out_file):
# 3. Initialize: Create a “merger” object that will hold all of our pages.
merger = PdfMerger()

# 4. Retrieve: Collect the names of files in the current directory.
pdf_files = [] # initialize empty list
all_files = os.listdir('.') # grab the files in the current directory
for f in all_files: # iterate through all files found in the current directory
if f.endswith('.pdf') and f != out_file: # 5. Filter and don't include outfile in list if it exists
pdf_files.append(f) # save just the pdf files for merging later

# 6. Sort: Put the files in alphabetical order.
pdf_files.sort() # sorts in place (alters the original file)

# 7. Report: List files found and count to the user.
# PDF files found: 2
# List:
# File1.pdf
# File2.pdf
print('PDF files found: ', len(pdf_files)) # prints the number of pdf files found
for f in pdf_files: # iterate through and print out all the pdf files
print(' ', f)

# 8. Prompt: Ask the user whether to continue operation: Continue (y/n):
prompt = input('Continue (y/n): ')
if prompt[0].lower() == 'y':
for f in pdf_files:
merger.append(f) # add the file to the merger object
print(f"Adding: {f}") # echo status back to user
merger.write(out_file) # write merged pdf file to disk
merger.close()

# 1. Read: Read the output file name from the command line. I.e. if the invocation is “python pdfmerger.py my_files”
# then the merged file will be my_files.pdf.
# 2. If a name is not specified, terminate the script with a message: Error: Merge file name not specified.
# Usage: python pdfmerger.py filename
if __name__ == "__main__":
if len(sys.argv) > 1:
if sys.argv[1].endswith('.pdf'): # if user appended .pdf to outfile then pass it through
out_file = sys.argv[1]
else:
out_file = sys.argv[1] + '.pdf' # if not add it
merge(out_file) # pass out file name to merge function
else:
print('Error: Merge file name not specified. Usage: python pdfmerger.py filename')