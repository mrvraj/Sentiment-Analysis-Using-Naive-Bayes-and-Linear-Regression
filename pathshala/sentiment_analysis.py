import json as j
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,accuracy_score
from pathshala.models import User, Post,Playlist,Comments,Videos,Contacts
from pathshala import app, db, bcrypt
from sqlalchemy.sql import func
import math
from sklearn.externals import joblib
# --- read and transform json file
json_data = None
with open('yelp_academic_dataset_review.json') as data_file:
    lines = data_file.readlines()
    joined_lines = "[" + ",".join(lines[5000:10000]) + "]"

    json_data = j.loads(joined_lines)

data = pd.DataFrame(json_data)


# --- prepare the data

data = data[data.stars != 3]
data['sentiment'] = data['stars'] >= 4
# print(data.head())

# --- build the model
class Sentiment():
    def _SA(self,comments,model='Naive bayes',train_size=0.80):
            X_train, X_test, y_train, y_test = train_test_split(data, data.sentiment, test_size=0.2)
            count = CountVectorizer()
            temp = count.fit_transform(X_train.text)
            tdif = TfidfTransformer()
            temp2 = tdif.fit_transform(temp)
            if model=='Naive bayes':
               text_regression=GaussianNB()
            else :
                text_regression=LogisticRegression()
            model = text_regression.fit(temp2.toarray(), y_train)
            # print(text_regression)
            comments_DT=Comments.query.filter_by()
            for comment in comments_DT:
                comment.sentiment=str(model.predict(tdif.transform(count.transform([comment.comment])).toarray())).replace('[','').replace(']','').strip()
                
            db.session.commit()
            # result = db.engine.execute("select p.sno,c.sentiment,count(c.sentiment) as count from playlist p, videos v ,comments c where p.sno=v.sno and v.ID=c.id group by p.sno,c.sentiment having c.sentiment='True' order by p.sno")
            Total_result = (db.session.query(Playlist.sno,db.func.count(Comments.sentiment))
                .filter(Playlist.sno==Videos.sno)
                .filter(Videos.ID==Comments.ID)
                .group_by(Playlist.sno)
                .order_by(Playlist.sno)
                ).all()
            result = (db.session.query(Playlist.sno,Comments.sentiment,db.func.count(Comments.sentiment))
                .filter(Playlist.sno==Videos.sno)
                .filter(Videos.ID==Comments.ID)
                .filter(Comments.sentiment=='True')
                .group_by(Playlist.sno)
                .group_by(Comments.sentiment)
                .order_by(Playlist.sno)
                ).all()
            out={}
            for x in range(0,len(result)):
                # print(result[x][2])
                out[x]=math.ceil(100*result[x][2]/(Total_result[x][1]+0.00001))
                # print(out[x])
                # print(Total_result[x])
            prediction_data = tdif.transform(count.transform(X_test.text))
            predicted = model.predict(prediction_data.toarray())
            print(np.mean(predicted == y_test))
            # print(model.predict(tdif.transform(count.transform(["product"])).toarray()))
            # print( accuracy_score(y_test, predicted),'Clasification report:',classification_report(y_test, predicted) ,'Confussion matrix:',confusion_matrix(y_test, predicted))
            return (classification_report(y_test, predicted),
                    accuracy_score(y_test, predicted),
                    confusion_matrix(y_test, predicted),
                    out)  

# SA=Sentiment()
# SA._SA()
