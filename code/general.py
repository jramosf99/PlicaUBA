from process import process
from activitytrack import  activitytrack
from files_win import files_win
from browsers import browsers
from network import network
from sockets import sockets
from users import users
from multiprocessing import Process
import threading, queue
import json
import time
import os
pathProcessCSV = "../data/process.csv" #output
pathActivityTrackCSV = "../data/activitytrack.csv" #output
pathFilesCSV = "../data/files.csv" #output
pathFilesToWatch =  r'C:\Users\jramo\Downloads\hadoop\hadoop-3.1.0' #folder to be watched 
pathBrowsersCSV = "../data/Browsers.csv"
pathNetworksCSV = "../data/Network.csv"
pathSocketsCSV="../data/Sockets.csv"
pathUsersCSV="../data/Users.csv"
pathProcessJSON = "../data/process/process.json" #output
pathActivityTrackJSON = "../data/activitytrack/activitytrack.json" #output
pathFilesJSON = "../data/files/files.json" #output
pathBrowsersJSON = "../data/Browsers/Browsers.json"
pathNetworksJSON = "../data/Network/Network.json"
pathSocketsJSON="../data/Sockets/Sockets.json"
pathUsersJSON="../data/Users/Users.json"
outputpathJSON="./json.json"

if __name__ == '__main__':  

    jsons = [outputpathJSON,pathActivityTrackJSON,pathBrowsersJSON,pathFilesJSON,pathNetworksJSON,pathProcessJSON,pathSocketsJSON,pathUsersJSON]

    q = queue.Queue()
    t1= threading.Thread(target=activitytrack, args=(pathActivityTrackCSV,q,False, 60), daemon=True)
    t2 = threading.Thread(target=browsers, args=(pathBrowsersCSV,q,False, 10), daemon=True)
    t3 = threading.Thread(target=files_win, args=(pathFilesCSV,pathFilesToWatch,q,False), daemon=True)
    t4 = threading.Thread(target=network, args=(pathNetworksCSV,q,False,120), daemon=True)
    t5 = threading.Thread(target=process, args=(pathProcessCSV,q, False, 10), daemon=True)
    t6 = threading.Thread(target=sockets, args=(pathSocketsCSV,q,False, 10), daemon=True)
    t7 = threading.Thread(target=users, args=(pathUsersCSV,q,False, 120), daemon=True)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    def write_json(data, filename):
        with open(filename,'w') as f:
            json.dump(data, f, indent=4)

    try:
        while True:
            time.sleep(1)
            element= q.get()
            head, tail = os.path.split(jsons[element["eventType"]])
            if not os.path.isdir(head):
                os.mkdir(head)
            if not os.path.isfile(jsons[element["eventType"]]):
                data = {}
                data['events'] = []
                with open(jsons[element["eventType"]], 'w') as file:
                    json.dump(data, file, indent=4)
            with open(jsons[element["eventType"]]) as json_file:
                data = json.load(json_file)
                temp = data['events']
                temp.append(element)     
            write_json(data,jsons[element["eventType"]]) 
    except KeyboardInterrupt:
        print("programa terminado")