# -*- coding: utf-8 -*-
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def get_presidents(path):
    with pd.get_store(path) as store:
        return store["presidents"]


def plot_presidents(presidents):
    x_labels = [i.strftime("%Y-%m-%d") for i in presidents["start"]]
    x = [mdates.date2num(i) for i in presidents["start"]]
    y = [i for i in range(len(presidents["start"]))]
    plt.plot(x, y)
    plt.ylabel("S&P 500")
    plt.xlabel("Presidents")
    plt.gca().set_xticks(x)
    plt.gca().set_xticklabels(x_labels, rotation=45, ha="right")
    plt.show()

if __name__ == "__main__":
    presidents = get_presidents("uspresidents.h5")
    plot_presidents(presidents)