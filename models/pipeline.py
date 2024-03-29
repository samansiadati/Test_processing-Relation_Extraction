# -*- coding: utf-8 -*-
"""Pipe.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d_4XQl9g-SUIP50HROZSCJ631iwo8Hla
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import seaborn as sns
import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix

from google.colab import drive
drive.mount('/content/gdrive')

address = '/content/gdrive/My Drive/codes/_data/'

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_colwidth', None)
pd.options.display.float_format = '{:,.0f}'.format



train = pd.read_csv(address + '/oscer/REdata/train.tsv', sep='\t', names=['sentence' , 'label'])



train.head()



train.isnull().sum()



X = train.sentence
y = train.label



Fhw1 = open('SpacyDispaly.sam_re.svd','w', encoding="utf8")
Fhw2 = open('ModelReport.sam_re.svd','w', encoding="utf8")


y.value_counts()





sentence_len = list(map(len,X))

len(sentence_len)

min(sentence_len)

max(sentence_len)





ax = sns.boxplot(sentence_len)







nlp = spacy.load('en_core_web_sm')



sentence = X[0]

doc = nlp(sentence)

print ("{:<15} | {:<8} | {:<15} | {:<20}".format('Token','Relation','Head', 'Children'))
print ("-" * 70)

for token in doc:
  # Print the token, dependency nature, head and all dependents of the token
  msg1 =  str ("{:<15} | {:<8} | {:<15} | {:<20}"
         .format(str(token.text), str(token.dep_), str(token.head.text), str([child for child in token.children])))
  
# Use displayCy to visualize the dependency 
msg2 = (displacy.render(doc, style='dep', jupyter=True, options={'distance': 120}))
Fhw1.write(msg1)




sent = nlp.create_pipe('sentencizer')

nlp.add_pipe(sent, before='parser')



stopwords = list(STOP_WORDS)

print(stopwords)

len(stopwords)





"""### Tokenization"""



punct = string.punctuation
punct

def text_data_cleaning(sentence):
    doc = nlp(sentence)
    
    tokens = []
    for token in doc:
        if token.lemma_ != "-PRON-":
            temp = token.lemma_.lower().strip()
        else:
            temp = token.lower_
        tokens.append(temp)
    
    cleaned_tokens = []
    for token in tokens:
        if token not in stopwords and token not in punct:
            cleaned_tokens.append(token)
    return cleaned_tokens



text_data_cleaning("    My name is Saman. I'm a data scientist.")



"""### Vectorization Feature Engineering (TF-IDF)"""



tfidf = TfidfVectorizer(tokenizer = text_data_cleaning, lowercase=True)
tfidf





X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

X_train.shape, X_test.shape

classifier = LinearSVC()
clf = Pipeline([('tfidf', tfidf), ('clf', classifier)])

clf.fit(X_train, y_train)

clf



y_pred = clf.predict(X_test)


msg3 = str('The classification report is : '+ (classification_report(y_test, y_pred)))
Fhw2.write(msg3)


msg4 = str(confusion_matrix(y_test, y_pred))
Fhw2.write(msg3)

Fhw1.close()
Fhw2.close()


