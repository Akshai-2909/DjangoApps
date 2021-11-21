import datetime, time

path = "C:/Users/Desktop/Cn-project/main/log/log.txt"

def getTimeStamp():
    return "[" + str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + "]"


def write(msg):
    with open(path, "a+") as file:
        file.write(msg)
        file.write("\n")
