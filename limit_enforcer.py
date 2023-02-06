# Read logs for today
from datetime import date
import sys
import json
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QApplication
# import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore

PATH = '' # Path where scripts are located, example - 'C:/Users/User/.../monitoring-script/'

GAMES_LIMIT_MINS: int = 1 * 60
PER_APP_LIMIT: int = 2 * 60

def format_func(x):
    '''
    Function changes seconds into hh:mm:ss format for matplotlib
    '''
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)

    # return "{:d}:{:02d}".format(hours, minutes)
    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def load_report(day):
    '''
    Tries to load the report from today.
    '''

    formatted_day = day.strftime("%Y%m%d")
    log_fpath = f'{PATH}logs/log_{formatted_day}.json'
    try:
        with open(log_fpath, 'r') as file:
            report = json.load(file)
        return report
    except Exception as ex:
        # TODO: Use logging to mark the next statement as an ERR.
        print('Failed to load the report for %s', formatted_day)
        # Pass exception along.
        raise ex

'''
def qt_window():
    # creating a pyqtgraph plot window
    window = pg.plot()
    window.setGeometry(100, 100, 600, 500)
    title = "App Using data for today"
    window.setWindowTitle(title)

    
'''


def main():
    # Load report for the current day.
    report = load_report(date.today())
    # Sort the report by time used.
    report = dict(sorted(report.items(), key=lambda x: x[1], reverse=True))
    # Sort report values
    print("Report loaded as %s", json.dumps(report, indent=2))

if __name__ == '__main__':
    main()

"""
LOGFILE = os.getcwd().replace('\\', '/') + '/logs/log_' +date_()+'.json'


def show_log(data):
    '''
    Shows log file for today
    '''
    data_to_show = data.copy()
    data_to_show['AppTime'] = data_to_show['AppTime'].apply(lambda x: str(timedelta(seconds=x)))
    print(data_to_show)


def read(logfile=LOGFILE):
    '''
    Takes file location and returns data from file
    '''
    try:
        data = pd.read_json(LOGFILE)
        return data
    except:
        print('There no log file for today')
        input('Press ENTER to quit')
        exit()


def main():

    '''
    print(LOGFILE)
    print(type(LOGFILE))
    data = read()
    show_log(data)
    input('Press ENTER to quit')
    '''


if __name__=="__main__":
    main()
"""
