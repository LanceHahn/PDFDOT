from PyPDF2 import PdfReader
from math import log
import seaborn as sns
import matplotlib.pyplot as plt

def findKeyword(document, pageNum, targetWord):
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

wList = findKeyword('DOT_PerformancePlan.pdf',20,'safety')

def cleanText(data):
    """
    cleans data entered into function, including eliminating punctuation characters and extra space
    :param data: list of values that need to be cleaned
    :return: list of cleaned data
    """
    cleaned = []
    for datum in data:
        clean = datum.rstrip()
        for char in ['.', ',', '"', "'", "?", '“', '\t', '\r', '\n',
                     '’', '”', ':']:
            clean = clean.replace(char, '')
        clean = clean.lower()
        if len(clean) > 0:
            cleaned.append(clean)
    print(cleaned)
    return cleaned

cleanedList = cleanText(wList)

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

wFreq = calculateDocFreqs(cleanedList)

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

scores = scoreWords(wList, wFreq)


def reportScores(scores, TopN):
    ix = 1
    for k, v in sorted(scores.items(), key=lambda item: -item[1]):
        if ix <= TopN:
            print(f"{ix:3} {k}: {v}")
            ix += 1
    return

reportScores(scores, 20)

# top 2 are numbers, most likely headers... should we eliminate all numerical values? is that too broad of a sweep?

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

reportHisto(scores,20)
