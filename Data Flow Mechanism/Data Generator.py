import csv
import time
import datetime
import os
import sys
import random
random.seed(62)

# Global Parameters - Constants
DELAY_SECONDS = 10
is_windows = 0 if os.name == "posix" else 1 # posix = linux

# Global Variables
LOG_COUNTER = 1

# Functions
def createDateFolder(DATA_PATH, LOG_PATH , CURRENT_DATE, is_windows):
    if is_windows:
        if not os.path.exists(DATA_PATH + "\\" + CURRENT_DATE):
            os.system("mkdir " + DATA_PATH  + CURRENT_DATE)
        if not os.path.exists(LOG_PATH + "\\" + CURRENT_DATE):
            os.system("mkdir " + LOG_PATH + CURRENT_DATE)
    else:
        if not os.path.exists(DATA_PATH + "/" + CURRENT_DATE):
            os.system("mkdir " + DATA_PATH  + CURRENT_DATE)
        if not os.path.exists(LOG_PATH + "/" + CURRENT_DATE):
            os.system("mkdir " + LOG_PATH + CURRENT_DATE)

# Path Location
if is_windows:
    DATASET_PATH = "..\\Dataset\\pmdataset.csv"
    DATA_PATH = ".\\Data\\"
    LOG_PATH = ".\\DataLogs\\"
else:
    DATASET_PATH = "../Dataset/pmdataset.csv"
    DATA_PATH = "./Data/"
    LOG_PATH = "./DataLogs/"


# Use Settings.txt for Configuration (Delay between new data) 
try:
    with open("Settings.txt", 'r') as FILE:
        line = FILE.readline().strip("\n")
        while line:
            if line.split(' ')[0] == "DELAY_SECONDS":
                DELAY_SECONDS = int(line.split(' ')[1])
            line = FILE.readline().strip("\n")
except Exception as e:
    print(str(e))

# Main Part of Data Generation Operation
with open(DATASET_PATH, 'r') as FILE:
    # Initialize Date Formatted Folder
    CURRENT_DATE = str(datetime.datetime.now().date())
    createDateFolder(DATA_PATH, LOG_PATH , CURRENT_DATE, is_windows)

    csvreader = csv.reader(FILE)
    for row in csvreader:
        # If date change, create new folder
        if str(datetime.datetime.now().date()) != CURRENT_DATE:
            CURRENT_DATE = str(datetime.datetime.now().date())
            createDateFolder(DATA_PATH, LOG_PATH, CURRENT_DATE, is_windows)

        TEXT = ""
        time.sleep(random.randint(1, DELAY_SECONDS))
        if is_windows:
            FILE = open(DATA_PATH + CURRENT_DATE + "\\" + str(LOG_COUNTER)+".txt", 'w')
            FILE2 = open(LOG_PATH + CURRENT_DATE + "\\" + str(LOG_COUNTER) + ".txt", 'w')
        else:
            FILE = open(DATA_PATH + CURRENT_DATE + "/" + str(LOG_COUNTER)+".txt", 'w')
            FILE2 = open(LOG_PATH + CURRENT_DATE + "/" + str(LOG_COUNTER) + ".txt", 'w')
        for column in row:
            TEXT += column + " "
        TEXT = TEXT[:-1]
        FILE.write(TEXT)
        FILE2.write(TEXT)
        FILE.close()
        FILE2.close()
        print(str(LOG_COUNTER) + ".txt Generated")
        LOG_COUNTER += 1
