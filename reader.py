# Read logs for today

import pandas as pd
from datetime import date, timedelta


def date_():
    '''
    Returns date in format yyyymmdd
    '''
    return f'{date.today().strftime("%Y%m%d")}'


LOGFILE = f'logs/log_{date_()}.json'


def show_log(data):
    '''
    Shows log file for today
    '''
    data_to_show = data.copy()
    data_to_show['AppTime'] = data_to_show['AppTime'].apply(lambda x: str(timedelta(seconds=x)))
    print(data_to_show)


def read(logfile=LOGFILE):
    '''
    Takes file lokation and returns data from file
    '''
    try:
        data = pd.read_json(LOGFILE)
        return data
    except:
        print('There no log file for today')
        exit()


def main():
    data = read()
    show_log(data)


if __name__=="__main__":
    main()
