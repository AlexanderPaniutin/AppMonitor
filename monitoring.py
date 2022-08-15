# Monitoring opened programs

from operator import index
import os
import signal
import win32gui
import pandas as pd
import numpy as np
from time import sleep
from datetime import date

def date_():
    return f'{date.today().strftime("%Y%m%d")}'

DF = pd.core.frame.DataFrame
DATE = date_()
LOGFILE = f'logs/log_{date_()}.json'


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


def get_foreground():
    w = win32gui
    return w.GetWindowText(w.GetForegroundWindow())


def get_clean_title(title):
    if title == '':
        return 'Nothing'
    lst = title.split(' - ')
    return lst[-1]


def apps_stopwatch(data={}):
    # data = {'app_name':*app_time*}
    
    count_seconds = 0
    while True:
        
        if count_seconds == 60:
            if DATE != date_:
                LOGFILE = f'logs/log_{date_()}.json'

            save_data(data)
            count_seconds = 0

        title = get_clean_title(get_foreground())

        if not data[data['AppName'] == title].index.empty:
            idx = data[data['AppName'] == title].index
            data.loc[idx, 'AppTime'] += 1
        else:
            data = data.append(pd.DataFrame([[title, 1]], columns=['AppName', 'AppTime']), ignore_index=True)
        
        # print log

        print(data)

        sleep(1)
        count_seconds += 1
        os.system('cls')


def load_data() -> DF:
    try:
        data = pd.read_json(LOGFILE)
    except:
        data = pd.DataFrame([],columns=['AppName', 'AppTime'])
    return data


def save_data(data: DF):
    data.to_json(LOGFILE, orient='records')


def main():
    # Add handler
    signal.signal(signal.SIGINT, handler)

    data = load_data()
    if data.empty:
        print('No data for today')

    apps_stopwatch(data)
        
    df = pd.DataFrame([['app1', 1], ['app2', 12]], columns=['AppName', 'AppTime'])
    #save_data(df)
    

if __name__=="__main__":
    main()