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

metrics = (
    MSE(), 
    Accuracy(),
    MultiFBeta(betas=({1:0.5, 2:0.5, 3:0.5, 4:0.5}))
    )

model = (
     StandardScaler() |
     DecisionTreeClassifier()
)
logging.info("Initial model created")
# Mse Accuracy Real
recordNumber = len(y)
text = ""
iterationTimeCounter = 0.0
previous_time = 0.0
logging.info("Learning process has been started")
for row, target, time_passed in tqdm.tqdm(zip(x, y, timeList)):
    time_range = time_passed - previous_time
    '''
    if time_range > 0.0:
        time.sleep(time_range)
    '''
    try:
        iterationStartTime = time.time()
        y_pred = model.predict_one(row)
        model.fit_one(row, target)
        if y_pred is None:
            continue
        iterationEndTime = time.time()
        iterationTimeCounter += iterationEndTime - iterationStartTime
        for metric in metrics:
            metric.update(target, y_pred)
            #print("%.5f" % metric.get(), end=" ")
            text += "%.5f" % metric.get() + ","
    except Exception as e:
        print("error||" + str(e))
        
    '''
    text += str(target) + "," + str(y_pred) + "," + str(time_passed) + "," + str(time_range) + ","
    if target == y_pred:
        text += "1\n"
    else:
        text += "0\n"
    print("Real:", target, " Predicted:", y_pred, " Time:", "%.5f" % time_passed, " Sleep Time:", "%.5f" % time_range)
    '''
    '''
    previous_time = time_passed
    mseRequest = requests.get('http://localhost:7070/elderlySensor/1/incremental/mse/' + str(metrics[0].get() * 100))
    print(mseRequest.status_code)
    accRequest = requests.get('http://localhost:7070/elderlySensor/1/incremental/acc/' + str(metrics[1].get() * 100))
    print(accRequest.status_code)
    '''
logging.info("Learning process is done")
logging.info("Total time for iterations in second " + str(iterationTimeCounter))
logging.info("Average time for an iteration in second " + str(iterationTimeCounter / recordNumber))
logging.info("Record number " + str(recordNumber))
logging.info("Mean squared error " + str(metrics[0].get()))
logging.info("Accuracy " + str(metrics[1].get()))
print("MSE: ", metrics[0].get())
print("Accuracy: ", metrics[1].get())
print("Multiclass F Beta: ", metrics[2].get())
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


    



