from creme.neighbors import KNeighborsClassifier
from creme.tree import DecisionTreeClassifier
from creme.preprocessing import StandardScaler
from creme.metrics import MSE, Accuracy
import pandas
from sqlalchemy import create_engine
from creme.compose import Pipeline
import time
import matplotlib.pyplot as plt

engine = create_engine('mysql+pymysql://root:@localhost/tez')

session = 41
query = "select * from elderly_sensor where session = "+str(session)+" order by 'time(second)'"
df = pandas.read_sql(query, engine)
df = df.drop("index", axis=1)
timeList = list(df["time(second)"])

df = df.drop("time(second)", axis=1)

x = df.drop("class", axis=1).to_dict(orient="row")
y = list(df["class"])

metrics = (
    MSE(), 
    Accuracy()
    )

model = (
     StandardScaler() |
     DecisionTreeClassifier()
)

# Mse Accuracy Real
outputfile = open('C:\\Users\\YigitCan\\Desktop\\Tez-Workspace\\Real-Time-Big-Data-Analytics\\Elderly Sensor\\Output'+str(session)+'.txt', 'w')



previous_time = 0.0
for row, target, time_passed in zip(x, y, timeList):
    time_range = time_passed - previous_time
    if time_range != 0.0:
        time.sleep(time_range)
    y_pred = model.predict_one(row)
    model.fit_one(row, target)
    if y_pred is None:
        continue
    for metric in metrics:
        metric.update(target, y_pred)
        print("%.5f" % metric.get(), end=" ")
        outputfile.write("%.5f" % metric.get() + ",")
    
    outputfile.write(str(target) + "," + str(y_pred) + "," + str(time_passed) + "," + str(time_range) + ",")
    if target == y_pred:
        outputfile.write("1\n")
    else:
        outputfile.write("0\n")
    print("Real:", target, " Predicted:", y_pred, " Time:", "%.5f" % time_passed, " Sleep Time:", "%.5f" % time_range)
    previous_time = time_passed
outputfile.close()
    


    



