import datetime as datetime
import pandas as pd
from browser_history import get_history
import time
import warnings
import os
import logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
warnings.filterwarnings("ignore")#para evitar warning de pandas que no influye

logging.getLogger("browser_history").setLevel(logging.WARNING)

def browsers(path, q, b, t):
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
                rec['date'] = int(time.mktime(time.strptime(rec['date'].to_pydatetime().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))
                q.put(rec)
            if b :
                if not os.path.isfile(outputPath):
                    df.to_csv(outputPath, index=None)
                else:
                    df.to_csv(outputPath, index=None, mode='a', header=False)
            p=pd.to_datetime(datetime.datetime.now()).tz_localize('CET')
        time.sleep(t)