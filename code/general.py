from process import process
from activitytrack import  activitytrack
from files import files
from browsers import browsers
from network import network
from sockets import sockets
from users import users
pathProcessCSV = "/home/ramos/Escritorio/TFG/data/process.csv" #output
pathActivityTrackCSV = "/home/ramos/Escritorio/TFG/data/activitytrack.csv" #output
pathFilesCSV = "/home/ramos/Escritorio/TFG/data/files.csv" #output
pathFilesToWatch = '/home/ramos/Escritorio/tocar/activitywatch-master' #folder to be watched 
pathBrowsersCSV = "/home/ramos/Escritorio/TFG/data/Browsers.csv"
pathNetworksCSV = "/home/ramos/Escritorio/TFG/data/Network.csv"
pathSockets="/home/ramos/Escritorio/TFG/data/Sockets.csv"
pathUsers="/home/ramos/Escritorio/TFG/data/Users.csv"
# process(pathProcessCSV)
# activitytrack(pathActivityTrackCSV)
# files(pathFilesCSV,pathFilesToWatch)
# browsers(pathBrowsersCSV)
# network(pathNetworksCSV)
# sockets(pathSockets)
users(pathUsers)