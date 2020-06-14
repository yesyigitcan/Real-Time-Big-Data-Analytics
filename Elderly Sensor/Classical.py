from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, fbeta_score
from sqlalchemy import create_engine
import pandas
import logging
import time
import requests

logging.basicConfig(filename='ElderlyClassical.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.INFO)

logging.info("Creating connection")
engine = create_engine('mysql+pymysql://root:@localhost/tez')
logging.info("Connection is ready")

session = 60
#query = "select * from elderly_sensor where session = "+str(session)+" order by 'time(second)'"
query = "select * from elderly_sensor"

df = pandas.read_sql(query, engine)
#logging.info("Data retrieved by Session = " + str(session))
logging.info("Data retrieved by all")
df = df.drop("index", axis=1)
df = df.drop("time(second)", axis=1)
X = df.drop("class", axis=1)
y = list(df["class"])


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
predict = model.predict(X_test)
predictEndTime = time.time()
acc = accuracy_score(y_test, predict)
mse = mean_squared_error(y_test, predict)
fbeta = fbeta_score(y_test, predict, average='macro', beta=0.5)
logging.info("Total time for learning part in second " + str(learningEndTime - learningStartTime))
logging.info("Total time for prediction part in second " + str(predictEndTime - predictStartTime))
logging.info("Train record number " + str(len(y_train)))
logging.info("Test record number " + str(len(y_test)))
logging.info("Mean squared error " + str(mse))
logging.info("Accuracy " + str(acc))
print("Metrics by Test Set") 
print("MSE:", mse)
print("Accuracy:", acc)
print("Multiclass F Beta:", fbeta)


X = scaler.transform(X)
predict2 = model.predict(X, y)
acc = accuracy_score(y, predict2)
mse = mean_squared_error(y, predict2)

'''
mseRequest = requests.get('http://localhost:7070/elderlySensor/1/classical/mse/' +  str(mse * 100))
print(mseRequest.status_code)
accRequest = requests.get('http://localhost:7070/elderlySensor/1/classical/acc/' +  str(acc * 100))
print(accRequest.status_code)
'''
print("Metrics by All")
print("MSE:", mse)
print("Accuracy:", acc)
'''
if (str(input("Real/Predict Comparision? (y:Yes)"))[0].lower() == 'y'):
    for real, predict in zip(y_test, predict):
        print("Real:", real, " Predicted:", predict)
'''