# Monitoring foreground programs


import os
import signal
import win32gui
import pandas as pd
import numpy as np
from time import sleep
from datetime import date, timedelta


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
    count_seconds = 0
    while True:
        # Save data every minute
        if count_seconds == 60:
            if DATE != date_:
                LOGFILE = f'logs/log_{date_()}.json'
            save_data(data)
            count_seconds = 0

        # Clean title
        title = get_clean_title(get_foreground())

        # Add app in list ore add time to that app if already in list
        if not data[data['AppName'] == title].index.empty:
            idx = data[data['AppName'] == title].index
            data.loc[idx, 'AppTime'] += 1
        else:
            data = data.append(pd.DataFrame([[title, 1]], columns=['AppName', 'AppTime']), ignore_index=True)

        # Show data in terminal
        data_to_show = data.copy()
        data_to_show['AppTime'] = data_to_show['AppTime'].apply(lambda x: str(timedelta(seconds=x)))
        print(data_to_show)

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
    # Add exit handler 
    signal.signal(signal.SIGINT, handler)

    data = load_data()
    apps_stopwatch(data)


if __name__=="__main__":
    main()