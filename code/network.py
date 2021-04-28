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
            'name': name, 'total_bytes_sent': bytes_sent, 'total_bytes_recv': bytes_recv, 'total_packets_sent':packets_sent, 'total_packets_recv':packets_recv, 
            'total_errin': errin,'total_errout': errout,'total_dropout': dropout})
    return interfaces

def network(path, q,b, t):

    outputPath = path #path of the CSV output file

    psutil.net_io_counters.cache_clear()
    previusinterfaces = get_interfaces_info()
    while True:
        interface = get_interfaces_info()
        for element in interface:
            for previusinterface in previusinterfaces:
                if previusinterface["name"]== element["name"]:
                    previuselement= previusinterface
            if previuselement is not None:
                element["eventType"]= 4
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pattern = "%Y-%m-%d %H:%M:%S"
                date = int(time.mktime(time.strptime(date_time, pattern)))
                element["date"]= date
                element["bytes_sent"]= element["total_bytes_sent"] - previuselement["total_bytes_sent"]
                element["bytes_recv"]= element["total_bytes_recv"] - previuselement["total_bytes_recv"]
                element["packets_sent"]= element["total_packets_sent"] - previuselement["total_packets_sent"]
                element["packets_recv"]= element["total_packets_recv"] - previuselement["total_packets_recv"]
                element["errin"]= element["total_errin"] - previuselement["total_errin"]
                element["errout"]= element["total_errout"] - previuselement["total_errout"]
                element["dropout"]= element["total_dropout"] - previuselement["total_dropout"]
                q.put(element)
            else:
                element["eventType"]= 4
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pattern = "%Y-%m-%d %H:%M:%S"
                date = int(time.mktime(time.strptime(date_time, pattern)))
                element["date"]= date
                element["bytes_sent"]= 0
                element["bytes_recv"]= 0
                element["packets_sent"]= 0
                element["packets_recv"]= 0
                element["errin"]= 0
                element["errout"]= 0
                element["dropout"]= 0
                q.put(element)
        if b:
            df = pd.DataFrame(interface)
            if not os.path.isfile(outputPath):
                df.to_csv(outputPath, index=None, header=True)
            else:
                df.to_csv(outputPath, index=None, mode='a', header=False)
        time.sleep(t)