from PyPDF2 import PdfWriter 

writer = PdfWriter()

pdfs = ["About Barbers.pdf, Luck.pdf, PDF Merger(1).pdf, PDF Merger.pdf, The Child's Story.pdf, Wit Inspiration of the Two Year Olds.pdf"]

for pdf in pdfs:
        writer.append(pdf)

writer.write("Mergerd.pdf")
print("PDF files successfully merged!")