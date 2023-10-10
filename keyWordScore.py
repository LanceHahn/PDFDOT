from PyPDF2 import PdfReader
from math import log
import seaborn as sns
import matplotlib.pyplot as plt

def readCSV(fName):
    with open(fName, 'r') as f:
        data = f.readlines()
    cleaned = []
    for datum in data:
        clean0 = datum.rstrip()
        row = clean0.split(',')
        cleaned.append(row)
    return cleaned


def getFreqs(fName):
    freqDict = dict()
    freqData = readCSV(fName)
    for row in freqData:
        freqDict[row[0]] = int(row[1])
    return freqDict


def extractList(document, pageNum):
    """
    reads in PDF document, extracts text, and splits text into list.
    converts all values into lower case.
    :param document: PDF document to analyze
    :param pageNum: page number you are searching
    :return: list of values extracted from PDF
    """
    reader = PdfReader(document)
    page = reader.pages[pageNum]
    pageExtract = page.extract_text()
    pageOutput = pageExtract.split()
    pageOutput = [x.lower() for x in pageOutput]
    return pageOutput

def extractDict(document):
    """
    uses PyPDF2 to extract text from a page of a given document,
    iterated over all pages in a documnet
    :param document: document to be read in
    :return: textDict: dictionary where key is page num and value is list of text
    """
    textDict = {}
    reader = PdfReader(document)
    totalPages = len(reader.pages)
    for i in range(totalPages):
        page = reader.pages[i]
        pageExtract = page.extract_text()
        pageOutput = pageExtract.split()
        pageOutput = [x.lower() for x in pageOutput]
        textDict[i] = pageOutput
    return textDict


def cleanText(data):
    """
    cleans data entered into function, including eliminating punctuation characters and extra space
    :param data: list of values that need to be cleaned
    :return: list of cleaned data
    """
    cleaned = []
    for datum in data:
        clean = datum.rstrip()
        digits = ['0','1','2','3','4','5','6','7','8','9']
        for char in ['.', ',', '"', "'", "?", '“', '\t', '\r', '\n',
                     '’', '”', ':', '*', '|', '%','(',')','[',']',
                     '•', '&'] + digits:
            clean = clean.replace(char, '')
        clean = clean.lower()
        if len(clean) > 0:
            cleaned.append(clean)
    return cleaned


def calculateDocFreqs(wordList):
    """
    takes in a list and counts the frequency of values in list
    :param wordList: a list whose values will be counted
    :return: wordFreq: dictionary of value in list and its frequency in that list
    """
    wordFreq = dict()
    for w in wordList:
        if w not in wordFreq.keys():
            count = 0
            for ix in range(len(wordList)):
                if w == wordList[ix]:
                    count += 1
            wordFreq[w] = count
    return wordFreq


def scoreWords(wordList, wordFreq):
    """
    calculates tf-idf score for each value in dictionary
    :param wordList: list of values whose frequency are counted
    :param wordFreq: dictionary that gives value:frequency
    :return:
    """
    docFreqs = calculateDocFreqs(wordList)
    scores = dict()
    maxFreq = max(docFreqs.values())
    for word in docFreqs.keys():
        tf = 0.5 + 0.5 * (docFreqs[word] / maxFreq)
        if word in wordFreq.keys():
            idf = log(500/(1+wordFreq[word]))
        else:
            idf = log(500/1)
        scores[word] = tf * idf
    return scores



def reportScores(scores, TopN):
    ix = 1
    for k, v in sorted(scores.items(), key=lambda item: -item[1]):
        if ix <= TopN:
            print(f"{ix:3} {k}: {v}")
            ix += 1
    return



def reportHisto(histogram, TopN, title="title", xLabel = 'xLabel'):
    """
    plots a histogram provided with a title
    :param histogram: a dict containing words as keys and the number of
    times the importance measure as value.
    :param title: title of plot
    :return: None
    """
    words = []
    freqs = []
    ix = 1
    for k, v in sorted(histogram.items(), key=lambda item: -item[1]):
        if ix <= TopN:
            words.append(k)
            freqs.append(histogram[k])
        ix += 1
    ax = sns.barplot(y=xLabel, x='word',
                     data={xLabel: words, 'word': freqs},
                     palette="rocket_r")
    ax.set(xlabel=xLabel, title=title)
    plt.show()
    return




def realWords(cleanedList, freqFile):
    """
    checks cleanedList of extracted text against KFreq file
    :param cleanedList: extracted text to analyze
    :return: realWordList is value that is found in both cleanedList and KFreq
    """
    realWordList = []
    dictFreqs = getFreqs(freqFile)
    libraryList = list(dictFreqs)
    for i in cleanedList:
        if i in libraryList:
            realWordList.append(i)
    return realWordList

def nonWords(cleanedList, freqFile):
    """
    checks cleanedList of extracted text against KFreq file
    :param cleanedList: extracted text to analyze
    :return: nonWordsList is value that is in cleanedList but not in KFreq file
    """
    nonWordsList = []
    dictFreqs = getFreqs(freqFile)
    libraryList = list(dictFreqs)
    for i in cleanedList:
        if i not in libraryList:
            nonWordsList.append(i)
    return nonWordsList


if __name__ == "__main__":

    # list of extracted text from PDF
    wList = extractList('DOT_PerformancePlan.pdf',20)

    # cleaned list of extracted text
    newList = cleanText(wList)

   # frequency that words apepar in cleaned list
    wFreq = calculateDocFreqs(newList)

    # calculated tf-idf scores of each word in cleaned list
    wordScores = scoreWords(newList, wFreq)

    # print words with top five tf-idf scores
    reportScores(wordScores, 5)

    # words that are in cleaned list and KF frequency file
    realList = realWords(newList, 'KFfreq.csv')

    # words that are in cleaned list but not in KF frequency file
    nonList = nonWords(newList, 'KFfreq.csv')

    # top 5 tf-idf scores of 'real' words
    reportScores(scoreWords(realList, wFreq), 5)

    # top 10 tf-idf scores of 'non-real' words
    reportScores(scoreWords(nonList, wFreq), 10)