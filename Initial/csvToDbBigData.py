import csv
import mysql.connector
import tqdm

filepath = "..\\Dataset\\Activity recognition exp\\Activity recognition exp\\Phones_accelerometer.csv"
tablename = "accelerometer"


db = mysql.connector.connect(
	host="localhost",
    user="root",
    passwd="",
    db="tez"
)


cur = db.cursor()
cur.execute("select count(*) from " + tablename)
indexCounter = cur.fetchone()[0]
query = "insert into " + tablename + " (index, Arrival_Time, Creation_Time, x, y, z, Model, gt) values (%s, %s, %s, %s, %s, %s, %s, %s)"

with open(filepath, 'r') as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)
    query = "insert into " + tablename + " (id, Arrival_Time, x, y, z, Model, gt) values (%s, %s, %s, %s, %s, %s, %s);"
    for i, row in tqdm.tqdm(enumerate(reader)):
        
        
        args = (indexCounter, int(row[1]), float(row[3]), float(row[4]), float(row[5]), row[7], row[9])
        indexCounter += 1
        cur.execute(query, args)
        '''
        query = "insert into " + tablename + " (index, Arrival_Time, x, y, z, Model, gt) values ("
        query += str(indexCounter) + ","
        query += str(row[1]) + ","
        query += str(row[3]) + ","
        query += str(row[4]) + ","
        query += str(row[5]) + ","
        query += "'" + str(row[7]) + "',"
        query += "'" + str(row[9]) + "')"
        cur.execute(query)
        '''
        if i % 100 == 0:
            db.commit()

cur.close()