#https://www.nationalgeographic.com/environment/global-warming/global-warming-effects/7
import sys
from bs4 import BeautifulSoup
import nltk
#nltk.download()
import nltk
from nltk.book import *
from nltk.tokenize import word_tokenize 
from nltk.stem import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
import random
from urllib.request import Request, urlopen
import re


## Read all Link
TopicDomain = ["Data Science", "Streaming Services","History of Singapore"]
pd.set_option('display.max_colwidth', None)
data = pd.read_excel("domainDocument.xlsx")
dataDict = {}
dataDict["Data Science"] = ''
dataDict["Streaming Services"] = ''
dataDict["History of Singapore"] = ''

dataDictPD = {}
dataDictPD["Data Science"] = ''
dataDictPD["Streaming Services"] = ''
dataDictPD["History of Singapore"] = ''

for tpd in TopicDomain:
    i = 0
    for url in data[tpd]:
        text = ''
        print(str(i) + ". "+url)
        req = Request(url,headers = {"User-Agent": "Mozilla/5.0"})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, features="html.parser")
        if (tpd=='Data Science'):
            para = soup.find_all('pre')
            for p in para:
                text = p.getText()
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                dataDict[tpd] = dataDict[tpd] + ' ' + text.replace('\n', '. ')
        for script in soup.find_all('span'):
            script.extract()
        para = soup.find_all('p')
        for p in para:
            s = p.getText()
            slices = []
            for match in re.finditer('\w\.\w', s):
                slices.append(match.start()+2)
            slices.append(len(s))
            offset = 0
            subsentences = ""
            for pos in sorted(slices):
                subsent = s[offset:pos]
                offset += len(subsent)
                subsentences = subsentences + " "+ subsent
            #print(subsentences)
            text = text +' ' + subsentences
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        dataDict[tpd] = dataDict[tpd] + ' ' + text
        
        i = i+1
        if i ==20 :
            break




# soup = BeautifulSoup(html, features="html.parser")

# para = soup.find_all('p')
# for p in para:
#     text = text +' ' + p.getText()
#     # if(text[len(text)-1]) != '.':
#     #     a = text[len(text)-1]
#     #     print(text)
#     #     print(a)



# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)
# print(text)

for tpd in TopicDomain:
    # token
    tokens = nltk.word_tokenize(dataDict[tpd])
    tokensArr = np.array(tokens)
    ## remove long link / may not need it
    index = []
    k = 0
    for t in tokensArr:
        if(len(t)>25):
            index.append(k)
            print(t,k)
        k = k +1
    tokensArr = np.delete(tokensArr, index)

    # stem
    stemmer = PorterStemmer()
    stem =[stemmer.stem(token) for token in tokensArr]
    stemsArr = np.array(stem)
        
    x = ['Before Stemming', "After Stemming"]
    y = [len(np.unique(tokensArr)),len(np.unique(stemsArr))]
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(x,y)
    plt.title("Number of Distinct Tokens - "+tpd)
    plt.show()

    token_df = pd.DataFrame(data=tokensArr, columns=["Word"])
    token_df['Number of Character'] = token_df.apply(lambda row: len(row.Word), axis = 1) 
    token_df = token_df.groupby(['Number of Character']).size().reset_index(name='Before Stemming')
    
    stem_df = pd.DataFrame(data=stemsArr, columns=["Word"])
    stem_df['Number of Character'] = stem_df.apply(lambda row: len(row.Word), axis = 1) 
    stem_df = stem_df.groupby(['Number of Character']).size().reset_index(name='After Stemming')
    
    df_merge_col = pd.merge(token_df, stem_df, on='Number of Character' , how='outer')
    df_merge_col['Before Stemming'] = df_merge_col['Before Stemming'].fillna(0.0).astype(int)
    df_merge_col['After Stemming'] = df_merge_col['After Stemming'].fillna(0.0).astype(int)
    df_merge_col.plot(x="Number of Character", y=["Before Stemming", "After Stemming" ], kind="bar")
    plt.title("Length Distribution of Tokens - " + tpd)
    plt.ylabel("Number of Tokens of each Length")
    dataDictPD[tpd]=y

