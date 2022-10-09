import argparse
import time
from tkinter import *
from tkinter import filedialog
import sys
import math
isRecursionSet = 0

def getPartition(array, low, high):
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1


def quickSort(array, low, high):
    if low < high:
        pi = getPartition(array, low, high)
        quickSort(array, low, pi - 1)
        quickSort(array, pi + 1, high)


def sortWrapper(listToSort):
    global isRecursionSet
    if isRecursionSet == 0:
        sys.setrecursionlimit(1500)
        isRecursionSet = 1
    listCopy = listToSort.copy()
    quickSort(listCopy, 0, len(listCopy) - 1)
    return listCopy


def openFileDialog():  # Path to file (string)
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path


def getRawViews(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    i = 0
    size = int(lines[0][:-1])
    rawViews = []
    for line in lines[1:]:
        trimmedLine = line
        if i != size - 1:
            trimmedLine = line[:-1]  # to avoid the \n symbol in the end of the line
        view = int(trimmedLine)
        rawViews.append(view)
        i = i + 1
    return rawViews


def getFrequencyDictionary(rawViews):
    frequencyDict = {}
    for viewCount in rawViews:
        if viewCount in frequencyDict:
            frequencyDict[viewCount] = frequencyDict[viewCount] + 1
        else:
            frequencyDict[viewCount] = 1
    return frequencyDict


def getCumulativeFrequencyDictionary(rawViews):
    sortedViews = sortWrapper(rawViews)
    cumulativeFrequencyDict = {}
    cumulativeIterator = 0
    for viewCount in sortedViews:
        if viewCount in cumulativeFrequencyDict:
            cumulativeFrequencyDict[viewCount] = cumulativeFrequencyDict[viewCount] + 1
        else:
            cumulativeFrequencyDict[viewCount] = 1 + cumulativeIterator
        cumulativeIterator = cumulativeFrequencyDict[viewCount]
    return cumulativeFrequencyDict


def getMean(rawViews):
    sumOfViews = 0
    for viewCount in rawViews:
        sumOfViews += viewCount
    mean = sumOfViews / len(rawViews)
    return mean


def getVariance(rawViews):
    standartDeviation = getStandartDeviation(rawViews)
    deviation = pow(standartDeviation, 2)
    return deviation


def getStandartDeviation(rawViews):
    mean = getMean(rawViews)
    sumOfDeviations = 0
    for viewCount in rawViews:
        sumOfDeviations += pow((viewCount - mean), 2)
    standartDeviation = pow(sumOfDeviations/len(rawViews), 0.5)
    return standartDeviation


def getMedian(sortedViews):
    size = len(sortedViews)
    if len(sortedViews) % 2 == 0:
        return sortedViews[round(size/2)]
    return sortedViews[math.ceil(size/2)]


def getMode(rawViews):
    freqDict = getFrequencyDictionary(rawViews)
    maxFreq = -100000
    maxKey = 0
    for key in freqDict:
        if(freqDict[key] > maxFreq):
            maxKey = key
            maxFreq = freqDict[key]
    return maxKey


def writeTableToFile(f, dictionary):
    st = ""
    for key in dictionary:
        st += f"\t{key} : {dictionary[key]}\n"
    f.write(st)


def drawWindow(views):
    maxViews = max(views)
    minViews = min(views)
    quantity = len(views)
    c_width = 1000
    if quantity >= 1000:
        c_width = quantity
    c_height = 700

    root = Tk()
    root.title("Bar Graph")
    frame = Frame(root, width=c_width, height=c_height)
    frame.pack(expand=True, fill=BOTH)
    c = Canvas(frame, width=c_width, height=c_height, bg="white", scrollregion=(0, 0, c_width, c_height))
    hbar = Scrollbar(frame, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=c.xview)
    c.config(width=1000, height=c_height)
    c.config(xscrollcommand=hbar.set)
    c.pack(side=LEFT, expand=True, fill=BOTH)
    c.pack()

    y_stretch = 0.6 * c_height / maxViews
    y_gap = 20
    x_stretch = 0
    x_width = 0.9 * c_width / quantity
    x_gap = 60

    minY = 100000
    for x, y in enumerate(views):
        x0 = x * x_stretch + x * x_width + x_gap
        y0 = c_height - (y * y_stretch + y_gap)
        if y0 < minY:
            minY = y0

        x1 = x * x_stretch + x * x_width + x_width + x_gap
        y1 = c_height - y_gap
        c.create_rectangle(x0, y0, x1, y1, fill="red", outline="")
        if quantity <= 100:
            c.create_text(x0 + 2, y0, anchor=SW, text=str(y))

    c.create_line(50, c_height - y_gap, 50, minY - 30, arrow=LAST)
    c.create_text(47, minY, anchor=SE, text=str(maxViews))
    c.create_line(47, minY, 53, minY)
    c.create_text(47, (minY + c_height - y_gap)/2, anchor=SE, text=str(maxViews/2))
    c.create_line(47, (minY + c_height - y_gap)/2, 53, (minY + c_height - y_gap)/2)

    #root.protocol("WM_DELETE_WINDOW", root.destroy())
    root.mainloop()


def getMostVieved(rawViews):
    l = len(rawViews)
    max = -1000000
    maxi = 0
    for i in range(l):
        if rawViews[i] > max:
            maxi = i
            max = rawViews[i]
    return maxi


def run(fileName):
    rawViews = getRawViews(fileName)
    sortedViews = sortWrapper(rawViews)
    mode = getMode(rawViews)
    median = getMedian(sortedViews)
    freq = getFrequencyDictionary(rawViews)
    cumulativeFreq = getCumulativeFrequencyDictionary(rawViews)
    dev = getVariance(rawViews)
    stDev = getStandartDeviation(rawViews)
    mostViewed = getMostVieved(rawViews)
    name = f"resultsOf{time.time()}.txt"
    with open(name, 'w') as f:
        f.write(f"Lab 1 results for {fileName}:\n")
        f.write("Frequency table:\n")
        writeTableToFile(f, freq)
        f.write("Cumulative frequency table:\n")
        writeTableToFile(f, cumulativeFreq)
        f.write(f"Most viewed film: {mostViewed} with {rawViews[mostViewed]} views\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Median: {median}\n")
        f.write(f"Variance: {dev}\n")
        f.write(f"Standart deviation: {stDev}\n")
        f.close()
    drawWindow(rawViews)
    return name


parser = argparse.ArgumentParser()
parser.add_argument('file_path', type=str, nargs='?',
                    help='path to the input file')
args = parser.parse_args()
fileName = args.file_path
if fileName is None:
    fileName = openFileDialog()
print(f"Results were written to the {run(fileName)}")
