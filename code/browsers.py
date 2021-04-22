import datetime as datetime
import pandas as pd
from browser_history import get_history
import time
import warnings
import os

warnings.filterwarnings("ignore")#para evitar warning de pandas que no influye


def browsers(path, q, b):
    outputPath = path #path of the CSV output file
    p=pd.to_datetime(datetime.datetime.now()).tz_localize('CET')
    while True:
        outputs = get_history()
        his = outputs.histories
        df=pd.DataFrame(his, columns=["date", "url"])
        df = df[df.date > p]
        if(df.size>0):
            p= df.to_dict('records')
            for rec in p:
                rec["eventType"]= 2
                rec['date'] = rec['date'].to_pydatetime().strftime('%Y-%m-%d, %H:%M:%S')
                q.put(rec)
            if b :
                if not os.path.isfile(outputPath):
                    q.put(df)
                    df.to_csv(outputPath, index=None)
                else:
                    q.put(df)
                    df.to_csv(outputPath, index=None, mode='a', header=False)
            p=pd.to_datetime(datetime.datetime.now()).tz_localize('CET')
        time.sleep(10)