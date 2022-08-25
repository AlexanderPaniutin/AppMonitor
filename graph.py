from datetime import timedelta
import matplotlib.pylab as plt
from  matplotlib.axes import Axes 
from matplotlib.ticker import FuncFormatter, MultipleLocator
import pandas as pd
import os


# Get one big dataframe from all log files
def get_all_data(files):
    result = pd.DataFrame([],columns=['AppName', 'AppTime'])
    for file in files:
        result = pd.concat([result, pd.read_json(f'logs/{file}')])
    result = result.groupby(['AppName'])['AppTime'].apply(sum).reset_index()
    result = result.sort_values('AppTime', ignore_index=True, ascending=True)
    
    #result['AppTime'] = result['AppTime'].apply(lambda x: str(timedelta(seconds=x)))
    return result


def format_func(x, pos):
    hours = int(x//3600)
    minutes = int((x%3600)//60)
    seconds = int(x%60)

    #return "{:d}:{:02d}".format(hours, minutes)
    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def last_apps_graph(all_data, top_apps=7):
    # Show top 7 apps by time
    data_to_show = all_data[-top_apps:]

    f = plt.figure()
    ax = f.add_subplot(1,1,1)
    ax.bar(data_to_show['AppName'], data_to_show['AppTime'])

    ax.yaxis.set_major_formatter(FuncFormatter(format_func))
    # this locates y-ticks at the hours
    #ax.yaxis.set_major_locator(MultipleLocator(base=3600))
    # this ensures each bar has a 'date' label
    #ax.xaxis.set_major_locator(MultipleLocator(base=1))

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def show_app_graph(date):
    pass


def main():
    # Get all logs
    files = os.listdir('logs/')
    
    # Get last 30 days data
    files = files[-30:]

    all_data = get_all_data(files)

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
            ent = input('Enter date in format yyyymmdd: ')
            show_app_graph(ent)


if __name__=="__main__":
    main()
