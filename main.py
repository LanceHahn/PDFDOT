from PyPDF2 import PdfReader

reader = PdfReader('DOT_PerformancePlan.pdf')

page = reader.pages[0]

text = page.extract_text()
print(text)