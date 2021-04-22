import psutil
from datetime import datetime
import pandas as pd
import time
import os


def get_interfaces_info():
    interfaces = []
    net_io = psutil.net_io_counters(pernic=True, nowrap=True)
    interfaces_names = list(net_io.keys())
    for name in interfaces_names:
        interface = net_io[name]
        bytes_sent=interface.bytes_sent
        bytes_recv = interface.bytes_recv
        packets_sent= interface.packets_sent
        packets_recv= interface.packets_recv
        errin= interface.errin
        errout= interface.errout
        dropin= interface.dropin
        dropout= interface.dropout
        interfaces.append({
            'name': name, 'bytes_sent': bytes_sent, 'bytes_recv': bytes_recv, 'packets_sent':packets_sent, 'packets_recv':packets_recv, 
            'errin': errin,'errout': errout,'dropout': dropout})
    return interfaces

def network(path, q,b):

    outputPath = path #path of the CSV output file

    psutil.net_io_counters.cache_clear()

    while True:
        interface = get_interfaces_info()
        for element in interface:
            element["eventType"]= 4
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pattern = "%Y-%m-%d %H:%M:%S"
            date = int(time.mktime(time.strptime(date_time, pattern)))
            element["date"]= date
            q.put(element)
        if b:
            df = pd.DataFrame(interface)
            if not os.path.isfile(outputPath):
                df.to_csv(outputPath, index=None, header=True)
            else:
                df.to_csv(outputPath, index=None, mode='a', header=False)
        time.sleep(600)
