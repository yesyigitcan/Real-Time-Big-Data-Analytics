import os
import sys
import pandas
import pymysql 
from sqlalchemy import create_engine

path_1 = "C:\\Users\\YigitCan\\Desktop\\Tez-Workspace\\Dataset\\Elderly People Sensor\\S1_Dataset"
path_2 = "C:\\Users\\YigitCan\\Desktop\\Tez-Workspace\\Dataset\\Elderly People Sensor\\S2_Dataset"

# Participants were allocated in two clinical room settings (S1 and S2). The setting of S1 (Room1) uses 4 RFID reader 
# antennas around the room (one on ceiling level, and 3 on wall level) for the collection of data, 
# whereas the room setting S2 (Room2) uses 3 RFID reader antennas (two at ceiling level and one at wall level) 
# for the collection of motion data. 
inside_attributes = ["time(second)", "acceleration_g_frontal", "acceleration_g_vectical", "acceleration_g_lateral",
                    "id of antenna", "signal strength indicator", "phase", "frequency", "class"]
                    # Class 1: sit on bed, 2: sit on chair, 3: lying, 4: ambulating 
                    # Gender 0: Male 1: Female
engine = create_engine('mysql+pymysql://root:@localhost/tez')
session = 1
for path in [path_1, path_2]:
    for filename in os.listdir(path):
        currentPath = path + "\\" + filename
        if filename[0] != 'd':
            continue
        room = int(filename[1])
        if(filename[-1].upper() == 'M'):
            gender = 0
        elif(filename[-1].upper() == 'F'):
            gender = 1
        else:
            raise TypeError
        df = pandas.read_csv(currentPath, names=inside_attributes)
        df["room"] = room
        df["session"] = session
        df["gender"] = gender
        df.to_sql(name="elderly_sensor",con=engine,if_exists="append")
        session += 1

# PATH C:\XAMPP\MYSQL\BIN;%PATH%;
# mysql -u root -p




