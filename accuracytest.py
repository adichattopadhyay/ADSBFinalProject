"""
Author: Aditya Chattopadhyay
ADSB Period 3
Semester Project
"""

#modules
from newspaper import Article
import re
import sys
import operator
import os
import pandas as pd

def frequencyAnalysis(rowNum, dictionary, df):
    """frequencyAnalysis takes the row number of the article in the dataset, 
    the dictionary for that article's bias, and the pandas dataframe.
    The function counts the frequency of words in the article given, and adds it
    to the dictionary for that article's bias
    """    
    string = df.iat[rowNum, 4] #Fourth row is the content of the article
    #string = re.sub("[^a-zA-Z0-9’\s]+",'', string) 
    string = re.sub("[^a-zA-Z’\s]+",'', string) #Takes the articles and removes all characters apart from apostrophes, spaces, and leters
    string = re.sub("’", "'", string) #Replaces ’ with '
    string = string.lower() #Ensures that all the charcters are lower case
    stringList = string.split() #Takes the article and turns it into a list
    
    #Started the frequency anaylsis
    for word in stringList:
        if "'s" in word: #Done to remove extra keys in the dictionary, removes the possessive such that it counts "Trump" and "Trump's" as one word
            word = word[0:-2]
        elif "s'" in word:
            word = word[0:-1]
        if word in dictionary:
            dictionary[word] +=1 #If it finds the word in the dictionary, the frequency has to increase by one
        else:
            dictionary[word] = 1 #If it finds a new word, it needs to add the word so the frequency is one

def correctFrequency(bias, dictionary):
    """
    If the user indicates that the prediction of bias is incorrect, correctFrequency will take the words
    in the article and change the frequncy of the words used in the bias file.
    """
    os.rename("cleanedData/"+str(bias)+"cleaned.txt", "cleanedData/"+str(bias)+"needToChange.txt")
    tempDict = {}
    with open("cleanedData/"+str(bias)+"needToChange.txt",'r') as f:
        for line in f:
            freq = line.split(": ")
            tempDict[freq[0]] = int(freq[1].strip())
    for tup in dictionary:
        if tup[0] in tempDict:
            tempDict[tup[0]]+=tup[1]
        else:
            tempDict[tup[0]]=tup[1]
    sortedDict = sorted(tempDict.items(),key=operator.itemgetter(1),reverse=True)
    
    url = "cleanedData/" + str(bias) + 'cleaned.txt'
    with open(url, 'w') as f:
        for word in sortedDict:
            f.write(word[0] + ": " +str(word[1])+"\n")  
    os.remove("cleanedData/"+str(bias)+"needToChange.txt")   

df = pd.read_csv("articles.csv")
df = df.sample(frac=1).reset_index(drop=True)

success = 0
fails = 0
for rowNumber in range(100):
    print(rowNumber)
    articleDict = {} 
    frequencyAnalysis(rowNumber, articleDict, df)
 
    articleDictSortedFirst = sorted(articleDict.items(),key=operator.itemgetter(1),reverse=True) #Sorting the dict, before removing the words
    articleDictSorted = []

    with open("removeWords.txt", 'r') as words: #opens the text file with words that need to be removed
        wordList = []
        for line in words:
            wordList.append(line.rstrip()) #makes the removed words a list
        for word in articleDictSortedFirst:
            if not(word[0] in wordList):
                articleDictSorted.append((word[0],word[1]))

    #Weights for each of the biases
    leftWeight = 0
    leftCentWeight = 0
    neutralWeight = 0
    rightCentWeight = 0
    rightWeight = 0

    #Weights stored in array for easy accessing
    weights = [leftWeight, leftCentWeight, neutralWeight, rightCentWeight, rightWeight]

    #Dictionary with the biases for easy accessing
    biasDict = {0:"Left Bias", 1:"Left Center Bias", 2:"Neutral Bias", 3:"Right Center Bias", 4:"Right Bias"}
    
    firstCounts = []
    maxFirstCount = 0
    for i in range(5):
        with open("cleanedData/"+str(i)+"cleaned.txt", 'r') as data:
            lines = data.read().split("\n")
            firstCounts.append(int(lines[0].split(": ")[1]))
    maxFirstCount = max(firstCounts)
    print("firstCounts: " + str(firstCounts))
    print("Max First Count: " + str(maxFirstCount))
    for i in range(5):
        with open("cleanedData/"+str(i)+"cleaned.txt", 'r') as data:
            lines = data.read().split("\n")
            dataLen = len(lines)
            weight = [j/dataLen for j in range(dataLen, 0, -1)] #Creates and array that has a weight for all of the words in whichever bias text file
            for word in articleDictSorted:
                for k,line in enumerate(lines):
                    if word[0] in line and line != "":
                        weights[i]+=(weight[k-1]*int(line.split(": ")[1])/maxFirstCount)#Looks through the article and looks through each bias document, if it finds it add it to the weight                                                    
            weights[i] = weights[i]/dataLen
    if((weights.index(max(weights)))+1==df.iat[rowNumber,3]):
        success+=1
        print("This was a sucess.")
    else:
        fails+=1
        print("This was a fail")
        correctFrequency(df.iat[rowNumber,3]-1, articleDictSorted)
    print("Guess: " + str((weights.index(max(weights)))+1))
    print("Actual: " + str(df.iat[rowNumber,3]))
    print("Weights: " + str(weights))
print(success)
print(fails)
print(success/(fails+success)*100)