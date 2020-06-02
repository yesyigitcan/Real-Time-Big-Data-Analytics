from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sqlalchemy import create_engine
import pandas

engine = create_engine('mysql+pymysql://root:@localhost/tez')

session = 41
query = "select * from elderly_sensor where session = "+str(session)+" order by 'time(second)'"

df = pandas.read_sql(query, engine)
df = df.drop("index", axis=1)
df = df.drop("time(second)", axis=1)
X = df.drop("class", axis=1)
y = list(df["class"])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
predict = model.predict(X_test)
acc = accuracy_score(y_test, predict)
mse = mean_squared_error(y_test, predict)

print("Metrics by Test Set")
print("MSE:", mse)
print("Accuracy:", acc)


X = scaler.transform(X)
predict2 = model.predict(X, y)
acc = accuracy_score(y, predict2)
mse = mean_squared_error(y, predict2)
print("Metrics by All")
print("MSE:", mse)
print("Accuracy:", acc)

if (str(input("Real/Predict Comparision? (y:Yes)"))[0].lower() == 'y'):
    for real, predict in zip(y_test, predict):
        print("Real:", real, " Predicted:", predict)