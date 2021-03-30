from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import time
from datetime import datetime, timedelta
import os

columnsNames = ["path","actions", "time"] #columns names of the CSV files

class MyHandler(FileSystemEventHandler):
    def __init__(self,outputPath):
        self.last_modified = datetime.now()
        self.outputPath = outputPath
 
    def on_any_event(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
            fileEvent = [event.src_path, event.event_type, datetime.now()]
            df1 = pd.DataFrame([fileEvent], columns = columnsNames)
            if not os.path.isfile(self.outputPath):
                df1.to_csv(self.outputPath, index=None, header=True)
            else:
                df1.to_csv(self.outputPath, index=None, mode='a', header=False)


def files_win(path1,path2):
    outputPath = path1
    event_handler = MyHandler(outputPath)
    observer = Observer()
    observer.schedule(event_handler, path=path2, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
