from PyPDF2 import PdfReader

def findKeyword(document, pageNum, targetWord):
    """
    function reads in PDF document and extracts text from a specified
    page, then converts all text to lower case to count frequency
    of a target word
    :param document: the PDF document to be analyzed
    :param pageNum: the page number to extract text from
    :param targetWord: the specific keyword to count frequency
    :return: pageOutputLower is the extracted lowercase text
    """
    reader = PdfReader(document)
    page = reader.pages[pageNum]
    pageExtract = page.extract_text()
    pageOutput = pageExtract.split()
    pageOutputLower = [x.lower() for x in pageOutput]
    print(f"Searching page {pageNum} of {document} for {targetWord}")
    print(f"{len(pageOutputLower)} strings: {pageOutputLower}")
    if targetWord in pageOutputLower:
        wordCount = pageOutputLower.count(targetWord)
        print(f"yes, {targetWord} is in this page {wordCount} time(s)")
    else:
        print("no")
    return pageOutputLower

print("A simple search for a word in the text of a PDF document.")
findKeyword('DOT_PerformancePlan.pdf',20,'safety')
