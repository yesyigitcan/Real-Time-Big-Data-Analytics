import pymysql 
import pandas
from sqlalchemy import create_engine



df = pandas.read_csv("..//pmsm_temperature_data.csv")
df["id"] = df.index

engine = create_engine('mysql+pymysql://root:@localhost/temperature')

df.to_sql(name="inf",con=engine,if_exists="append",index=False)
