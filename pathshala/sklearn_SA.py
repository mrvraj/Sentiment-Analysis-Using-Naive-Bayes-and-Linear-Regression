from sklearn import datasets
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import random
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,accuracy_score

data = []
data_labels = []
with open("./pos.txt") as f:
    for i in f: 
        data.append(i) 
        data_labels.append(i[-2])
vectorizer = CountVectorizer(
    analyzer = 'word',
    lowercase = False,
)
features = vectorizer.fit_transform(
    data
)
features_nd = features.toarray() # for easy usage



class Sentiment():
    def _SA(self,model='Naive bayes',train_size=0.80):

        X_train, X_test, y_train, y_test  = train_test_split(
        features_nd, 
        data_labels,
        train_size=train_size,
        test_size=1-train_size-0.02,
        random_state=1234)

        if model=='Naive bayes':
            log_model=GaussianNB()
        else :
            log_model =LogisticRegression()
        log_model = log_model.fit(X=X_train, y=y_train)

        y_pred = log_model.predict(X_test)

        # j = random.randint(0,len(X_test)-7)
        # for i in range(j,j+7):
        #     print(y_pred[i])
        #     ind = features_nd.tolist().index(X_test[i].tolist())
        #     print(data[ind].strip())

        print( accuracy_score(y_test, y_pred),'Clasification report:',classification_report(y_test, y_pred) ,'Confussion matrix:',confusion_matrix(y_test, y_pred))
        return (classification_report(y_test, y_pred),accuracy_score(y_test, y_pred),confusion_matrix(y_test, y_pred))  



# SA=Sentiment()
# SA._SA()
