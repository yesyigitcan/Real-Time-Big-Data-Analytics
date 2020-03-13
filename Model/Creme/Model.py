from creme.neighbors import KNeighborsRegressor
import time
import os
import datetime
import sys

# Global Parameters
LISTEN_DELAY = 1 # seconds
is_windows = 0 if os.name == "posix" else 1 # posix = linux

# Path Location
if is_windows:
    DATA_PATH = "..\\..\\Data Flow Mechanism\\Data\\"
else:
    DATA_PATH = "../../Data Flow Mechanism/Data/"
CURRENT_DATE = str(datetime.datetime.now().date())
FINAL_PATH = DATA_PATH + CURRENT_DATE

PROCESSED_FILE_COUNT = 0

MODEL = KNeighborsRegressor()

while True:
    print("Total Processed File Count:",PROCESSED_FILE_COUNT)
    time.sleep(1)
    if str(datetime.datetime.now().date()) != CURRENT_DATE:
        if os.listdir(FINAL_PATH):
            pass
        else:
            CURRENT_DATE = str(datetime.datetime.now().date())
            FINAL_PATH = DATA_PATH + CURRENT_DATE
            if is_windows:
                os.system("RD /S /Q " + FINAL_PATH)
            else:
                os.system("rm -rf " + FINAL_PATH)

    try:
        for FILE_NAME in os.listdir(FINAL_PATH):
            try:
                if is_windows:
                    DATA_FILE_PATH = FINAL_PATH + "\\" + FILE_NAME
                else:
                    DATA_FILE_PATH = FINAL_PATH + "/" + FILE_NAME
                with open(DATA_FILE_PATH, 'r') as FILE:
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
                if is_windows:
                    os.remove(FINAL_PATH + "\\" + FILE_NAME)
                else:
                    os.remove(FINAL_PATH + "/" + FILE_NAME)
            except Exception as e:
                print("Error", FILE_NAME, str(e))
    except Exception as e:
        print(str(e))
    time.sleep(LISTEN_DELAY)
