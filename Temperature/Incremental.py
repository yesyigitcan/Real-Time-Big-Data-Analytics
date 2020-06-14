import pymysql 
import pandas
from sqlalchemy import create_engine
import logging
import logging.handlers
import os
import requests
import tqdm
import time


logging.basicConfig(filename='Incremental.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.INFO)

host = "localhost"
username = "root"
password = ""
db = "temperature"

tablename = "inf_20"

engine = create_engine('mysql+pymysql://' + username + password +':@' + host + '/' + db)

df = pandas.read_sql_table(table_name=tablename, con=engine)

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error



# i_q is highly correlated with torque (ρ = 0.99656) Rejected
# stator_tooth is highly correlated with stator_yoke (ρ = 0.9499) Rejected
# stator_winding is highly correlated with stator_tooth (ρ = 0.96563) Rejected
# possible target features stator_yoke, stator_winding, stator_tooth, pm
	 
selected_features = ["ambient", "coolant", "u_d", "u_q", "motor_speed", "torque", "i_d", "stator_yoke"]
target_feature = "pm"


df_x = df[selected_features]
df_y = df[target_feature]


##### Data Set Info ######
print("Tablename:", tablename)
logging.info("Tablename: " + tablename)

import matplotlib.pyplot as plt
from creme.metrics import Accuracy, MSE

from creme.neighbors import KNeighborsRegressor
from creme.linear_model import LinearRegression

##### KNN Regression #####
model = KNeighborsRegressor()
mse = MSE()

startTime = time.time()
for x, y in tqdm.tqdm(zip(df_x.to_dict("records"), df_y)):
    y_pred = model.predict_one(x)
    mse.update(y, y_pred)
    requests.get("http://localhost:7070/temp/1/incremental/m1/" +  str(mse.get() * 100000))
    model = model.fit_one(x, y)

endTime = time.time()
totalTime = endTime - startTime
logging.info("Total Time: " + str(totalTime))
logging.info("Time per iteration: " + str(totalTime/len(list(df_y))))

print("KNN | MSE: " + str(mse.get()))
logging.info("KNN | MSE: " + str(mse.get()))

'''
##### Linear Regression #####
model = LinearRegression()
metric1 = MSE()

for x, y in zip(df_x.to_dict("records"), df_y):
    y_pred = model.predict_one(x)
    metric1.update(y, y_pred)
    model = model.fit_one(x, y)

print("Linear Regression | MSE: " + str(metric1.get()))
logging.info("Linear Regression | MSE: " + str(metric1.get()))
'''