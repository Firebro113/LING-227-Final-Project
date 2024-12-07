import re
import os
import sys
import random
from unidecode import unidecode

lengths = []

def processFile(filename, dataType, trainingFile, validationFile, testFile):
    input1 = open("data_raw/" + dataType + "/" + filename, 'r', encoding='utf-8')
    clean = []
    index = 0

    for x, line in enumerate(input1):

        # Removes all characters not part of the Greek alphabet, converts into Latin alphabet, removes all characters except alphabet and spaces

        line = re.sub(r'[A-Za-z]+', '', line)
        
        line = unidecode(line)
        line = line.strip()
        line = line.replace('-', ' ')
        line = re.sub(r'[^A-Za-z ]+', '', line)
        line = re.sub(' +', ' ', line)

        words = line.split()

        # Removes words in all caps (because there are labels in the dataset)
        
        for word in words:
            if len(word) > 1 and word[1].isupper():
                continue
            if len(word) > 2 and word[2].isupper():
                continue
            
            word = word.lower()

            forbidden = []
            if word in forbidden:
                continue

            clean += [word]

    input1.close()

    # Get documents based on predetermined size and split them into training, validation, and test sets (80%, 10%, 10% respectively)

    trainingSet = open(trainingFile, 'a', encoding='utf-8')
    validationSet = open(validationFile, 'a', encoding='utf-8')
    testSet = open(testFile, 'a', encoding='utf-8')

    for index in range(len(clean)):
        if (index + 1) * documentSize >= len(clean):
            break
        value = -1
        if dataType == "plato":
            value = 1
        elif dataType == "notplato":
            value = 0
        document = str(value) + ' ' + filename[:-4].replace(' ', '') + ' ' + ' '.join(clean[index*documentSize:(index+1)*documentSize])

        firstDigit = index % 10
        if firstDigit <= 7:
            trainingSet.write(document + '\n')
        elif firstDigit <= 8:
            validationSet.write(document + '\n')
        else:
            testSet.write(document + '\n')
    
    trainingSet.close()
    validationSet.close()
    testSet.close()

    return len(clean)


def clean(dataTypes, folderName, documentSize, split):

    parentPath = "data_" + str(documentSize)
    currentPath = parentPath + "/" + folderName

    if split:
        trainingFile = currentPath + "/training.txt"
        validationFile = currentPath + "/validation.txt"
        testFile = currentPath + "/test.txt"
    else:
        trainingFile = currentPath + "/main.txt"
        validationFile = trainingFile
        testFile = trainingFile

    # Create appropriate directories

    if not os.path.exists(parentPath):
        os.mkdir(parentPath)
    if not os.path.exists(currentPath):
        os.mkdir(currentPath)
    
    # Wipe each file

    open(trainingFile, 'w').close()
    open(validationFile, 'w').close()
    open(testFile, 'w').close()

    # Run the dataset creator for each file in each folder

    lengths = []

    for dataType in dataTypes:

        for filename in os.listdir("data_raw/" + dataType):
            f = os.path.join("data_raw/" + dataType, filename)
            if os.path.isfile(f):
                lengths += [processFile(filename, dataType, trainingFile, validationFile, testFile)]
                print(lengths[-1], filename)
    
    with open(trainingFile, 'r') as trainingSet, open(validationFile, 'r') as validationSet, open(testFile, 'r') as testSet:
        trainingLength = len(trainingSet.readlines())

        if split:
            validationLength = len(validationSet.readlines())
            testLength = len(testSet.readlines())
            totalLength = trainingLength+validationLength+testLength
            if totalLength == 0:
                totalLength = 1
            print(trainingLength, trainingLength/totalLength, validationLength, validationLength/totalLength, testLength, testLength/totalLength, trainingLength+validationLength+testLength, "documents")
        
        else:
            print(trainingLength, "documents")

    if len(lengths) != len(set(lengths)):
        print("ERROR")


if __name__ == "__main__":

    print("What is the document size?")
    documentSize = int(input())

    # Run main function
    
    clean(["plato", "notplato"], "main", documentSize, True)
    clean(["dubia"], "dubia", documentSize, False)