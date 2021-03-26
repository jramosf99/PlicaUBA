import psutil
from datetime import datetime
import pandas as pd
import time
import os

outputPath = "/home/ramos/Escritorio/TFG/network/data/data1.csv" #path of the CSV output file


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


psutil.net_io_counters.cache_clear()

while True:
    interfaces = pd.DataFrame(get_interfaces_info())
    interfaces.to_csv(outputPath, index=None)
    time.sleep(10)
