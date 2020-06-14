from creme.neighbors import KNeighborsClassifier
from creme.tree import DecisionTreeClassifier
from creme.preprocessing import StandardScaler
from creme.metrics import MSE,Accuracy, F1, LogLoss,MultiFBeta
import pandas
from sqlalchemy import create_engine
from creme.compose import Pipeline
import time
import matplotlib.pyplot as plt
import requests
import logging
import logging.handlers
import mysql.connector
import tqdm

dataPackageLimit = 100000
tableName = "accelerometer"
phoneType = "s3mini"

db = mysql.connector.connect(
	host="localhost",
    user="root",
    passwd="",
    db="tez"
)


cur = db.cursor()
cur.execute("select count(*) from " + tableName + "_" + phoneType + " where Model = '" + phoneType + "'")
tableSize = int(cur.fetchone()[0])
cur.close()
del db

stepNumber = int(tableSize / dataPackageLimit)

logging.basicConfig(filename='ActivityRecogIncremental.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.INFO)
logging.info("Creating connection")
engine = create_engine('mysql+pymysql://root:@localhost/tez')
logging.info("Connection is ready")

n = 5
metrics = (
    Accuracy(),
    MultiFBeta(betas=({'bike':1, 'null':1, 'sit':1, 'stairsdown':1, 'stairsup':1, 'stand':1, 'walk':1}))
)



model = (
     StandardScaler() |
     DecisionTreeClassifier()
)
logging.info("Initial model created for phone type " + phoneType)

#modelName = ["nexus4", "s3", "s3mini", "samsungold"]
previousTime = None
logging.info("Learning stage started with total step of " + str(stepNumber))
for step in tqdm.tqdm(range(stepNumber+1)):
    logging.info("Data retrieved at step " + str(step+1) + "/" + str(stepNumber))
    if step < stepNumber:
        query = "select * from " + tableName + "_" + phoneType + " where Model = '" + phoneType + "' and id >= " + str(step * dataPackageLimit) + " and id <= " + str((step+1) * dataPackageLimit)
    else:
        query = "select * from " + tableName + "_" + phoneType + " where Model = '" + phoneType + "' and id < " + str(stepNumber * dataPackageLimit)
    df = pandas.read_sql(query, engine)
    df = df.drop("id", axis=1)
    df = df.drop('Arrival_Time', axis=1)
    df = df.drop("Model", axis=1)
    x = df.drop("gt", axis=1).to_dict(orient="row")
    y = list(df["gt"])

    window = [] #  [ (x_1,y_1,z_1), (x_2,y_2,z_2), .... ]
    for row, target in tqdm.tqdm(zip(x, y)):
        if len(window) < n:
            window.append((row["x"], row["y"], row["z"]))
            continue
        for i in range(n):
            row.update({"x_" + str(i): window[i][0]})
            row.update({"y_" + str(i): window[i][1]})
            row.update({"z_" + str(i): window[i][2]})

        for i in range(n-1):
            window[i] = window[i+1]
        window[-1] = (row["x"], row["y"], row["z"])  
        
        y_pred = model.predict_one(row)
        model.fit_one(row, target)
        if y_pred is None:
            continue
        for metric in metrics:
            metric.update(target, y_pred)
            #print(metric.get(), end=" ")
        requests.get('http://localhost:7070/elderlySensor/1/incremental/acc/' + str(metrics[0].get() * 100))
logging.info("Learning stage is done")
logging.info("Test stage started")

engine = create_engine('mysql+pymysql://root:@localhost/tez')
logging.info("New connection for test stage established")

limitForEachClass = 100
classNames = ["bike", "null", "sit", "stairsdown", "stairup", "stand", "walk"]
logging.info("Test stage has " + str(limitForEachClass) + " records for each class from " + str(len(classNames)) + " different classes")


bigDf = None
for i in range(len(classNames)):
    query = "select x,y,z,gt from accelerometer a  where a.Model = '" + phoneType + "' and a.gt = '" + classNames[i] + "' limit " + str(limitForEachClass)
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
logging.info("Test data set has been created")

metrics = (
    Accuracy(),
    MultiFBeta(betas=({'bike':1, 'null':1, 'sit':1, 'stairsdown':1, 'stairsup':1, 'stand':1, 'walk':1}))
)
logging.info("Metrics are reset")
bigDf = bigDf.reset_index()
X = bigDf.drop("gt", axis=1)
y = list(bigDf["gt"])

logging.info("Test results have been started to send to Grafana")
for i in range(len(y)):
    row = X.iloc[i]
    y_pred = model.predict_one(row)
    y_real = y[i] 
    if y_pred is None:
        continue
    for metric in metrics:
        metric.update(y_real, y_pred)
    requests.get('http://localhost:7070/elderlySensor/1/incremental/acc/' + str(metrics[0].get() * 100))
logging.info("All processes are done")




    


    



