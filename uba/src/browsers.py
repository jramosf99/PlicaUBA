import datetime as datetime
import pandas as pd
from browser_history import get_history
import time
import warnings
import os
import logging.config

#To ignore the comments of browser_history
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
logging.getLogger("browser_history").setLevel(logging.WARNING)

#To ignore a pandas warning that doesn't affect
warnings.filterwarnings("ignore")


# exported main method
def browsers(path, q, b, t):
    outputPath = path #path of the CSV output file
    p=pd.to_datetime(datetime.datetime.now()).tz_localize('CET')
    
    while True:
        #Get all the URLs and just select the ones from the last period
        outputs = get_history()
        his = outputs.histories
        df=pd.DataFrame(his, columns=["date", "url"])
        df = df[df.date > p]
        #Only if have new URLs
        if(df.size>0):
            p= df.to_dict('records')
            for rec in p:
                rec["eventType"]= 2
                rec['date'] = int(time.mktime(time.strptime(rec['date'].to_pydatetime().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))
                q.put(rec)
            #Only if CSV option is active
            if b :
                if not os.path.isfile(outputPath):
                    df.to_csv(outputPath, index=None)
                else:
                    df.to_csv(outputPath, index=None, mode='a', header=False)
            p=pd.to_datetime(datetime.datetime.now()).tz_localize('CET')
        time.sleep(t)