import csv
import mysql.connector



db = mysql.connector.connect(
	host="localhost",
    user="root",
    passwd="",
    db="temperature"
)
		
def dbfunc(id, ln):
    #try:
    cur = db.cursor()
    query = """INSERT INTO inf (id, ambient, coolant, u_d, u_q, motor_speed, torque, i_d, i_q, pm, stator_yoke, stator_tooth, stator_winding, profile_id) VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


    args = (id ,ln[0],ln[1],ln[2],ln[3],ln[4],ln[5],ln[6],ln[7],ln[8],ln[9],ln[10],ln[11],ln[12])
    cur.execute(query, args)
    print("yaziliyor : "+ str(id ))
    db.commit()
    #except Error as error:
    #print(error)
    #finally:
    cur.close()
        #db.close()


with open("pmsm_temperature_data.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    flag = True
    sayi = -1
    for i, line in enumerate(reader):
        if not flag:
            #print ('line[{}] = {}'.format(i, line))
            sayi=sayi + 1
            ln = line[0].split(",")
            dbfunc(sayi, ln)
        else:
            column_names = line
            flag = False
    """
    print (column_names)
    print(line)
    print(" birinci")
    print(str(0) + ln[0])
    print(" ikinci   ::::")
    print(str(len(ln)) + ln[-1])
    """


"""
# Use all the SQL you like
cur.execute("INSERT INTO inf (ambient, coolant, u_d, u_q, motor_speed, torque, i_d, i_q, pm, stator_yoke, stator_tooth, .stator_winding, profile_id) VALUES ( -0.75214297, 7.7777777, 0.3279352, -1.2978575, -1.2224282,  -0.2501821, 1.0295724, -0.24586003, -2.522071, -1.8314217, -2.0661428, -2.0180326, 4 );")
"""
