#!/usr/bin/python2
import csv
import os
import sys

from bs4 import BeautifulSoup
try:
    import http.client as httplib
except ImportError:
    import httplib

class Brick:
    def __init__(self, partno, color, desc, image_url):
        # A unique identification of this part.
        self.uid = partno + '-' + color.upper()

        # LEGO's identifier for this class of part.
        self.partno = partno

        # The specific color of the part.
        self.color = color

        # A description of the part.
        self.description = desc

        # An optional URL with a part image.
        self.image_url = image_url

    @classmethod
    def from_csv(cls, row):
        bricksetid = int(row[0])
        img = "http://cache.lego.com/media/bricks/5/1/{}.jpg".format(bricksetid)
        return Brick(
            int(row[4]), # partno
            row[2],      # color
            row[5],      # desc
            img)

    def __str__(self):
        return "{}:{}/{}".format(self.partno, self.description, self.color)

def get_bricklist_brickset(setno):
    """
    Set number should be in a form like: 8460-1
    """
    # Grab the URL like:
    #   http://www.brickset.com/export/inventory/?Set=8460-1
    conn = httplib.HTTPConnection('www.brickset.com')
    conn.connect()
    conn.request('GET', '/export/inventory/?Set=' + setno)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()

    # Parse as csv
    csvreader = csv.reader(data.split())
    next(csvreader) # skip header
    part_list = [(int(row[1]), Brick.from_csv(row)) for row in csvreader]
    return part_list

def get_bricklist_peeron(setno):
    """
    Set number should be in a form like: 8460-1
    """
    # Grab the URL like:
    #   http://peeron.com/inv/sets/8210-1
    conn = httplib.HTTPConnection('peeron.com')
    conn.connect()
    conn.request('GET', '/inv/sets/' + setno)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()

    # Parse as html
    part_list = []
    soup = BeautifulSoup(data)
    for tbl in soup.find_all('table'):
        if tbl.th is not None:
            for tr in tbl.find_all('tr'):
                tds = [td for td in tr.find_all('td')]
                if not tds:
                    continue
                cnt = tds[0].get_text()
                partno = tds[1].get_text()
                color = tds[2].get_text()
                desc = tds[3].get_text()
                try:
                    img = tds[4].a.img.get('src')
                except AttributeError:
                    img = '' # sticker sheets mostly
                part_list.append((int(cnt), Brick(partno, color, desc, img)))
    return part_list

def main():
    part_list = get_bricklist_peeron('8872-1')
    for cnt, part in part_list:
        print("{}-{}".format(cnt, part))
    return 0

if __name__ == '__main__':
    sys.exit(main())
