from process import process
from activitytrack import  activitytrack
from files import files
from browsers import browsers
from network import network
from sockets import sockets
from users import users
from multiprocessing import Process
import threading, queue
import json
pathProcessCSV = "/home/ramos/Escritorio/TFG/TFG/data/process.csv" #output
pathActivityTrackCSV = "/home/ramos/Escritorio/TFG/TFG/data/activitytrack.csv" #output
pathFilesCSV = "/home/ramos/Escritorio/TFG/TFG/data/files.csv" #output
pathFilesToWatch = '/home/ramos/Escritorio/tocar/activitywatch-master' #folder to be watched 
pathBrowsersCSV = "/home/ramos/Escritorio/TFG/TFG/data/Browsers.csv"
pathNetworksCSV = "/home/ramos/Escritorio/TFG/TFG/data/Network.csv"
pathSocketsCSV="/home/ramos/Escritorio/TFG/TFG/data/Sockets.csv"
pathUsersCSV="/home/ramos/Escritorio/TFG/TFG/data/Users.csv"
outputpathJSON="./json.json"
pathProcessJSON = "/home/ramos/Escritorio/TFG/TFG/data/process.json" #output
pathActivityTrackJSON = "/home/ramos/Escritorio/TFG/TFG/data/activitytrack.json" #output
pathFilesJSON = "/home/ramos/Escritorio/TFG/TFG/data/files.json" #output
pathBrowsersJSON = "/home/ramos/Escritorio/TFG/TFG/data/Browsers.json"
pathNetworksJSON = "/home/ramos/Escritorio/TFG/TFG/data/Network.json"
pathSocketsJSON="/home/ramos/Escritorio/TFG/TFG/data/Sockets.json"
pathUsersJSON="/home/ramos/Escritorio/TFG/TFG/data/Users.json"
outputpathJSON="./json.json"


q = queue.Queue()
threading.Thread(target=activitytrack, args=(pathActivityTrackCSV,q,False)).start()
threading.Thread(target=browsers, args=(pathBrowsersCSV,q,False)).start()
threading.Thread(target=files, args=(pathFilesCSV,pathFilesToWatch,q,False)).start()
threading.Thread(target=network, args=(pathNetworksCSV,q,False)).start()
threading.Thread(target=process, args=(pathProcessCSV,q, False), daemon=True).start()
threading.Thread(target=sockets, args=(pathSocketsCSV,q,False)).start()
threading.Thread(target=users, args=(pathUsersCSV,q,False)).start()

def write_json(data, filename=outputpathJSON):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

while True:
    element= q.get()
    with open(outputpathJSON) as json_file:
        data = json.load(json_file)
        temp = data['events']
        temp.append(element)     
    write_json(data) 

