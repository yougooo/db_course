import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


def make_series(data,index):
    return pd.Series(data,index=index)

def make_plots(series_data):
    plt.figure(figsize=(20,8))
    plt.legend(['p1','p2','p3','p4'],fontsize=20)
    for plot in series_data:
        plot.plot()
    plt.legend(['p1','p2','p3','p4'],fontsize=20)
    plt.savefig('db_lab/static/image/new.png', bbox_inches='tight')
