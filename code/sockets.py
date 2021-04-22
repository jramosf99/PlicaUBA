import psutil
from datetime import datetime
import pandas as pd
import time
import os


def get_sockets_info():
    # the list the contain all process dictionaries
    sockets = []
    for socket in psutil.net_connections(kind='inet'):
        fd = socket.fd
        family = socket.family
        type = socket.type
        laddr = socket.laddr
        raddr = socket.raddr
        pid = socket.pid
        if pid == None:
            pid = 0
        sockets.append({
            'fd': fd, 'family': family, 'type': type,
            'laddr':laddr, 'raddr':raddr,'pid':pid, 'detection_time': datetime.now().strftime('%Y-%m-%d, %H:%M:%S'), 'closed_time': "open"})
    return sockets


def sockets(path, q, b):

    outputPath = path #path of the CSV output file

    sockets = pd.DataFrame(get_sockets_info())
    previusSockets = pd.DataFrame(get_sockets_info())



    while True:
        actuales = pd.DataFrame(get_sockets_info())
        terminados =  set(previusSockets['laddr']) -set(actuales['laddr'])
        if len(terminados) > 0:
            sockets[sockets.laddr.isin(terminados)] = sockets[sockets.laddr.isin(terminados)].assign(close=datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
            if b:
                if not os.path.isfile(outputPath):
                    sockets[sockets.laddr.isin(terminados)].to_csv(outputPath, index=None)
                else:
                    sockets[sockets.laddr.isin(terminados)].to_csv(outputPath, index=None, mode='a', header=False)
            p= sockets[sockets.laddr.isin(terminados)].to_dict('records')
            for rec in p:
                print("wnefoierngpi")
                rec["eventType"]= 6
                rec["laddrport"] = rec["laddr"][1]
                rec["laddr"] = rec["laddr"][0]
                rec["raddrport"] = rec["raddr"][1]
                rec["raddr"] = rec["raddr"][0]
                q.put(rec)
            terminados = set()
        nuevos = set(actuales['laddr']) -set(previusSockets['laddr'])
        if len(nuevos) > 0:
            sockets = sockets.append(actuales[actuales.laddr.isin(nuevos)])
            nuevos = set()
        previusSockets = actuales
        changes = False
        time.sleep(2)