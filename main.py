from PyPDF2 import PdfReader

def findKeyword(document, pageNum, targetWord):
    reader = PdfReader(document)
    page = reader.pages[pageNum]
    pageExtract = page.extract_text()
    pageOutput = pageExtract.split()
    pageOutputLower = [x.lower() for x in pageOutput]
    print(pageOutputLower)
    if targetWord in pageOutputLower:
        wordCount = pageOutputLower.count(targetWord)
        print(f"yes, {targetWord} is in this page {wordCount} time(s)")
    else:
        print("no")
    return

findKeyword('DOT_PerformancePlan.pdf',20,'safety')

# need to find some ranking system for word counts
# highest word count is most relevant