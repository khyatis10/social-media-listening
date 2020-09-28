from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import LinearSVC
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

df1 = pd.read_csv('D:/Social Media Listening/test_csvs/xuv300reviews.csv')
df1a = df1[['reviews','ratings']]

analyser = SentimentIntensityAnalyzer()
def calculate_sentiment(Clean_text):
    return TextBlob(Clean_text).sentiment

def calculate_sentiment_analyser(Clean_text):
    return analyser.polarity_scores(Clean_text)



df1a['sentiment']=df1a.reviews.apply(calculate_sentiment)
df1a['sentiment_analyser']=df1a.reviews.apply(calculate_sentiment_analyser)
#EXTRACTING SENTIMENT LABELS
s = pd.DataFrame(index = range(0,len(df1a)),columns= ['compound_score','compound_score_sentiment'])

for i in range(0,len(df1a)):
  s['compound_score'][i] = df1a['sentiment_analyser'][i]['compound']

  if (df1a['sentiment_analyser'][i]['compound'] <= -0.05):
    s['compound_score_sentiment'][i] = 'Negative'
  if (df1a['sentiment_analyser'][i]['compound'] >= 0.05):
    s['compound_score_sentiment'][i] = 'Positive'
  if ((df1a['sentiment_analyser'][i]['compound'] >= -0.05) & (df1a['sentiment_analyser'][i]['compound'] <= 0.05)):
    s['compound_score_sentiment'][i] = 'Neutral'

df1a['compound_score'] = s['compound_score']
df1a['compound_score_sentiment'] = s['compound_score_sentiment']
features = df1a.iloc[:, 0].values
labels = df1a.iloc[:, 5].values

#CLEANING DATA
processed_features = []

for sentence in range(0, len(features)):
    # Remove all the special characters
    processed_feature = re.sub(r'\W', ' ', str(features[sentence]))

    # remove all single characters
    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

    # Remove single characters from the start
    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature)

    # Substituting multiple spaces with single space
    processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

    # Removing prefixed 'b'
    processed_feature = re.sub(r'^b\s+', '', processed_feature)

    # Converting to Lowercase
    processed_feature = processed_feature.lower()

    processed_features.append(processed_feature)

vectorizer = TfidfVectorizer (max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
processed_features = vectorizer.fit_transform(processed_features).toarray()

X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.2, random_state=0)

#RANDOMFOREST
text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
text_classifier.fit(X_train, y_train)
predictions = text_classifier.predict(X_test)

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))

print('Accuracy Score: ',metrics.accuracy_score(y_test,predictions)*100,'%',sep='')
#SVM
SVM = LinearSVC(multi_class='ovr')
SVM.fit(X_train, y_train)
y_pred = SVM.predict(X_test)
print('\nSupport Vector Machine')
print('Accuracy Score: ',metrics.accuracy_score(y_test,y_pred)*100,'%',sep='')
print('Confusion Matrix: ',metrics.confusion_matrix(y_test,y_pred), sep = '\n')


