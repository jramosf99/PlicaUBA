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
        time = datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
        terminal = user.terminal
        host = user.host
        pid = user.pid
        actualusers.append({'name': str(name), 'time': str(time), 'terminal': str(terminal), 'host': str(host), 'pid': pid, 'close': "active"})
    return actualusers

def users(path):

    outputPath = path

    changes = True
    users = pd.DataFrame(getActualusers())
    previusUsers = pd.DataFrame(getActualusers())

    while True:
        actuales = pd.DataFrame(getActualusers())
        terminados =  set(previusUsers['pid']) -set(actuales['pid'])
        if len(terminados) > 0:
            changes = True
            users[users.pid.isin(terminados)] = users[users.pid.isin(terminados)].assign(close=datetime.now())
            terminados = set()
        nuevos = set(actuales['pid']) -set(previusUsers['pid'])
        if len(nuevos) > 0:
            changes = True
            users = users.append(actuales[actuales.pid.isin(nuevos)])
            nuevos = set()
        if changes:
            users.to_csv(outputPath, index=None)
        previusUsers = actuales
        changes = False
        time.sleep(5)
