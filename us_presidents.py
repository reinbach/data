#!/usr/bin/env python
# Gather and display data about US Presidents, stock market (S&P 500) and jobs
import urllib
import pandas as pd
import pytz

from bs4 import BeautifulSoup
from datetime import datetime
from pandas.io.data import DataReader


US_SITE = "https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States"
START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()

def scrape_list(site):
    hdr = {'User-Agent': 'Mozilla/5,0'}
    req = urllib.request.Request(site, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page)

    table = soup.find('table', {'class': "wikitable"})
    presidents = list()
    for row in table.findAll("tr"):
        col = row.findAll("td")
        if len(col) > 4:
            president = str(col[1].findAll("a")[0].string)
            start_office = str(col[2].find('span', {'class': 'date'}).string)
            end_office = str(col[3])
            presidents.append({"president": president,
                               "start": start_office, "end": end_office})
    return presidents


if __name__ == "__main__":
    presidents = scrape_list(US_SITE)
    for p in presidents:
        print(p["president"], p["start"])
