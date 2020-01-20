"""
Author: Aditya Chattopadhyay
ADSB Period 3
Semester Project
"""

with open("removeWords.txt", 'r') as words: #opens the text file with words that need to be removed
    wordList = []
    for line in words:
        wordList.append(line.rstrip()) #makes the removed words a list

    for i in range(5): #Goes through all five files
        with open("unCleanedData/" + str(i)+'.txt', 'r') as original:
            with open("cleanedData/"+str(i)+'cleaned.txt', 'w') as removed:
                for line in original:
                    if not(line.split(":")[0] in wordList): #Looks at the line, and if the first value (before the colon) is not in the word list, it adds it to the cleaned file 
                        removed.write(line)
        print("Data for " + str(i) +".txt has been cleaned up.")    
