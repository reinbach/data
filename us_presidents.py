#!/usr/bin/env python
# Gather and display data about US Presidents, stock market (S&P 500) and jobs
import pandas as pd
import pytz
import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime


US_SITE = "https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States"
START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()


def get_date(col):
    date = col.find('span', {'class': 'date'})
    if date is None:
        try:
            col.span.extract()
        except AttributeError:
            pass
        try:
            col.a.extract()
        except AttributeError:
            pass
        date = col.get_text()
    else:
        date = str(date.string)
    if date:
        date = datetime.strptime(date.strip(), "%B %d, %Y")
    return date


def scrape_list(site):
    print("Downloading President data...")
    presidents = list()
    hdr = {'User-Agent': 'Mozilla/5,0'}
    req = urllib.request.Request(site, headers=hdr)
    with urllib.request.urlopen(req) as page:
        soup = BeautifulSoup(page)
        table = soup.find('table', {'class': "wikitable"})
        for row in table.findAll("tr"):
            col = row.findAll("td")
            if len(col) > 4:
                president = str(col[1].findAll("a")[0].string)
                start_office = get_date(col[2])
                end_office = get_date(col[3])
                party = str(col[4].findAll("a")[0].string)
                presidents.append({"president": president,
                                   "start": start_office, "end": end_office,
                                   "party": party})
    return presidents


def store_HDF5(presidents, path):
    with pd.get_store(path) as store:
        pres_list = []
        start_list = []
        end_list = []
        party_list = []
        for data in presidents:
            pres_list.append(data["president"])
            start_list.append(data["start"])
            end_list.append(data["end"])
            party_list.append(data["party"])
        store["presidents"] = pd.DataFrame({"name": pres_list,
                                            "start": start_list,
                                            "end": end_list,
                                            "party": party_list})

def get_presidents():
    presidents = scrape_list(US_SITE)
    store_HDF5(presidents, 'uspresidents.h5')


if __name__ == "__main__":
    get_presidents()
