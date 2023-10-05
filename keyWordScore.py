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


def findKeyword(document, pageNum):
    """
    reads in PDF document, extracts text, and splits text into list.
    converts all values into lower case.
    ** consider eliminating numerical values in this function **
    :param document: PDF document to analyze
    :param pageNum: page number you are searching
    :param targetWord: keyword to find
    :return: list of values extracted from PDF
    """
    reader = PdfReader(document)
    page = reader.pages[pageNum]
    pageExtract = page.extract_text()
    pageOutput = pageExtract.split()
    pageOutputLower = [x.lower() for x in pageOutput]
    return pageOutputLower


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


def calculateDocFreqs(wList):
    """
    takes in a list and counts the frequency of values in list
    :param wList: a list whose values will be counted
    :return: dictionary of value in list and its frequency in that list
    """
    wFreq = dict()
    for w in wList:
        if w not in wFreq.keys():
            count = 0
            for ix in range(len(wList)):
                if w == wList[ix]:
                    count += 1
            wFreq[w] = count
    return wFreq


def scoreWords(wList, wFreq):
    """
    calculates tf-idf score for each value in dictionary
    :param wList: list of values whose frequency are counted
    :param wFreq: dictionary that gives value:frequency
    :return:
    """
    docFreqs = calculateDocFreqs(wList)
    scores = dict()
    maxFreq = max(docFreqs.values())
    for word in docFreqs.keys():
        tf = 0.5 + 0.5 * (docFreqs[word] / maxFreq)
        if word in wFreq.keys():
            idf = log(500/(1+wFreq[word]))
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




def realWords(cleanedList):
    """
    checks cleanedList of extracted text against KFreq file
    :param cleanedList: extracted text to analyze
    :return: realWordList is value that is found in both cleanedList and KFreq
    """
    realWordList = []
    nonWordList = []
    for i in cleanedList:
        if i in KFreqList:
            realWordList.append(i)
        else:
            nonWordList.append(i)
    return realWordList

def nonWords(cleanedList, goodWords):
    """
    checks cleanedList of extracted text against KFreq file
    :param cleanedList: extracted text to analyze
    :return: nonWordsList is value that is in cleanedList but not in KFreq file
    """
    realWordList = []
    nonWordList = []
    for i in cleanedList:
        if i in goodWords:
            realWordList.append(i)
        else:
            nonWordList.append(i)
    return nonWordList


if __name__ == "__main__":

    KFreq = readCSV('KFfreq.csv')

    dictFreqs = getFreqs('KFfreq.csv')
    KFreqList = list(dictFreqs)

    wList = findKeyword('DOT_PerformancePlan.pdf',20)
    cleanedList = cleanText(wList)
    wFreq = calculateDocFreqs(cleanedList)
    scores = scoreWords(cleanedList, wFreq)
    reportScores(scores, 5)
    # top 2 are numbers, most likely headers... should we eliminate all numerical values? is that too broad of a sweep?

    # reportHisto(scores,5)

    realWordsList = realWords(cleanedList)
    nonWordsList = nonWords(cleanedList, KFreqList)


    reportScores(scoreWords(realWordsList, wFreq), 5)
    reportScores(scoreWords(nonWordsList, wFreq), 10)