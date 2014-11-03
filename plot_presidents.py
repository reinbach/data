# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd


def get_presidents(path):
    with pd.get_store(path) as store:
        return store["presidents"]


def plot_presidents(presidents):
    plt.plot(presidents["start"], [0 for i in range(len(presidents["start"]))])
    plt.ylabel("S&P 500")
    plt.xlabel("Presidents")
    plt.show()

if __name__ == "__main__":
    presidents = get_presidents("uspresidents.h5")
    plot_presidents(presidents)