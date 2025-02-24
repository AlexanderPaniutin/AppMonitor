# Monitoring foreground programs

import os
import signal
import win32gui
'''
import pandas as pd
import numpy as np
'''
import time
import threading
from datetime import date, timedelta


class AppMonitorService:
  '''
  Current service is watching what application
  is in foreground and for how long.
  The report is written into the file specified
  in the report_path. If None, the report will be
  in the same directory as the current scritp.
  '''

  def __init__(self, report_path=None):
    self.report_path = report_path
    self.keep_running = False
    # self.run_thread = threading.Thread(target=self._run)
    self.check_delay = 1  # check every second
    self.store_delay = 60 # store every minute
    
    # the main report holder as app_name : usage_secs.
    self.report = {}
  
  
  def start(self):
    '''
    Starts the monitoring service.
    '''
    
    self.keep_running = True
    # self.run_thread.start()
  
  
  def stop(self):
    '''
    Stops the monitoring service.
    '''
    self.keep_running = False
    # self.run_thread.join()
  
  
  def print_report(self):
    '''
    Prints the current report to stdout
    '''
    
    for app_name in self.report.keys():
      print("-" * 80)
      print("App Time")
      print("%20s %5d" % (app_name, self.report[app_name]))
    

  def run(self):
    fallback_cnt = 60
    
    last_report_time = time.time()
    report_period_sec = 5
    while self.keep_running:
      
      self._register_app()
      time.sleep(self.check_delay)
      
      if time.time() - last_report_time > report_period_sec:
        self.print_report()
        last_report_time = time.time()

      if fallback_cnt <= 0:
        break
        
      fallback_cnt -= 1

  def _load_report(self):
    '''
    Tries to load the report from today.
    '''
    pass
    
  def _store_report(self):
    '''
    Generates and stores a report
    '''
    pass
  
  def _register_app(self):
    app_name = self._get_fg_app_name()
    if app_name is None:
      return
     
    old_time = self.report.get(app_name, 0)
    self.report[app_name] = old_time + 1
    
  def _get_fg_app_name(self):
    '''
    Returns a current foreground application window name unparsed.
    '''
    w = win32gui
    title = w.GetWindowText(w.GetForegroundWindow())
  
    if title == '':
        return None
    app_name = title.split(' - ')[-1]
    return app_name
    
  
def date_():
    return f'{date.today().strftime("%Y%m%d")}'


def handler(signum, frame):
    print("Handling interrupt ", signum)
    app_monitor_service.stop()
    
    '''
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
    '''


'''
DF = pd.core.frame.DataFrame
DATE = date_()
LOGFILE = f'logs/log_{date_()}.json'



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
                LOGFILE = os.getcwd().replace('\\', '/') + '/logs/log_' +date_()+'.json'
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
'''

def main():
    print("Hello AppMonitorService!")
    # Add exit handler 
    signal.signal(signal.SIGINT, handler)

    app_monitor_service.start()
    app_monitor_service.run()
    print("Bye!!!!!")


if __name__=="__main__":
    main()