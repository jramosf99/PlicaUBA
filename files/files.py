import inotify.adapters
import pandas as pd
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
outputPath = "/home/ramos/Escritorio/TFG/files/data/data.csv" #path of the CSV output file
columnsNames = ["path","file_name","actions"] #columns names of the CSV files

def _main():
    i = inotify.adapters.Inotify()
    i.add_watch('/home/ramos/Escritorio/tocar/activitywatch-master')
    for event in i.event_gen(yield_nones=False):
        print(event)
        (_, type_names, path, filename) = event    
        if any(elem in list  for elem in type_names):
            fileEvent = [path, filename, type_names]
            df1 = pd.DataFrame([fileEvent], columns = columnsNames)
            if not os.path.isfile(outputPath):
                df1.to_csv(outputPath, index=None, header=True)
            else:
                df1.to_csv(outputPath, index=None, mode='a', header=False)

if __name__ == '__main__':
    _main()

