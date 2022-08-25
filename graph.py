import matplotlib.pylab as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import os


PATH = '' # Path where scripts are located, example - 'C:/Users/User/.../monitoring-script/'
LAST_DAYS_SHOW = 30 # Number of last log files that will be used 
NUMBER_APPS = 7 # Number of top used programs that will be showed 


def all_log_data(files):
    """
    Get all data from all log files into one dataframe
    """
    data = pd.DataFrame([],columns=['AppName', 'AppTime'])
    for file in files:
        data = pd.concat([data, pd.read_json(f'{PATH}logs/{file}')])
    data = data.groupby(['AppName'])['AppTime'].apply(sum).reset_index()
    data = data.sort_values('AppTime', ignore_index=True, ascending=False)
    
    return data


def get_app_data(files):
    pass


def format_func(x, pos):
    '''
    Function changes seconds into hh:mm:ss format for matplotlib
    '''
    hours = int(x//3600)
    minutes = int((x%3600)//60)
    seconds = int(x%60)

    #return "{:d}:{:02d}".format(hours, minutes)
    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def last_apps_graph(all_data):
    """
    Show plot label of most frequently used apps
    """
    data_to_show = all_data[:NUMBER_APPS]

    f = plt.figure()
    ax = f.add_subplot(1,1,1)
    ax.bar(data_to_show['AppName'], data_to_show['AppTime'])

    ax.yaxis.set_major_formatter(FuncFormatter(format_func))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def show_app_graph(all_data):
    """
    Show plot label of some app usage 
    """
    pass


def main():
    # Prepare the data that will be used  
    files = os.listdir(f'{PATH}logs/')
    files = files[:LAST_DAYS_SHOW]
    all_data = all_log_data(files)

    # Terminal UI
    while True:
        print('[1] - Show graph with most using apps')
        print('[2] - Show graph of one app')
        print('[q] - quit')
        ent = input('>>> ')

        if ent == 'q':
            exit()
        
        elif ent == '1':
            last_apps_graph(all_data)
            exit()
        
        elif ent == '2':
            show_app_graph(all_data)
            exit()


if __name__=="__main__":
    main()
