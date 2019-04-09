from bs4 import BeautifulSoup
import requests
import json
import csv
from advanced_expiry_caching import Cache
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

FILENAME = "parks_cache.json"
program_cache = Cache(FILENAME)

url = "https://www.nps.gov/index.htm"
data = requests.get(url).text
soup = BeautifulSoup(data,features="html.parser")
# print(soup.prettify()) # nice for investigation

#get each url from the dropdown menu - each state
all_urls = soup.findAll('div', attrs={'class': 'SearchBar-keywordSearch input-group input-group-lg'})
for url in all_urls:
    links = url.findAll('a')
    for a in links:
        new_url = "https://www.nps.gov" + a['href']
        #cache all the urls into a json file
        data = program_cache.get(new_url)
        # print(new_url)
        if not data:
            data = requests.get(new_url).text
            program_cache.set(new_url, data)

try:
    cache_file = open(FILENAME, 'r')
    cache_contents = cache_file.read()
    cache_diction = json.loads(cache_contents)
    cache_file.close()
except:
    cache_diction = {}

# state_list = []
# print(state_list)
types_list = []
names_list = []
locations_list = []
paragraphs_list = []
num_list = []
# numbers_list = []

for item in cache_diction:
    # print(cache_diction[item]["item"])
    url_data = cache_diction[item]["values"]
    soup = BeautifulSoup(url_data,features="html.parser")


    #state
    # head1 = soup.findAll("h1", {"class": "page-title"})
    # for item in head1:
    #     k = item.text
    #     state_list.append(k)
    #     if not k:
    #         state_list.append("na")
    #     else:
    #         state_list.append(k)

    # num = soup.find("ul", {"class": "state_numbers"})
    # list_num = num.findChildren("li")
    # for item in list_num:
    #     x = item.text
    #     if "National Parks" in x:
    #         numbers_list.append(x)

    #types
    head2 = soup.find("ul", {"id": "list_parks"})
    list_h2 = head2.findChildren("h2")
    for item in list_h2:
        x = item.text
        if not x:
            types_list.append("na")
        else:
            types_list.append(x)
    # print (types_list)

    #names
    head3 = soup.find("ul", {"id": "list_parks"})
    list_h3 = head3.findChildren("h3")
    for item in list_h3:
        y = item.text
        if not y:
            names_list.append("na")
        else:
            names_list.append(y)
    # print(names_list)

    #locations
    head4 = soup.find("ul", {"id": "list_parks"})
    list_h4 = head4.findChildren("h4")
    for item in list_h4:
        z = item.text
        if not z:
            locations_list.append("na")
        else:
            locations_list.append(z)
    # print(locations_list)

    #paragraphs
    par = soup.find("ul", {"id": "list_parks"})
    list_p = par.findChildren("p")

    for item in list_p:
        p = item.text.replace("\n","",2)
        if not p:
            locations_list.append("na")
        else:
            paragraphs_list.append(p)
    # print(paragraphs_list)

# CSV File
rows = zip(names_list, types_list, locations_list, paragraphs_list)

with open("parks_info.csv", 'w', newline='', encoding = "utf8") as csvfile:
    samplecsvwriter = csv.writer(csvfile, delimiter=",",quotechar='"', quoting=csv.QUOTE_ALL)
    samplecsvwriter.writerow(["Name", "Type", "Location", "Description"])

    for row in rows:
        samplecsvwriter.writerow(row)
    csvfile.close()

with open("parks_info.csv", 'r', encoding='utf-8') as parkcsv:
    reader = csv.reader(parkcsv)
    data = []
    for data_info in reader:
        data.append(data_info)
    parkcsv.close()

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'dafhsoi3453fdsfaddfsdf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./parks.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

class Description(db.Model):
    __tablename__ = "descriptions"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(300))
    description = db.Column(db.String(3000))

    parks = db.relationship('Park', backref='Description')

    def __repr__(self):
        return "{} (ID: {})".format(self.type, self.id)


class Park(db.Model):
    __tablename__ = "parks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    location = db.Column(db.String(400))
    description_id = db.Column(db.Integer, db.ForeignKey("descriptions.id"))

    def __repr__(self):
        return "{} located in {} | description: {}".format(self.name, self.location, self.description_id)

db.create_all()

for row in data[1:]:
    park_name = row[0]
    park_location = row[2]
    park_type = row[1]
    park_description = row[3]
    example1 = Description(type = park_type, description = park_description)
    example2 = Park(name = park_name, location = park_location)
    session.add(example1)
    session.add(example2)
    session.commit()


# sqlite_file = "parks.db"
#
# conn = sqlite3.connect(sqlite_file)
# c = conn.cursor()
#
# c.execute('''CREATE TABLE IF NOT EXISTS Descriptions(Id INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT, Description TEXT)''')
#
# c.execute('''CREATE TABLE IF NOT EXISTS Parks(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name INTEGER, Location TEXT, DescriptionId INTEGER, FOREIGN KEY (DescriptionId) REFERENCES Descriptions(Id))''')
#
# conn.commit()




# c.executemany('INSERT INTO Descriptions(Type, Description) VALUES (?, ?)', parks_des_ls)
# conn.commit()
#
#
#
# #HAVE TO FIX DescriptionId
# c.executemany('INSERT INTO Parks(Name, Location, Description_id) VALUES (?, ?, (SELECT(Id) FROM Descriptions))', parks_ls)
# conn.commit()
#
# conn.close()


# @app.route('/')
# def number():
#     parks = Parks.query.all()
#     num_parks = len(parks)
#     return str(num_parks)

# @app.route('/')
# def welcome():
#     num = len(data)
#     return '<h1> {} national sites </h1>'.format(num)
#
#
#
# if __name__ == "__main__":
#     app.run()
