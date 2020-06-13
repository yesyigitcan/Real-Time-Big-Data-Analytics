from creme.neighbors import KNeighborsClassifier
from creme.tree import DecisionTreeClassifier
from creme.preprocessing import StandardScaler
from creme.metrics import MSE, Accuracy
import pandas
from sqlalchemy import create_engine
from creme.compose import Pipeline
import time
import matplotlib.pyplot as plt
import requests
import logging
import logging.handlers
import mysql.connector
dataPackageLimit = 100000
tableName = "accelerometer"


db = mysql.connector.connect(
	host="localhost",
    user="root",
    passwd="",
    db="tez"
)


cur = db.cursor()
cur.execute("select count(*) from " + tableName)
tableSize = int(cur.fetchone()[0])
cur.close()
del db

stepNumber = int(tableSize / dataPackageLimit)
offsetNumber = tableSize - stepNumber * dataPackageLimit

logging.basicConfig(filename='ActivityRecogIncremental.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.INFO)
logging.info("Creating connection")
engine = create_engine('mysql+pymysql://root:@localhost/tez')
logging.info("Connection is ready")

'''
metrics = (
    MSE(), 
    Accuracy()
    )
'''
metric = Accuracy()

model = (
     StandardScaler() |
     DecisionTreeClassifier()
)
logging.info("Initial model created")

#modelName = ["nexus4", "s3", "s3mini", "samsungold"]
previousTime = None
for step in range(stepNumber):
    logging.info("Data retrieved at step " + str(step+1) + "/" + str(stepNumber))
    query = "select * from " + tableName + " where Model = 'nexus4' and id >= " + str(step * dataPackageLimit) + " and id <= " + str((step+1) * dataPackageLimit)
    df = pandas.read_sql(query, engine)
    df = df.drop("id", axis=1)
    df = df.drop('Arrival_Time', axis=1)
    df = df.drop("Model", axis=1)
    x = df.drop("gt", axis=1).to_dict(orient="row")
    y = list(df["gt"])
    
    n = 5
    window = [] #  [ (x_1,y_1,z_1), (x_2,y_2,z_2), .... ]
    for row, target in zip(x, y):
        if len(window) < n:
            window.append((row["x"], row["y"], row["z"]))
            continue
        for i in range(n):
            row.update({"x_" + str(i): window[i][0]})
            row.update({"y_" + str(i): window[i][1]})
            row.update({"z_" + str(i): window[i][2]})
        '''
        for name in modelName:
            if row["Model"] == name:
                row.update({name:1})
            else:
                row.update({name:0})
        row.pop("Model")
        '''

        for i in range(n-1):
            window[i] = window[i+1]
        window[-1] = (row["x"], row["y"], row["z"])  
        print(row)
        y_pred = model.predict_one(row)
        model.fit_one(row, target)
        if y_pred is None:
            continue
        '''
        for metric in metrics:
            metric.update(target, y_pred)
            print(metric.get(), end=" ")
        print()
        '''
        print("target: ", target, "  Pred: " , y_pred)
        metric.update(target, y_pred)
        print(metric.get())

    


    



