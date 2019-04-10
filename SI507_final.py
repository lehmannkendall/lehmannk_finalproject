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

url = "https://www.petwave.com/Dogs/Breeds.aspx"
data = requests.get(url).text
soup = BeautifulSoup(data,features="html.parser")
# print(soup.prettify()) # nice for investigation

all_urls = soup.findAll('div', attrs={'class': 'pw-breed-list-item'})
for url in all_urls:
    links = url.findAll('a')
    for a in links:
        new_url = "https://www.petwave.com" + a['href']
        #cache all the urls into a json file
        data = program_cache.get(new_url)
        # print(new_url)
        if not data:
            data = requests.get(new_url).text
            program_cache.set(new_url, data)

# try:
#     cache_file = open(FILENAME, 'r')
#     cache_contents = cache_file.read()
#     cache_diction = json.loads(cache_contents)
#     cache_file.close()
# except:
#     cache_diction = {}
#
# names_list = []
# description_list = []
#
# for item in cache_diction:
#     # print(cache_diction[item]["item"])
#     url_data = cache_diction[item]["values"]
#     soup = BeautifulSoup(url_data,features="html.parser")
#
#
#     #names of guides
#     list_h2 = soup.find("h2", {"class": "header"})
#     # list_h2 = head2.findChildren("h2")
#     for item in list_h2:
#         x = item.text
#         if not x:
#             names_list.append("na")
#         else:
#             names_list.append(x)
#     # print(names_list)
#
#     #descriptions
#     p = soup.find("div", {"class": "body-divider"})
#     for item in p:
#         y = item.text
#         if not y:
#             description_list.append("na")
#         else:
#             description_list.append(y)
#     print(description_list)
