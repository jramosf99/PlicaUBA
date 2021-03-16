import psutil
from datetime import datetime
import pandas as pd
import time
import os

outputPath = "/home/ramos/Escritorio/TFG/network/data/data.csv" #path of the CSV output file


    

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
            'laddr':laddr, 'raddr':raddr,'status':status,'pid':pid})
    return sockets

def construct_dataframe(sockets):
    df = pd.DataFrame(sockets)
    return df

p = get_sockets_info()
df1 = construct_dataframe(p)
df1.to_csv(outputPath, index=None)

