import datetime as datetime
import pandas as pd
from browser_history import get_history
import time
import warnings

warnings.filterwarnings("ignore")#para evitar warning de pandas que no influye

outputPath = "/home/ramos/Escritorio/TFG/network/data/data2.csv" #path of the CSV output file

p=pd.to_datetime(datetime.datetime.now()).tz_localize('CET')
while True:
    outputs = get_history()
    his = outputs.histories
    df=pd.DataFrame(his, columns=["date", "url"])
    df = df[df.date > p]
    df.to_csv(outputPath, index=None)
    time.sleep(10)