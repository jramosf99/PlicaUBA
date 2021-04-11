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
pathSockets="/home/ramos/Escritorio/TFG/TFG/data/Sockets.csv"
pathUsers="/home/ramos/Escritorio/TFG/TFG/data/Users.csv"
outputpath="./json.json"

# p1 = Process(target=process, args=(pathProcessCSV,))
# p1.start()
# p2 = Process(target=activitytrack, args=(pathActivityTrackCSV,))
# p2.start()
# p3 = Process(target=files, args=(pathFilesCSV,pathFilesToWatch,))
# p3.start()
# p4 = Process(target=browsers, args=(pathBrowsersCSV,))
# p4.start()
# p5 = Process(target=network, args=(pathNetworksCSV,))
# p5.start()
# p6 = Process(target=sockets, args=(pathSockets,))
# p6.start()
# p7 = Process(target=users, args=(pathUsers,))
# p7.start()
q = queue.Queue()
threading.Thread(target=activitytrack, args=(pathActivityTrackCSV,q,False)).start()
threading.Thread(target=browsers, args=(pathBrowsersCSV,q,False)).start()
threading.Thread(target=files, args=(pathFilesCSV,pathFilesToWatch,q,False)).start()
threading.Thread(target=network, args=(pathNetworksCSV,q,False)).start()
threading.Thread(target=process, args=(pathProcessCSV,q, False), daemon=True).start()
threading.Thread(target=sockets, args=(pathSockets,q,False)).start()
threading.Thread(target=users, args=(pathUsers,q,False)).start()
def write_json(data, filename=outputpath):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

while True:
    element= q.get()
    with open(outputpath) as json_file:
        data = json.load(json_file)
        temp = data['events']
        temp.append(element)     
    write_json(data) 

