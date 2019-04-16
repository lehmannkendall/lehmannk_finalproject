from SI507project_tools import *
from bs4 import BeautifulSoup
import requests
import json
import csv
from advanced_expiry_caching import Cache
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import unittest
import re
import os


#1 I want to have one to check the length of the dogs_cache.json - should be 194 items
#4 I want to somehow test my flask routes

# class PartOne(unittest.TestCase):
#     def test_scrape_json(self):
#         self.json_file = open('dogs_cache.json', 'r')
#         self.row_reader = self.json_file.readlines()
#         self.assertTrue(len(self.row_reader[0]) is 194, "Testing to see if the json file has 194 items")
#         print(len(self.row_reader[0])
#         self.json_file.close()

class PartOne(unittest.TestCase):
    def test_scrape_json(self):
        exists = os.path.isfile('dogs_cache.json')
        self.assertTrue(exists)

    def test_csvFileExists(self):
        exists = os.path.isfile('dogs_info.csv')
        self.assertTrue(exists)

class PartTwo(unittest.TestCase):
    def test_num_json(self):
        json_file = open('dogs_cache.json', 'r', encoding = 'utf-8')
        row_reader = json_file.readline()
        json_file.close()
        self.assertTrue(len(row_reader), 194) 

class PartThree(unittest.TestCase):

    def test_csvHeaders(self):
        csv_file = open('dogs_info.csv', 'r', encoding='utf-8')
        row_reader = csv_file.readline()
        csv_file.close()
        self.assertEqual(row_reader, '"Name","Description","Fun Fact 1","Fun Fact 2","Fun Fact 3"\n')
    # def test_csv(self):
    #     self.csv_file = open('dogs_info.csv', 'r')
    #     self.row_reader = self.csv_file.readlines()
    #     self.assertTrue("Name" in self.row_reader[0].split(",")[0], "Testing that Name is the first header in the csv")
    #     self.assertTrue("Description" in self.row_reader[0].split(",")[1], "Testing that Description is the second header in the csv")
    #     self.assertTrue("Fun Fact 1" in self.row_reader[0].split(",")[2], "Testing that Fun Fact 1 is the third header in the csv")
    #     self.assertTrue("Fun Fact 2" in self.row_reader[0].split(",")[3], "Testing that Fun Fact 2 is the fourth header in the csv")
    #     self.assertTrue("Fun Fact 3" in self.row_reader[0].split(",")[4], "Testing that Fun Fact 3 is the fifth header in the csv")
    #     self.csv_file.close()

class PartFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///dogs.db')

    def test_db_breeds_exists(self):
        results = self.engine.dialect.has_table(self.engine, "breeds")
        self.assertTrue(results)

    def test_db_facts_exists(self):
        results = self.engine.dialect.has_table(self.engine, "facts")
        self.assertTrue(results)

# class PartFive(unittest.TestCase):
#     def test_

if __name__ == "__main__":
    unittest.main(verbosity=2)
