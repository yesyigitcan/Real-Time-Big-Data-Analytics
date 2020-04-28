import pymysql 
import pandas
from sqlalchemy import create_engine
import logging
import logging.handlers
import os


logging.basicConfig(filename='Classical.log',
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

X_train, X_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.30, random_state=42)

##### Data Set Info ######
print("Tablename:", tablename)
logging.info("Tablename: " + tablename)

###### Support Vector Regression #####
from sklearn.svm import SVR
model = SVR()
model.fit(X_train, y_train)

print("SVR | Accuracy Score:", model.score(X_test, y_test))
logging.info("SVR | Accuracy Score: " + str(model.score(X_test, y_test)))
print("SVR | MSE:", mean_squared_error(y_test, model.predict(X_test)))
logging.info("SVR | MSE: " + str(mean_squared_error(y_test, model.predict(X_test))))

##### Random Forest Regression #####
from sklearn.ensemble import RandomForestRegressor 
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

print("Random Forest | Accuracy Score:", model.score(X_test, y_test))
logging.info("Random Forest | Accuracy Score: " + str(model.score(X_test, y_test)))
print("Random Forest | MSE:", mean_squared_error(y_test, model.predict(X_test)))
logging.info("Random Forest | MSE: " + str(mean_squared_error(y_test, model.predict(X_test))))

##### KNN Regression #####
from sklearn.neighbors import KNeighborsRegressor
model = KNeighborsRegressor()
model.fit(X_train, y_train)

print("KNN | Accuracy Score:", model.score(X_test, y_test))
logging.info("KNN | Accuracy Score: " + str(model.score(X_test, y_test)))
print("KNN | MSE:", mean_squared_error(y_test, model.predict(X_test)))
logging.info("KNN | MSE: " + str(mean_squared_error(y_test, model.predict(X_test))))

##### Linear Regression #####
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

print("Linear Regression | Accuracy Score:", model.score(X_test, y_test))
logging.info("Linear Regression | Accuracy Score: " + str(model.score(X_test, y_test)))
print("Linear Regression | MSE:", mean_squared_error(y_test, model.predict(X_test)))
logging.info("Linear Regression | MSE: " + str(mean_squared_error(y_test, model.predict(X_test))))

##### Decision Tree Regression #####
from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

print("Decision Tree Regression | Accuracy Score:", model.score(X_test, y_test))
logging.info("Decision Tree Regression | Accuracy Score: " + str(model.score(X_test, y_test)))
print("Decision Tree Regression | MSE:", mean_squared_error(y_test, model.predict(X_test)))
logging.info("Decision Tree Regression | MSE: " + str(mean_squared_error(y_test, model.predict(X_test))))

##### Bayesian Ridge #####
from sklearn.linear_model import BayesianRidge
model = BayesianRidge()
model.fit(X_train, y_train)

print("Bayesian Ridge | Accuracy Score:", model.score(X_test, y_test))
logging.info("Bayesian Ridge | Accuracy Score: " + str(model.score(X_test, y_test)))
print("Bayesian Ridge | MSE:", mean_squared_error(y_test, model.predict(X_test)))
logging.info("Bayesian Ridge | MSE: " + str(mean_squared_error(y_test, model.predict(X_test))))
