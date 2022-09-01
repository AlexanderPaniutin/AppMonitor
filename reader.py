# Read logs for today
from datetime import date, timedelta
import sys
import json
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
"""
import pandas as pd
import os
"""

PATH = '' # Path where scripts are located, example - 'C:/Users/User/.../monitoring-script/'


def format_func(x):
    '''
    Function changes seconds into hh:mm:ss format for matplotlib
    '''
    hours = int(x//3600)
    minutes = int((x%3600)//60)
    seconds = int(x%60)

    #return "{:d}:{:02d}".format(hours, minutes)
    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def date_():
    '''
    Returns date in format yyyymmdd
    '''
    return f'{date.today().strftime("%Y%m%d")}'


def load_report():
    '''
    Tries to load the report from today.
    '''
    try:
        with open(f'{PATH}logs/log_{date_()}.json', 'r') as file:
            report = json.load(file)
        return report
    except:
        print('There no log file for today')
        exit()


def qt_window():
    # creating a pyqtgraph plot window
    window = pg.plot()
    window.setGeometry(100, 100, 600, 500)
    title = "App Using data for today"
    window.setWindowTitle(title)

    report = load_report()
    # Sort report values
    report = dict(sorted(report.items(), key=lambda x: x[1], reverse=True))
    yval = list(report.values())
    yval_copy = yval.copy()
    ylab = list(map(lambda x: format_func(x), yval_copy))
    
    xlab = list(report.keys())
    xval = list(range(1,len(xlab)+1))

    y_ticks = []
    for i, item in enumerate(ylab):
        y_ticks.append( (yval[i], item) )
    y_ticks = [y_ticks]

    x_ticks=[]
    for i, item in enumerate(xlab):
        x_ticks.append( (xval[i], item) )
    x_ticks = [x_ticks]

    bargraph = pg.BarGraphItem(x=xval, height=yval, width=0.5, brush='g')
    window.addItem(bargraph)
    ax = window.getAxis('bottom')
    ax.setTicks(x_ticks)

    ay = window.getAxis('left')
    ay.setTicks(y_ticks)
    window.showGrid(y=True)


def main():
    qt_window()
    
    # Start Qt event loop unless running in interactive mode or using
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()


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
