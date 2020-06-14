from creme.neighbors import KNeighborsClassifier
from creme.tree import DecisionTreeClassifier
from creme.preprocessing import StandardScaler
from creme.metrics import MSE, Accuracy, MultiFBeta
import pandas
from sqlalchemy import create_engine
from creme.compose import Pipeline
import time
import matplotlib.pyplot as plt
import requests
import logging
import logging.handlers
import tqdm

logging.basicConfig(filename='ElderlyIncremental.log',
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
timeList = list(df["time(second)"])

df = df.drop("time(second)", axis=1)

x = df.drop("class", axis=1).to_dict(orient="row")
y = list(df["class"])


acc = Accuracy()
fbeta = MultiFBeta(betas=({1:0.5, 2:0.5, 3:0.5, 4:0.5})) 

model = (
     StandardScaler() |
     DecisionTreeClassifier()
)
logging.info("Initial model created")
# Mse Accuracy Real
recordNumber = len(y)
text = ""
previous_time = 0.0
logging.info("Learning process has been started")
startTime = time.time()
for row, target, time_passed in tqdm.tqdm(zip(x, y, timeList)):
    '''
    time_range = time_passed - previous_time
    
    if time_range > 0.0:
        time.sleep(time_range)
    previous_time = time_passed
    '''
    try:
        y_pred = model.predict_one(row)
        model.fit_one(row, target)
        if y_pred is None:
            continue
        acc.update(target, y_pred)
        fbeta.update(target, y_pred)
        requests.get('http://localhost:7070/elderlySensor/1/incremental/m1/' + str(fbeta.get() * 100000))
        requests.get('http://localhost:7070/elderlySensor/1/incremental/m2/' + str(acc.get() * 100000))
    except Exception as e:
        print("error||" + str(e))
        
    
endTime = time.time()
totalTime = endTime - startTime
logging.info("Learning process is done")
logging.info("Total time " + str(totalTime))
logging.info("Time per one iteration " + str(totalTime / recordNumber))
logging.info("Record number " + str(recordNumber))
logging.info("Accuracy " + str(acc.get()))
logging.info("Multiclass F Beta " + str(fbeta.get()))

print("Accuracy: ", acc.get())
print("Multiclass F Beta: ", fbeta.get())



















'''
try:
    outputfile = open('C:\\Users\\YigitCan\\Desktop\\Tez-Workspace\\Real-Time-Big-Data-Analytics\\Elderly Sensor\\Output'+str(session)+'.txt', 'w')
except:
    print("File cannot create at specific position")
    import os
    print("So it is created in " , os.getcwd())
    outputfile = open("output.txt", 'w')
outputfile.write(text)
outputfile.close()
'''    


    



