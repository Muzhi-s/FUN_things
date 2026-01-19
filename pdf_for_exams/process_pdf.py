from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("题库3.pdf")
reader.decrypt("CISP6666")

writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

with open("题3.pdf", "wb") as f:
    writer.write(f)