import csv
import time
import random
import datetime
import os

def changeDate(DATA_PATH, LOG_PATH , CURRENT_DATE):
    if not os.path.exists(DATA_PATH + "\\" + CURRENT_DATE):
        os.system("mkdir " + DATA_PATH + "\\" + CURRENT_DATE)
    if not os.path.exists(LOG_PATH + "\\" + CURRENT_DATE):
        os.system("mkdir " + LOG_PATH + "\\" + CURRENT_DATE)


CURRENT_DATE = str(datetime.datetime.now().date())
DATASET_PATH = "..\\Dataset\\pmdataset.csv"
DATA_PATH = ".\\Data\\"
LOG_PATH = ".\\DataLogs\\"

changeDate(DATA_PATH, LOG_PATH , CURRENT_DATE)

LOG_COUNTER = 1
DELAY_SECONDS = 10
random.seed(62)


try:
    with open("Settings.txt", 'r') as FILE:
        line = FILE.readline().strip("\n")
        while line:
            if line.split(' ')[0] == "DELAY_SECONDS":
                DELAY_SECONDS = int(line.split(' ')[1])
            line = FILE.readline().strip("\n")
except Exception as e:
    print(str(e))

with open(DATASET_PATH, 'r') as FILE:
    csvreader = csv.reader(FILE)
    for row in csvreader:
        # If date change, create new folder
        if str(datetime.datetime.now().date()) != CURRENT_DATE:
            CURRENT_DATE = str(datetime.datetime.now().date())
            changeDate(DATA_PATH, LOG_PATH, CURRENT_DATE)

        TEXT = ""
        time.sleep(random.randint(1, DELAY_SECONDS))
        FILE = open(DATA_PATH + "\\" + CURRENT_DATE + "\\" + str(LOG_COUNTER)+".txt", 'w')
        FILE2 = open(LOG_PATH + "\\" + CURRENT_DATE + "\\" + str(LOG_COUNTER) + ".txt", 'w')
        for column in row:
            TEXT += column + " "
        TEXT = TEXT[:-1]
        FILE.write(TEXT)
        FILE2.write(TEXT)
        FILE.close()
        FILE2.close()
        print(str(LOG_COUNTER) + ".txt Generated")
        LOG_COUNTER += 1
