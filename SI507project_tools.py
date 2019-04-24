from bs4 import BeautifulSoup
import requests, json, csv, re, random
from advanced_expiry_caching import Cache
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

FILENAME = "dogs_cache.json"
program_cache = Cache(FILENAME)

url = "https://www.petwave.com/Dogs/Breeds.aspx"
data = requests.get(url).text
soup = BeautifulSoup(data,features="html.parser")
# print(soup.prettify()) # nice for investigation

all_urls = soup.findAll('div', attrs={'class': 'pw-rid-small-headline'})
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

try:
    cache_file = open(FILENAME, 'r')
    cache_contents = cache_file.read()
    cache_diction = json.loads(cache_contents)
    cache_file.close()
except:
    cache_diction = {}

names_list = []
description_list = []

fact1_list = []
fact2_list = []
fact3_list = []

# print(len(url_data)) #93285
# print(len(cache_diction)) #194


for item in cache_diction:
    # print(cache_diction[item]["item"])
    url_data = cache_diction[item]["values"]
    soup = BeautifulSoup(url_data,features="html.parser")

    titles = soup.find_all("title")
    for item in titles:
        x = item.text.replace("\n", "").replace("\r", "").replace("\t", "")
        new_x = re.split("\|", x)
        names_list.append(new_x[0])
        # names_list.append(x)
    # print(names_list)

    info = soup.find("div", {"class": "pw-main-content-text"})
    list_p = []
    p = info.findChild("p")
    list_p.append(p)
    for item in list_p:
        y = item
        if not y:
            description_list.append("Not Available")
        else:
            description_list.append(y.text)
    # print(description_list)

    fact1 = soup.find("p", {"id": "htmlbody_3_centercontent_7_rptRelated_description_0"})
    for item in fact1:
        z = item
        # print(item)
        fact1_list.append(z.replace("\n", "").replace("\r", "").replace("\t", "").strip())
        # if not z:
        #     fact1_list.append("na")
        # else:
        #     fact1_list.append(item)

    fact2 = soup.find("p", {"id": "htmlbody_3_centercontent_7_rptRelated_description_1"})
    for item in fact2:
        k = item
        fact2_list.append(k.replace("\n", "").replace("\r", "").replace("\t", "").strip())
        # if not k:
        #     fact2_list.append("na")
        # else:
        #     fact2_list.append(item)

    fact3 = soup.find("p", {"id": "htmlbody_3_centercontent_7_rptRelated_description_2"})
    for item in fact3:
        h = item
        fact3_list.append(h.replace("\n", "").replace("\r", "").replace("\t", "").strip())
        # if not h:
        #     fact3_list.append("na")
        # else:
        #     fact3_list.append(item)

rows = zip(names_list, description_list, fact1_list, fact2_list, fact3_list)

with open("dogs_info.csv", 'w', newline='', encoding = "utf8") as csvfile:
    samplecsvwriter = csv.writer(csvfile, delimiter=",",quotechar='"', quoting=csv.QUOTE_ALL)
    samplecsvwriter.writerow(["Name", "Description", "Fun Fact 1", "Fun Fact 2", "Fun Fact 3"])

    for row in rows:
        samplecsvwriter.writerow(row)
    csvfile.close()


with open("dogs_info.csv", 'r', encoding='utf-8') as parkcsv:
    reader = csv.reader(parkcsv)
    data = []
    for data_info in reader:
        data.append(data_info)
    parkcsv.close()


app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'dafhsoi3453fdsfaddfsdf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./dogs.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

class Fact(db.Model):
    __tablename__ = "facts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    fun_fact_1 = db.Column(db.String(3000))
    fun_fact_2 = db.Column(db.String(3000))
    fun_fact_3 = db.Column(db.String(3000))

    breeds = db.relationship('Breed', backref='Fact')

    def __repr__(self):
        return "{} (ID: {})".format(self.fun_fact_1, self.id)


class Breed(db.Model):
    __tablename__ = "breeds"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    overview = db.Column(db.String(5000))
    fact_id = db.Column(db.Integer, db.ForeignKey("facts.id"))

    def __repr__(self):
        return "{} | fact_id: {}".format(self.name, self.fact_id)

db.drop_all()
db.create_all()
session.commit()

for row in data[1:]:
    breed_name = row[0]
    breed_overview = row[1]
    fact1 = row[2]
    fact2 = row[3]
    fact3 = row[4]
    table1 = Fact(name = breed_name, fun_fact_1 = fact1, fun_fact_2 = fact2, fun_fact_3 = fact3)
    session.add(table1)
    session.commit()
    table2 = Breed(name = breed_name, overview = breed_overview, fact_id = table1.id)
    session.add(table2)
    session.commit()

image_file = Image.open("static/puppies.jpg")
b_image_file = image_file.convert('1')
b_image_file.save('static/new_puppies.jpg')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/numbers')
def numbers():
    breeds = Breed.query.all()
    num_breeds = len(breeds)
    return render_template('numbers.html', num_breeds=num_breeds)

@app.route('/breedinfo')
def breeds():
    one_breed = []
    breeds = Breed.query.all()
    random.shuffle(breeds)
    for dog in breeds[:3]:
        newtup = (dog.name, dog.overview)
        one_breed.append(newtup)
    return render_template('breeds.html', dog_names=one_breed)

@app.route('/funfacts')
def facts():
    facts_fun = []
    facts_all = Fact.query.all()
    random.shuffle(facts_all)
    for fact in facts_all[:3]:
        newtup = (fact.name, fact.fun_fact_1, fact.fun_fact_2, fact.fun_fact_3)
        facts_fun.append(newtup)
    return render_template('facts.html', facts=facts_fun)


if __name__ == "__main__":
    app.run()
