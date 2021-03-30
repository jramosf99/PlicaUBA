from process import process
from activitytrack import  activitytrack
from files import files
from browsers import browsers
from network import network
from sockets import sockets
from users import users
from multiprocessing import Process
pathProcessCSV = "/home/ramos/Escritorio/TFG/TFG/data/process.csv" #output
pathActivityTrackCSV = "/home/ramos/Escritorio/TFG/TFG/data/activitytrack.csv" #output
pathFilesCSV = "/home/ramos/Escritorio/TFG/TFG/data/files.csv" #output
pathFilesToWatch = '/home/ramos/Escritorio/tocar/activitywatch-master' #folder to be watched 
pathBrowsersCSV = "/home/ramos/Escritorio/TFG/TFG/data/Browsers.csv"
pathNetworksCSV = "/home/ramos/Escritorio/TFG/TFG/data/Network.csv"
pathSockets="/home/ramos/Escritorio/TFG/TFG/data/Sockets.csv"
pathUsers="/home/ramos/Escritorio/TFG/TFG/data/Users.csv"

p1 = Process(target=process, args=(pathProcessCSV,))
p1.start()
p2 = Process(target=activitytrack, args=(pathActivityTrackCSV,))
p2.start()
p3 = Process(target=files, args=(pathFilesCSV,pathFilesToWatch,))
p3.start()
p4 = Process(target=browsers, args=(pathBrowsersCSV,))
p4.start()
p5 = Process(target=network, args=(pathNetworksCSV,))
p5.start()
p6 = Process(target=sockets, args=(pathSockets,))
p6.start()
p7 = Process(target=users, args=(pathUsers,))
p7.start()