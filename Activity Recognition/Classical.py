from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, fbeta_score
from sqlalchemy import create_engine
import pandas
import logging
import time
import requests

logging.basicConfig(filename='ActivityRecogClassical.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.INFO)

n = 5
logging.info("Creating connection")
engine = create_engine('mysql+pymysql://root:@localhost/tez')
logging.info("Connection is ready")

limitForEachClass = 1000
logging.info("Limit for each class: " + str(limitForEachClass))
classNames = ["bike", "null", "sit", "stairsdown", "stairup", "stand", "walk"]

tableName = "accelerometer"
phoneType = "s3mini"

bigDf = None
for i in range(len(classNames)):
    query = "select x,y,z,gt from " + tableName + "_" + phoneType + " where gt = '" + classNames[i] + "' limit " + str(limitForEachClass)
    df = pandas.read_sql(query, engine)
    for i in range(1, n+1):
        df["x_" + str(i)] = None
        df["y_" + str(i)] = None
        df["z_" + str(i)] = None
    for i in range(n, len(df)):
        for j in range(1, n+1):
            df.loc[i, 'x_' + str(j)] = df.loc[i-j, 'x']
            df.loc[i, 'y_' + str(j)] = df.loc[i-j, 'y']
            df.loc[i, 'z_' + str(j)] = df.loc[i-j, 'z']
    df = df.dropna(subset=["x_1"])
    if type(bigDf) == None:
        bigDf = df
    else:
        bigDf = pandas.concat([bigDf, df])
logging.info("Big Df created")
X = bigDf.drop("gt", axis=1)
y = list(bigDf["gt"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = DecisionTreeClassifier()
logging.info("Initial model created")
logging.info("Learning process has been started")
learningStartTime = time.time()
model.fit(X_train, y_train)
learningEndTime = time.time()
logging.info("Learning process is done")
predictStartTime = time.time()
predictStartTime = time.time()
predict = model.predict(X_test)
predictEndTime = time.time()
logging.info("Train total time: " + str(learningEndTime - learningStartTime))
logging.info("Test total time: " + str(predictEndTime - predictStartTime))
acc = accuracy_score(y_test, predict)
requests.get('http://localhost:7070/activity/1/classical/m2/' +  str(acc * 100000))    
fbeta = fbeta_score(y_test, predict, average='macro', beta=0.5)
requests.get('http://localhost:7070/activity/1/classical/m1/' +  str(fbeta * 100000))
logging.info("Accuracy: " + str(acc))




