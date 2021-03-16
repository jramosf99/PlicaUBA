import psutil
from datetime import datetime
import pandas as pd
import time
import os
import warnings
warnings.filterwarnings("ignore")#para evitar warning de pandas que no influye

outputPath = "/home/ramos/Escritorio/TFG/process/data/data.csv" #path of the CSV output file
outputPath1 = "/home/ramos/Escritorio/TFG/process/data/data1.csv" #path of the CSV output file

outputPath2 = "/home/ramos/Escritorio/TFG/process/data/data2.csv" #path of the CSV output file

def get_users_info():
    # the list the contain all process dictionaries
    users = []
    for user in psutil.users():
        name = user.name
        time = datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
        users.append({'name': name, 'time': time,})
    df = pd.DataFrame(users)
    df.to_csv(outputPath2, index=None)
    

def get_processes_info():
    # the list the contain all process dictionaries
    processes = []
    for process in psutil.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid
            if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                continue
            # get the name of the file executed
            name = process.name()
            # get the time the process was spawned
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())
            try:
                # get the number of CPU cores that can execute this process
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            # get the CPU usage percentage
            cpu_usage = process.cpu_percent()
            # get the status of the process (running, idle, etc.)
            status = process.status()
            try:
                # get the process priority (a lower value means a more prioritized process)
                nice = int(process.nice())
            except psutil.AccessDenied:
                nice = 0
            try:
                # get the memory usage in bytes
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            # get the number of total threads spawned by this process
            n_threads = process.num_threads()
            # get the username of user spawned the process
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"
            
        processes.append({
            'pid': pid, 'name': str(name), 'create_time': create_time,
            'cores': int(cores), 'cpu_usage': float(cpu_usage), 'status': str(status), 'nice': int(nice),
            'memory_usage': float(memory_usage), 'n_threads': int(n_threads), 'username': str(username),
        })
    df = pd.DataFrame(processes)
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    return df



procesos_viejos = get_processes_info()
while True:
    time.sleep(1)
    procesos = get_processes_info()
    n_terminados = set(procesos_viejos['pid']) - set(procesos['pid'])
    if len(n_terminados)>0:
        procesos_terminados = procesos_viejos[procesos_viejos.pid.isin(n_terminados)]
        procesos_terminados = procesos_terminados.assign(FinishTime=datetime.now())
        if not os.path.isfile(outputPath):
            procesos_terminados.to_csv(outputPath, index=None, header=True)
        else:
            procesos_terminados.to_csv(outputPath, index=None, mode='a', header=False)
    #este bucle se encarga de por cada iteración quedarse con el valor máximo de cpu y memoria
    for i in procesos.index: 
        procces_viejo = procesos_viejos[(procesos_viejos['pid']== procesos["pid"][i])]
        if len(procces_viejo)>0:
            cpu_max = max(float(procces_viejo['cpu_usage']), procesos["cpu_usage"][i])
            memory_max = max(float(procces_viejo['memory_usage']), procesos["memory_usage"][i])
            procesos["cpu_usage"][i]= cpu_max
            procesos["memory_usage"][i]= memory_max
    procesos_viejos=procesos