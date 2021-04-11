import inotify.adapters
import pandas as pd
from datetime import datetime
import os

#tyoes of actions
# 'IN_MOVED_TO' 
# "IN_CLOSE_NOWRITE"  
# "IN_DELETE"  
# 'IN_CREATE'  
# 'IN_MODIFY'  
# 'IN_ACCESS' 
# 'IN_CLOSE_WRITE'
# 'IN_OPEN' 
# 'IN_MOVED_FROM'

list = ['IN_MOVED_TO', "IN_DELETE" , 'IN_CREATE', 'IN_MODIFY', 'IN_CLOSE_WRITE','IN_MOVED_FROM']#actions to register
columnsNames = ["path","actions","time"] #columns names of the CSV files

def files(path1,path2, q, b):
    outputPath = path1#path of the CSV output file
    while True:
        i = inotify.adapters.Inotify()
        i.add_watch(path2)
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event    
            if any(elem in list  for elem in type_names):
                event = {"eventType": 3, "date":datetime.now().strftime('%Y-%m-%d, %H:%M:%S'),"path": os.path.join(path, filename), "type": type_names}
                q.put(event)
                if b:
                    fileEvent = [os.path.join(path, filename), type_names, datetime.now()]
                    df1 = pd.DataFrame([fileEvent], columns = columnsNames)
                    if not os.path.isfile(outputPath):
                        df1.to_csv(outputPath, index=None, header=True)
                    else:
                        df1.to_csv(outputPath, index=None, mode='a', header=False)



