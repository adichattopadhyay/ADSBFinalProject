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

def frequencyAnalysis(article, dictionary):
    """frequencyAnalysis in main.py is similar to the frequencyAnalysis
    in create_dict.py, however all it requires is the article and the dictionary
    The function counts the frequency of words in the article given, and adds it
    to the dictionary for that article's bias
    """
    string = article #Sets the string to the article
    string = re.sub("[^a-zA-Z0-9’\s]+",'', string) #Takes the articles and removes all characters appart from apostrophes, spaces, digits, and leters
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
        if word != "advertisement":
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

print("Welcome!\n")
url = str(input("Please enter a news source url that you would like me to check: ")).rstrip()

article = Article(url, language='en') #Uses the newspaper module to scrape the article
try:  
    article.download()
    article.parse()
except:
    print("Something went wrong with the article that was entered.") #In case the article doesn't exist or there is some other error
    sys.exit()
    
articleDict = {} #The first dictionary for the frequency

frequencyAnalysis(article.text, articleDict)
 
articleDictSortedFirst = sorted(articleDict.items(),key=operator.itemgetter(1),reverse=True) #Sorting the dict, before removing the words
articleDictSorted = []

with open("removeWords.txt", 'r') as words: #opens the text file with words that need to be removed
    wordList = []
    for line in words:
        wordList.append(line.rstrip()) #makes the removed words a list
    for word in articleDictSortedFirst:
        if not(word[0] in wordList):
            articleDictSorted.append((word[0],word[1]))


print("Starting comparison with other data")

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

for i in range(5):
    with open("cleanedData/"+str(i)+"cleaned.txt", 'r') as data:
        lines = data.read().split("\n")
        dataLen = len(lines)
        print("\nLoading")
        weight = [j/dataLen for j in range(dataLen, 0, -1)] #Creates and array that has a weight for all of the words in whichever bias text file
        for word in articleDictSorted:
            for k,line in enumerate(lines): 
                if word[0] in line:
                    weights[i]+=(weight[k-1]*int(line.split(": ")[1]))#Looks through the article and looks through each bias document, if it finds it add it to the weight
        weights[i] = weights[i]/dataLen
print(weights)
print("Left Bias                 Right Bias")
arrow = "<---------------------------------->"
print(arrow)
print(" "*(weights.index(max(weights)))*int(len(arrow)/4)+'|')

print("\nThe article \"" + article.title + "\" has a " + biasDict[weights.index(max(weights))]+ ".")

correct = str(input("Is this correct?(y or n): ")).lower()
if(correct=='y'):
    print("Cool.")
elif(correct=='n'):
    print("Oh no, I was wrong.")
    try:
        biasCorrect = int(input("What was the bias of the article? (0-4, 0: Left Bias, 1: Left Center Bias, 2: Neutral Bias, 3: Right Center Bias, 4: Right Bias): "))
    except:
        print("Incorrect input, you have to enter a number from 0-4")
        sys.exit()
    correctFrequency(biasCorrect, articleDictSorted)
    
else:
    print("Incorrect input, you need to enter y or n")
input("Hit enter to exit")