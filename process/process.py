import psutil
from datetime import datetime
import pandas as pd
import time
import os

outputPath = "/home/ramos/Escritorio/TFG/process/data/data.csv" #path of the CSV output file
outputPath2 = "/home/ramos/Escritorio/TFG/process/data/data1.csv" #path of the CSV output file

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
            'pid': pid, 'name': name, 'create_time': create_time,
            'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
            'memory_usage': memory_usage, 'n_threads': n_threads, 'username': username,
        })

    return processes

def construct_dataframe(processes):
    df = pd.DataFrame(processes)
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    return df

p = get_processes_info()
df1 = construct_dataframe(p)
df1.to_csv(outputPath, index=None)
get_users_info()