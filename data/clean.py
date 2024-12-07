import re
import os
import math
import sys
import random
from unidecode import unidecode

lengths = []

def processFile(filename, dataType, outputFile1, outputFile2, outputFile3):
    input1 = open("data_raw/" + dataType + "/" + filename, 'r', encoding='utf-8')
    clean = []

    for line in input1:

        # Removes all characters not part of the Greek alphabet, converts into Latin alphabet, removes all characters except alphabet and spaces

        line = re.sub(r'[A-Za-z]+', '', line)
        
        # Diacritics including aspirations are lost
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

    value = -1
    if dataType == "plato":
        value = 1
    elif dataType == "notplato":
        value = 0
    filenameNew = filename[:-4].replace(' ', '')
    proem = str(value) + ' ' + filenameNew + ' '

    document1 = ""
    document2 = ""
    document3 = ""

    output1 = open(outputFile1, 'a', encoding='utf-8')
    if outputFile2 == "":
        document1 = proem + ' '.join(clean)
        output1.write(document1 + '\n')
    elif filenameNew == "Ion" or filenameNew == "Xenocrates":
        output2 = open(outputFile2, 'a', encoding='utf-8')
        document2 = proem + ' '.join(clean)
        output2.write(document2 + '\n')
        output2.close()
    elif filenameNew == "Crito" or filenameNew == "IsocratesHelen":
        output3 = open(outputFile3, 'a', encoding='utf-8')
        document3 = proem + ' '.join(clean)
        output3.write(document3 + '\n')
        output3.close()
    else:
        validationIndex = 0
        testIndex = 0
        while validationIndex == testIndex:
            validationIndex = random.randint(0, 9)
            testIndex = random.randint(0, 9)

        output2 = open(outputFile2, 'a', encoding='utf-8')
        output3 = open(outputFile3, 'a', encoding='utf-8')

        document1 = ' '.join(clean[: math.floor(0.8*len(clean))])
        document2 = ' '.join(clean[math.floor(0.8*len(clean)): math.floor(0.9*len(clean))])
        document3 = ' '.join(clean[math.floor(0.9*len(clean)): ])

        document1 = proem + document1
        document2 = proem + document2
        document3 = proem + document3

        output1.write(document1 + '\n')
        output2.write(document2 + '\n')
        output3.write(document3 + '\n')

        output2.close()
        output3.close()
    output1.close()

    print(len(document1.split()), len(document2.split()), len(document3.split()))
    return len(clean)

def clean(dataType, split):
    lengths = []

    parentPath = "data_clean"

    trainingFile = parentPath + "/training.txt"
    validationFile = parentPath + "/validation.txt"
    testFile = parentPath + "/test.txt"
    dubiaFile = parentPath + "/dubia.txt"

    for filename in os.listdir("data_raw/" + dataType):
        f = os.path.join("data_raw/" + dataType, filename)
        if not os.path.isfile(f):
            continue
        
        if split:
            lengths += [processFile(filename, dataType, trainingFile, validationFile, testFile)]
        else:
            lengths += [processFile(filename, dataType, dubiaFile, "", "")]
        
        print(lengths[-1], filename)
    
    print(dataType, sum(lengths), '\n')

if __name__ == "__main__":

    parentPath = "data_clean"

    trainingFile = parentPath + "/training.txt"
    validationFile = parentPath + "/validation.txt"
    testFile = parentPath + "/test.txt"
    dubiaFile = parentPath + "/dubia.txt"

    # Create appropriate directories

    if not os.path.exists(parentPath):
        os.mkdir(parentPath)
    
    open(trainingFile, 'w').close()
    open(validationFile, 'w').close()
    open(testFile, 'w').close()
    open(dubiaFile, 'w').close()

    # Run main function
    
    clean("plato", True)
    clean("notplato", True)
    clean("dubia", False)

    trainingSize = os.path.getsize(trainingFile)
    validationSize = os.path.getsize(validationFile)
    testSize = os.path.getsize(testFile)
    sumSize = trainingSize+validationSize+testSize
    dubiaSize = os.path.getsize(dubiaFile)

    print(trainingSize/sumSize, validationSize/sumSize, testSize/sumSize, sumSize)
    print(dubiaSize)
