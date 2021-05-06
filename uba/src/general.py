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
import os
import sys
import time
import configparser


def write_json(data, filename):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

def read_config(param):
    config = configparser.ConfigParser()
    config.read(param)
    print(">> Configuracion: {}".format(param))
    conf = {}
    
    conf["pathFilesToWatch"] = config["watch_path"].get("pathFilesToWatch")

    conf["outputpathJSON"] = config["jsons_paths"].get("outputpathJSON").encode("utf-8")
    conf["pathProcessJSON"] = config["jsons_paths"].get("pathProcessJSON").encode("utf-8")
    conf["pathActivityTrackJSON"] = config["jsons_paths"].get("pathActivityTrackJSON").encode("utf-8")
    conf["pathFilesJSON"] = config["jsons_paths"].get("pathFilesJSON").encode("utf-8")
    conf["pathBrowsersJSON"] = config["jsons_paths"].get("pathBrowsersJSON").encode("utf-8")
    conf["pathNetworksJSON"] = config["jsons_paths"].get("pathNetworksJSON").encode("utf-8")
    conf["pathSocketsJSON"] = config["jsons_paths"].get("pathSocketsJSON").encode("utf-8")
    conf["pathUsersJSON"] = config["jsons_paths"].get("pathUsersJSON").encode("utf-8")

    conf["activityTrackTime"] = config["times"].getint("activityTrackTime")
    conf["browserTime"] = config["times"].getint("browserTime")
    conf["NetworkTime"] = config["times"].getint("NetworkTime")
    conf["ProcessTime"] = config["times"].getint("ProcessTime")
    conf["SocketsTime"] = config["times"].getint("SocketsTime")
    conf["UsersTime"] = config["times"].getint("UsersTime")

    conf["activitytrackBoolean"] = config["booleans"].getboolean("activitytrackBoolean")
    conf["browsersBoolean"] = config["booleans"].getboolean("browsersBoolean")
    conf["filesBoolean"] = config["booleans"].getboolean("filesBoolean")
    conf["networkBoolean"] = config["booleans"].getboolean("networkBoolean")
    conf["processBoolean"] = config["booleans"].getboolean("processBoolean")
    conf["socketsBoolean"] = config["booleans"].getboolean("socketsBoolean")
    conf["usersBoolean"] = config["booleans"].getboolean("usersBoolean")

    conf["pathProcessCSV"] = config["csvs_paths"].get("pathProcessCSV")
    conf["pathActivityTrackCSV"] = config["csvs_paths"].get("pathActivityTrackCSV")
    conf["pathFilesCSV"] = config["csvs_paths"].get("pathFilesCSV")
    conf["pathBrowsersCSV"] = config["csvs_paths"].get("pathBrowsersCSV")
    conf["pathNetworksCSV"] = config["csvs_paths"].get("pathNetworksCSV")
    conf["pathSocketsCSV"] = config["csvs_paths"].get("pathSocketsCSV")
    conf["pathUsersCSV"] = config["csvs_paths"].get("pathUsersCSV")

    conf["metadata"] = {}
    conf["metadata"]["version"] = config["metadata"].get("version")
    conf["metadata"]["id"] = config["metadata"].get("id")
    conf["metadata"]["event"] = config["metadata"].get("event")
    conf["type"] = ["",config["metadata"].get("type1"),config["metadata"].get("type2"),config["metadata"].get("type3"),config["metadata"].get("type4"),config["metadata"].get("type5"),config["metadata"].get("type6"),config["metadata"].get("type7")]
    return conf



conf = read_config(sys.argv[1])

jsons = [conf["outputpathJSON"],conf["pathActivityTrackJSON"],conf["pathBrowsersJSON"],conf["pathFilesJSON"],conf["pathNetworksJSON"],conf["pathProcessJSON"],conf["pathSocketsJSON"],conf["pathUsersJSON"]]




if __name__ == '__main__': 
    conf = read_config(sys.argv[1])

    jsons = [conf["outputpathJSON"],conf["pathActivityTrackJSON"],conf["pathBrowsersJSON"],conf["pathFilesJSON"],conf["pathNetworksJSON"],conf["pathProcessJSON"],conf["pathSocketsJSON"],conf["pathUsersJSON"]]
 
    q = queue.Queue()
    t1= threading.Thread(target=activitytrack, args=(conf["pathActivityTrackCSV"],q,conf["activitytrackBoolean"], conf["activityTrackTime"]))
    t2 = threading.Thread(target=browsers, args=(conf["pathBrowsersCSV"],q,conf["browsersBoolean"], conf["browserTime"]))
    t3 = threading.Thread(target=files_win, args=(conf["pathFilesCSV"],conf["pathFilesToWatch"],q,conf["filesBoolean"]))
    t4 = threading.Thread(target=network, args=(conf["pathNetworksCSV"],q,conf["networkBoolean"],conf["NetworkTime"]))
    t5 = threading.Thread(target=process, args=(conf["pathProcessCSV"],q, conf["processBoolean"], conf["ProcessTime"]))
    t6 = threading.Thread(target=sockets, args=(conf["pathSocketsCSV"],q,conf["socketsBoolean"], conf["SocketsTime"]))
    t7 = threading.Thread(target=users, args=(conf["pathUsersCSV"],q,conf["usersBoolean"], conf["UsersTime"]))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()

    try:
        while True:
            time.sleep(1)
            element= q.get()
            head, tail = os.path.split(jsons[element["eventType"]])
            if not os.path.isdir(head):
                os.mkdir(head)
            if not os.path.isfile(jsons[element["eventType"]]):
                data = {}
                data['data'] = []
                with open(jsons[element["eventType"]], 'w') as file:
                    json.dump(data, file, indent=4)
            with open(jsons[element["eventType"]]) as json_file:
                data = json.load(json_file)
                temp = data['data']
                temp.append(element)
                print(element)     
            write_json(data,jsons[element["eventType"]]) 
    except KeyboardInterrupt:
        print("programa terminado")





