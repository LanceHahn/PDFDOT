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


def cleanText(data):

    cleaned = []
    for datum in data:
        clean = datum.rstrip()
        for char in ['.', ',', '"', "'", "?", '“', '\t', '\r', '\n',
                     '’', '”', ':']:
            clean = clean.replace(char, '')
        clean = clean.lower()
        if len(clean) > 0:
            cleaned.append(clean)
    return cleaned


def readTxt(fName):
    with open(fName, 'r') as f:
        data = f.readlines()
    return data


def makeList(text):
    wordList = []
    for line in text:
        lineList = line.split(' ')
        for word in lineList:
            wordList.append(word)
    return wordList


def calculateDocFreqs(wList):
    wFreqs = dict()
    for w in wList:
        if w not in wFreqs.keys():
            count = 0
            for ix in range(len(wList)):
                if w == wList[ix]:
                    count += 1
            wFreqs[w] = count
    return wFreqs


def scoreWords(wList, wFreq):
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


def getParams():
    freqFile = input("What word freq file (default: KFfreq.csv)? ")
    if len(freqFile) < 1:
        freqFile = 'KFfreq.csv'
    TopN = int(input("How many keywords to display? "))
    textFile = input("Name of text file to process (blank to avoid using a file)? ")
    if len(textFile) < 1:
        text = [input("What text to process? ")]
    else:
        text = ''
    return freqFile, TopN, textFile, text

def main():
    freqFile, TopN, textFile, text = getParams()
    wordFreq = getFreqs(freqFile)
    if len(text) < 1:
        text = readTxt(textFile)
    text = cleanText(text)
    wordList = makeList(text)
    scores = scoreWords(wordList, wordFreq)
    reportScores(scores, TopN=TopN)
    reportHisto(scores, TopN,
                title=f"{TopN} Keywords",
                xLabel=f'approx TF-IDF')
    return

if __name__ == '__main__':
    main()