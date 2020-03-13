import os
import sys

is_windows = 0 if os.name == "posix" else 1 # posix = linux

if is_windows:
    LOG_PATH = ".\\DataLogs\\"
else:
    LOG_PATH = "./DataLogs/"
FOLDER_LIST = os.listdir(LOG_PATH)
for FOLDER in FOLDER_LIST:
    if is_windows:
        os.system("RD /S /Q " + LOG_PATH + FOLDER)
    else:
        os.system("rm -rf " + LOG_PATH + FOLDER)


print("Clean Done!")