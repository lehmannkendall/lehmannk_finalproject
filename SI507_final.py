from bs4 import BeautifulSoup
import requests
import json
import csv
from advanced_expiry_caching import Cache
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

FILENAME = "dogs_cache.json"
program_cache = Cache(FILENAME)

# url = "https://www.akc.org/dog-breeds/"
# url = "https://www.akc.org/dog-breeds/"

url = "http://www.animalplanet.com/breed-selector/dog-breeds/all-breeds-a-z.html"
data = requests.get(url).text
soup = BeautifulSoup(data,features="html.parser")
# print(soup.prettify()) # nice for investigation

all_urls = soup.findAll('section', attrs={'id': 'tabAtoZ'})
for url in all_urls:
    links = url.findAll('a')
    for a in links:
        new_url = a['href']
        #cache all the urls into a json file
        data = program_cache.get(new_url)
        print(new_url)
        if not data:
            data = requests.get(new_url).text
            program_cache.set(new_url, data)
