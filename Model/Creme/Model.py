from creme.neighbors import KNeighborsRegressor
import time
import os
import datetime

MODEL = KNeighborsRegressor()
DATA_PATH = "..\\..\\Data Flow Mechanism\\Data\\"
CURRENT_DATE = str(datetime.datetime.now().date())
FINAL_PATH = DATA_PATH + CURRENT_DATE
PROCESSED_FILE_COUNT = 0

while True:
    print("Total Processed File Count:",PROCESSED_FILE_COUNT)
    time.sleep(1)
    if str(datetime.datetime.now().date()) != CURRENT_DATE:
        if os.listdir(FINAL_PATH):
            pass
        else:
            CURRENT_DATE = str(datetime.datetime.now().date())
            FINAL_PATH = DATA_PATH + CURRENT_DATE
            os.system("RD /S /Q " + FINAL_PATH)

    try:
        for FILE_NAME in os.listdir(FINAL_PATH):
            with open(FINAL_PATH + "\\" + FILE_NAME, 'r') as FILE:
                DATA_ROW = FILE.readline().strip("\n")
                COLUMNS = DATA_ROW.split(" ")
                x = {}
                for i in range(len(COLUMNS[:4])):
                    x.update({i: float(COLUMNS[i])})
                print(x)

                y = float(COLUMNS[5])
                print("Predict: ", MODEL.predict_one(x), " REAL: ", y)
                MODEL.fit_one(x, y)
                PROCESSED_FILE_COUNT += 1
            os.remove(FINAL_PATH + "\\" + FILE_NAME)
    except Exception as e:
        print(str(e))
