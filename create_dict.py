"""
Author: Aditya Chattopadhyay
ADSB Period 3
Semester Project
"""

#modules
import pandas as pd
import re
import operator
import numpy

def frequencyAnalysis(rowNum, dictionary, df):
    """frequencyAnalysis takes the row number of the article in the dataset, 
    the dictionary for that article's bias, and the pandas dataframe.
    The function counts the frequency of words in the article given, and adds it
    to the dictionary for that article's bias
    """
    print("Accessing article", rowNum+1)
    
    string = df.iat[rowNum, 4] #Fourth row is the content of the article
    #string = re.sub("[^a-zA-Z0-9’\s]+",'', string) 
    string = re.sub("[^a-zA-Z’\s]+",'', string) #Takes the articles and removes all characters apart from apostrophes, spaces, and leters
    string = re.sub("’", "'", string) #Replaces ’ with '
    string = string.lower() #Ensures that all the charcters are lower case
    stringList = string.split() #Takes the article and turns it into a list
    
    print("\nConverted article to list\n")
        
    print("Starting frequency analysis\n")

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
    
print("\nLoading the Articles\n")
df = pd.read_csv("articles.csv")
print(df.columns+"\n")

#Creates the dictionaries
leftDict = {}
leftCentDict = {}
neutralDict = {}
rightCentDict = {}
rightDict = {}

#Creates an array of the dictionaries for easier access later on
dictArray = [leftDict, leftCentDict, neutralDict, rightCentDict, rightDict]

#Does the frequency analysis for every article
for rowNum in range(len(df.index)):
    frequencyAnalysis(rowNum, dictArray[df.iat[rowNum, 3]-1],df)

print("\nAll Done!\n")

#Sorts all the dicts in descending order of frequency, and turns them into an array of tuples
leftDictSorted = sorted(leftDict.items(),key=operator.itemgetter(1),reverse=True)
leftCentDictSorted = sorted(leftCentDict.items(),key=operator.itemgetter(1),reverse=True)
neutralDictSorted = sorted(neutralDict.items(),key=operator.itemgetter(1),reverse=True)
rightCentDictSorted = sorted(rightCentDict.items(),key=operator.itemgetter(1),reverse=True)
rightDictSorted = sorted(rightDict.items(),key=operator.itemgetter(1),reverse=True)

#Stores the arrays into an array for easier use
dictArraySort = [leftDictSorted, leftCentDictSorted, neutralDictSorted, rightCentDictSorted, rightDictSorted]

#Count for creating the url for each bias dict
num = 0
#Saves each dictionary into a seperate file
for i in range(len(dictArraySort)):
    url = "unCleanedData/" + str(num) + '.txt'
    with open(url, 'w') as f:
        for word in dictArraySort[i]:
            f.write(word[0] + ": " +str(word[1])+"\n") #Writes each tuple on a new line with the format 'word: frequency'
    print(url)
    num+=1
print("NOW ALL DONE")
