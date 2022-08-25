from operator import index
from unicodedata import name
import matplotlib.pylab as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import os


PATH = '' # Path where scripts are located, example - 'C:/Users/User/.../monitoring-script/'
LAST_DAYS_SHOW = 30 # Number of last log files that will be used 
NUMBER_APPS = 12 # Number of top used programs that will be showed 


def all_log_data(file_names):
    """
    Get all data from all log files into one dataframe
    """
    data = pd.DataFrame([],columns=['AppName', 'AppTime'])
    for file in file_names:
        data = pd.concat([data, pd.read_json(f'{PATH}logs/{file}')])
    data = data.groupby(['AppName'])['AppTime'].apply(sum).reset_index()
    data = data.sort_values('AppTime', ignore_index=True, ascending=False)
    
    return data


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


def get_app_data(file_names, app_name):
    """
    Get all data about some app from log files using its name
    """

    result = pd.DataFrame([], columns=['AppDate', 'AppTime'])

    for file in file_names:
        data = pd.read_json(f'{PATH}logs/{file}')
        app_time = data[data['AppName'] == app_name]['AppTime']
        if app_time.empty:
            app_time = 0
        else:
            app_time = list(app_time)[0]

        app_date = file[4:]
        app_date = app_date[:-5]
        result = pd.concat([result,pd.DataFrame([[app_date, app_time]], columns=['AppDate', 'AppTime'])],
            ignore_index=True)

    return result
        



def show_app_graph(all_data, file_names):
    """
    Show plot label of some app usage 
    """
    all_data['AppTime'] = all_data['AppTime'].apply(lambda x: format_func(x, None))
    print(all_data)
    
    while True:
        ent = input('Enter app nomber (q - quit): ')
        if ent == 'q':
            exit()
        
        elif ent.isdigit() and int(ent) < len(all_data):
            app_name = all_data.loc[int(ent)]['AppName']
            app_data = get_app_data(file_names, app_name)
            print(app_data)

            # PLOTING
            f = plt.figure()
            ax = f.add_subplot(1,1,1)
            ax.plot(app_data['AppDate'], app_data['AppTime'])

            ax.yaxis.set_major_formatter(FuncFormatter(format_func))
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()

            exit()

        


def main():
    # Prepare the data that will be used  
    file_names = os.listdir(f'{PATH}logs/')
    file_names = file_names[:LAST_DAYS_SHOW]
    all_data = all_log_data(file_names)

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
            show_app_graph(all_data, file_names)
            exit()


if __name__=="__main__":
    main()
