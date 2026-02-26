import sys
from PyPDF2 import PdfMerger

def myfunction():
#Initialize: Create a “merger” object that will hold all of our pages.
Merger = PdfMerger()
    if__name==’__main__’: 
if len(sys.argv)> 1:
Fname = sys.argv[1]
else:
print(‘error’)
myfunction(fname) #define your function at the top of code “def myfunction ():”
# list files in a directory
files = os,listdir(‘.’)
for f in files:
print(f)
#Only PDF files needed 
pdf_files = []
print (“/nPython Files:”)
for f in files:
If f.endswith(‘.py’):
pdf_files.append(f)
print(f)
#get operating system
print(‘OS Name: ‘, os.name)