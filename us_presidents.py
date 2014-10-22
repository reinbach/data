#!/usr/bin/env python
# Gather and display data about US Presidents, stock market (S&P 500) and jobs
import pytz
import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime

US_SITE = "https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States"
START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()


def get_date(col):
    date = col.find('span', {'class': 'date'})
    try:
        if date is None:
            col.span.extract()
            col.a.extract()
            date = col.get_text()
        else:
            date = str(date.string)
        date = datetime.strptime(date.strip(), "%B %d, %Y")
    except AttributeError:
        pass
    return date


def scrape_list(site):
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
                presidents.append({"president": president,
                                   "start": start_office, "end": end_office})
    return presidents


if __name__ == "__main__":
    presidents = scrape_list(US_SITE)
    for p in presidents:
        print(p["president"], "::", p["start"], "::", p["end"])
