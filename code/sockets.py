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
        status = socket.status
        pid = socket.pid
        sockets.append({
            'fd': fd, 'family': family, 'type': type,
            'laddr':laddr, 'raddr':raddr,'status':status,'pid':pid, 'detection_time': datetime.now(), 'close': "open"})
    return sockets


def sockets(path):

    outputPath = path #path of the CSV output file

    changes = True
    sockets = pd.DataFrame(get_sockets_info())
    previusSockets = pd.DataFrame(get_sockets_info())



    while True:
        actuales = pd.DataFrame(get_sockets_info())
        terminados =  set(previusSockets['laddr']) -set(actuales['laddr'])
        if len(terminados) > 0:
            changes = True
            sockets[sockets.laddr.isin(terminados)] = sockets[sockets.laddr.isin(terminados)].assign(close=datetime.now())
            terminados = set()
        nuevos = set(actuales['laddr']) -set(previusSockets['laddr'])
        if len(nuevos) > 0:
            changes = True
            sockets = sockets.append(actuales[actuales.laddr.isin(nuevos)])
            nuevos = set()
        if changes:
            sockets.to_csv(outputPath, index=None)
        previusSockets = actuales
        changes = False
        time.sleep(3)