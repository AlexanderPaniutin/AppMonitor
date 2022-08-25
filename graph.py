from datetime import timedelta
import matplotlib.pylab as plt
from  matplotlib.axes import Axes 
import pandas as pd
import os


# Get one big dataframe from all log files
def get_all_data(files):
    result = pd.DataFrame([],columns=['AppName', 'AppTime'])
    for file in files:
        result = pd.concat([result, pd.read_json(f'logs/{file}')])
    result = result.groupby(['AppName'])['AppTime'].apply(sum).reset_index()
    result = result.sort_values('AppTime', ignore_index=True, ascending=True)
    
    result['AppTime'] = result['AppTime'].apply(lambda x: str(timedelta(seconds=x)))
    return result


def main():
    # Get all logs
    files = os.listdir('logs/')
    
    # Get last 30 days data
    files = files[-30:]

    all_data = get_all_data(files)
    
    # Show top 7 apps by time
    data_to_show = all_data[-7:]

    plt.bar(data_to_show['AppName'], data_to_show['AppTime'])
    plt.ylabel 
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    main()
