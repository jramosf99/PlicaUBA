from process import process
from activitytrack import  activitytrack
# from files import files
from browsers import browsers
from network import network
from sockets import sockets
from users import users
from multiprocessing import Process
pathProcessCSV = r"C:\Users\jramo\Desktop\tfg\TFG\data\process.csv" #output
pathActivityTrackCSV = r"C:\Users\jramo\Desktop\tfg\TFG\data\activitytrack.csv" #output
pathFilesCSV = r"C:\Users\jramo\Desktop\tfg\TFG\data\files.csv" #output
pathFilesToWatch = r'C:\Users\jramo\Downloads\hadoop\hadoop-3.1.0' #folder to be watched 
pathBrowsersCSV = r"C:\Users\jramo\Desktop\tfg\TFG\data\Browsers.csv"
pathNetworksCSV =  r"C:\Users\jramo\Desktop\tfg\TFG\data\Network.csv"
pathSockets=r"C:\Users\jramo\Desktop\tfg\TFG\data\Sockets.csv"
pathUsers=r"C:\Users\jramo\Desktop\tfg\TFG\data\Users.csv"

# process(pathProcessCSV)
# p1 = Process(target=process, args=(pathProcessCSV,))
# p1.start()
# activitytrack(pathActivityTrackCSV)
# p2 = Process(target=activitytrack, args=(pathActivityTrackCSV,))
# p2.start()
# p3 = Process(target=files, args=(pathFilesCSV,pathFilesToWatch,))
# p3.start()
# browsers(pathBrowsersCSV)
# p4 = Process(target=browsers, args=(pathBrowsersCSV,))
# p4.start()
# network(pathNetworksCSV)
# p5 = Process(target=network, args=(pathNetworksCSV,))
# p5.start()
# sockets(pathSockets)
# p6 = Process(target=sockets, args=(pathSockets,))
# p6.start()
# users(pathUsers)
# p7 = Process(target=users, args=(pathUsers,))
# p7.start()