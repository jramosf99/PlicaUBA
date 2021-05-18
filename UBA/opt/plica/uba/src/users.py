import psutil
from datetime import datetime
import pandas as pd
import time
import os
import warnings


def getActualusers():
    actualusers = []
    # the list the contain all process dictionaries
    for user in psutil.users():
        repetido = False
        name = user.name
        date =int(time.mktime(time.strptime(datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))
        terminal = user.terminal
        host = user.host
        pid = user.pid
        if pid == None:
            pid = 0
        actualusers.append({'name': str(name), 'time': date, 'terminal': str(terminal), 'host': str(host), 'pid': int(pid), 'close': "active"})
    return actualusers

def users(path, q, b, t):

    outputPath = path

    changes = True
    users = pd.DataFrame(getActualusers())
    previusUsers = pd.DataFrame(getActualusers())
    p= users.to_dict('records')
    for rec in p:
        rec["eventType"]= 7
        q.put(rec)

    while True:
        actuales = pd.DataFrame(getActualusers())
        terminados =  set(previusUsers['pid']) -set(actuales['pid'])
        if len(terminados) > 0:
            changes = True
            users[users.pid.isin(terminados)] = users[users.pid.isin(terminados)].assign(close=int(time.mktime(time.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))))
            p = users[users.pid.isin(terminados)].to_dict('records')
            for rec in p:
                rec["eventType"]= 7
                q.put(rec)
            nuevos = set()
            terminados = set()
        nuevos = set(actuales['pid']) -set(previusUsers['pid'])
        if len(nuevos) > 0:
            changes = True
            users = users.append(actuales[actuales.pid.isin(nuevos)])
            p = actuales[actuales.pid.isin(nuevos)].to_dict('records')
            for rec in p:
                rec["eventType"]= 7
                q.put(rec)
            nuevos = set()
        if changes and b:
            users.to_csv(outputPath, index=None)
        previusUsers = actuales
        changes = False
        time.sleep(t)