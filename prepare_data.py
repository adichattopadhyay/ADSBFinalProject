"""
Author: Aditya Chattopadhyay
ADSB Period 3
Semester Project
"""
#Important to note that bias from 1-5 Goes as 'Left Bias', 'Left-Center Bias', 'Neutral', 'Right Center', 'Right Bias'
#modules
import pandas as pd

#Loads all the articles and ensures that they are working properly
print("Loading the Articles")
df1 = pd.read_csv("articles1.csv")
print(df1.columns)
print(set(df1.publication))
df2 = pd.read_csv("articles2.csv")
print(df2.columns)
print(set(df2.publication))
df3 = pd.read_csv("articles3.csv")
print(df3.columns)
print(set(df3.publication))

#loads the biases
print("Loading the biases")
biases_df = pd.read_csv("biases.csv")
biases_df.set_index(biases_df['News Company'], inplace=True)
print(biases_df)

#Creates and opens 'articles.csv' where all the articles and biases will be stored
with open('articles.csv', 'w+', encoding="utf-8") as f:
    df = pd.DataFrame()
    #Creates a list with all the publishers from the first set of articles to the last
    publishers = df1.publication.values.tolist()
    publishers.extend(df2.publication.values.tolist())
    publishers.extend(df3.publication.values.tolist())
    
    #Creates a list with all the titles from the first set of articles to the last
    title = df1.title.values.tolist()
    title.extend(df2.title.values.tolist())
    title.extend(df3.title.values.tolist())
    
    #Creates a list with all the biases by looping through the publishers and finding the bias value in 'biases.csv'
    biases = [biases_df.loc[i].at['Bias'] for i in publishers]
    
    #Creates a list with all the content from the first set of articles to the last
    content = df1.content.values.tolist()
    content.extend(df2.content.values.tolist())
    content.extend(df3.content.values.tolist())
    
    #Inserts all the columns into the dataframe
    df.insert(0,column='publication', value=publishers)
    df.insert(1,column='title', value=title)
    df.insert(2,column='biases', value=biases)
    df.insert(3,column='content', value=content)
    df.to_csv(f, encoding='utf-8')
print("Data is ready!")