df_data = pd.DataFrame.from_dict(dataDictPD,orient='index')
#df_data = df_data.rename(index={0: 'Before Stemming', 1: 'After Stemming'})
df_data = df_data.rename(columns={0: "Before Stemming", 1: "After Stemming"})
df_data.plot(kind="bar",rot=0,title="Number Of Distinct Tokens",ylabel='Number Of Token' ,xlabel='Topical Domain'  )
print(df_data)

sentancesArr1 = sent_tokenize(dataDict["Data Science"] )
sentancesArr2 = sent_tokenize(dataDict["Streaming Services"] )
sentancesArr3 = sent_tokenize(dataDict["History of Singapore"]  )

sentances_df1 = pd.DataFrame(data=sentancesArr1, columns=["Sentences"])
sentances_df2 = pd.DataFrame(data=sentancesArr2, columns=["Sentences"])
sentances_df3 = pd.DataFrame(data=sentancesArr3, columns=["Sentences"])

sentances_df1['Number of Word'] = sentances_df1.apply(lambda row: len(nltk.word_tokenize((row.Sentences))) , axis = 1) 
sentances_df2['Number of Word'] = sentances_df2.apply(lambda row: len(nltk.word_tokenize((row.Sentences))) , axis = 1) 
sentances_df3['Number of Word'] = sentances_df3.apply(lambda row: len(nltk.word_tokenize((row.Sentences))) , axis = 1) 

sentances_df1 = sentances_df1.groupby(['Number of Word']).size().reset_index(name='Data Science')
sentances_df2 = sentances_df2.groupby(['Number of Word']).size().reset_index(name='Streaming Services')
sentances_df3 = sentances_df3.groupby(['Number of Word']).size().reset_index(name='History of Singapore')

sentances_df1 = sentances_df1[sentances_df1['Number of Word'] < 200]
sentances_df2 = sentances_df2[sentances_df2['Number of Word'] < 100]


ax = sentances_df1.plot(x="Number of Word" , y=["Data Science" ], kind="line") 
sentances_df2.plot(x="Number of Word" , y=["Streaming Services" ], kind="line",ax=ax) 
sentances_df3.plot(x="Number of Word" , y=["History of Singapore" ], kind="line",ax=ax) 
plt.ylabel('Frequency')
plt.title("Distribution Of The Sentence Length")



for tpd in TopicDomain:
    ar = sent_tokenize(dataDict[tpd])
    print(tpd)
    for i in range(3):
        ranSen = random.choice(ar)
        print(ranSen)
        print(nltk.pos_tag(word_tokenize(ranSen),tagset='universal'))


ar = sent_tokenize(dataDict['Streaming Services'])
for i in ar:
    if len(word_tokenize(i)) <10:
        print(i)



ar = sent_tokenize('The top three streaming video services in July were Netflix, Alphabet\'s (GOOGL) YouTube and Amazon (AMZN) Prime Video, according to ComScore data.')
print(ar)
print(nltk.pos_tag(word_tokenize(ar[0])))




# dataDict = {}

# dataDict['tpd'] = ""

url = 'https://switchboard.live/blog/live-streaming-glossary-terms-definitions-in-plain-english'
tpd='stream'
dataDict['tpd'] = ""
text = ''
req = Request(url,headers = {"User-Agent": "Mozilla/5.0"})
html = urlopen(req).read()
soup = BeautifulSoup(html, features="html.parser")
if (tpd=='Data Science'):
    para = soup.find_all('pre')
    for p in para:
        text = p.getText()
        
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        print(text.replace('\n', '. '))
        dataDict['tpd'] = dataDict['tpd'] + ' ' + text.replace('\n', '. ')
  
for script in soup.find_all('span'):
    script.extract()
para = soup.find_all('p')
for p in para:
    s = p.getText()
    slices = []
    for match in re.finditer('\w\.\w', s):
        slices.append(match.start()+2)
    slices.append(len(s))
    offset = 0
    subsentences = ""
    for pos in sorted(slices):
        subsent = s[offset:pos]
        offset += len(subsent)
        subsentences = subsentences + " "+ subsent
    #print(subsentences)
    text = text +' ' + subsentences
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
dataDict['tpd'] = dataDict['tpd'] + ' ' + text

        
print(dataDict['tpd'])
ar = sent_tokenize(dataDict['tpd'])
for i in ar:
    print(i)
    print(nltk.pos_tag(word_tokenize(i),tagset='universal')) 
        
        
# print(tpd)
        
        
        