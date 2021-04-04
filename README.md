# Simple-natural-language-processing
Assignment 1

## Dataset that is going to be used in general 

1.  Data Science is a field that uses various tools, processes, algorithms and machine learning principles to obtain knowledge and insights patterns from data.  
3.  Streaming Services is a subscription-based service that offers online streaming of movies and television programs 
3.  History of Singapore 

## Tokenization and Stemming
The library we used to perform tokenization and stemming is word_tokenize and PorterStemmer respectively from NLTK.  

### Tokenization 
In the tokenization process, we will perform tokenization for all the text in our dataset. Tokenization are important as text needs to be split into smaller units such as words, punctuation, numbers before any processing can be done. The table below shows the incorrect token for domain specific word.
Domain        | Unexpected Tokens  | Expected Tokens  | 
--------------| ---- | ---- |
Data Science  | ' (' 'k−1' ') ' '×'  ' (' 'k−2'   ') '  | ' (k−1) ' '×' ' (k−2) '  |
Streaming Services   | 'Acorn' 'TV'  / 'Amazon' 'Video'   | 'Acorn TV' - is an American subscription video streaming service  <br>'Amazon Video' - is an American Internet video owned by Amazon   |
History of Singapore   | 'M' 'Veerasamy'  / 'Bak' 'Kut' 'Teh'   | 'M Veerasamy'  <br> 'Bak Kut Teh'   |

### How to identify incorrect tokens
To identify the tokens that are incorrect, we can use the following methods: 

1.  Check Isupper() for the next tokens. If is a noun, the first character of the tokens is in upper character.  
2.  Check for special character, for example ‘$’,  

### Improving the tokenizer 
To improve the tokenizer, following are the possible solutions we could implement: 

1.  Regular-Expression - In order to correctly identify tokens like ‘$’, ‘0.50’, we can use regular expression e.g “\$[\d\.]+”.
2.  Multi-Word Expression Tokenizer (MWETokenizer) - It will take existing tokens and retokenizes them as a single token. We can add phrase like “'Bak' 'Kut' 'Teh' to MWETokenizer which will retokenizes it as a single token. Similar can be done with a person name. 
3.  S-Expression Tokenizer – we can use SExprTokenizer to look for parenthesized expressions in a string and tokenizes as a single token. 


### Stemming
Stemming will reduce the word to their root form. This suggest that by performing stemming the length of the token will be reduced as the root form of word has lesser number of characters. 

### Sentence Segmentation 
The library we used for to perform sentence segmentation will be sent_tokenize from NLTK.

### POS Tagging
In this experiment we will randomly select 3 sentences from each topical domain. From the result in appendix Table 8, we can see that most of the word is tagged correctly. However, it was observed that certain domain specific terms such as mathematical formulas and programming language in data science domain was tagged wrongly. An example sentence from the result set is “The probability of an event is always between 0 and 1, 0≤P(A)≤1”. The tagger tags the mathematical term '0≤P' as NUM, 'A' as DET and '≤1' as NOUN. This shows that the tagger is unable to handle such domain specific terms. The reason for this is because the tagger uses pre-trained model for generic English sentences only.  

We can improve the tagging result by performing a regex tagging for the domain specific terms such as mathematical formulas and programming language. Then fallback on our regular pos tagger for the tokens which have not been identified.








