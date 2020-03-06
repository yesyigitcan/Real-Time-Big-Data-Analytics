import os

LOG_PATH = ".\\DataLogs\\"
FOLDER_LIST = os.listdir(LOG_PATH)
for FOLDER in FOLDER_LIST:
    os.system("RD /S /Q " + LOG_PATH + FOLDER)


print("Clean Done!")