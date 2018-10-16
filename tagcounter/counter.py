from tagcounter.page import Page
from tagcounter.parser import MyParser
from tagcounter.logs import write_to_logs
from datetime import datetime
import sqlite3
import pickle
import yaml
from collections import OrderedDict

def count_tags(domain_name):
    url = "http://"+domain_name
    page = Page(url)
    if page.status_code == 200:
        data = page.get_data()
        parser = MyParser()
        parser.feed(data)
        write_to_logs(domain_name)
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        return {"domain_name": domain_name,
                "url": page.url,
                "date": date,
                "tagdict": parser.tagdict}
    else:
        return None

def upload_to_db(domain_name, url, date, tagdict):
    def pickle_tagdict(tagdict):
        pickled_tagdict = pickle.dumps(tagdict, 2)
        return pickled_tagdict
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS tags (name text, url text, date text, tagdict text)"
    cursor.execute(create_table)
    query = "SELECT * FROM tags WHERE name=?"
    result = cursor.execute(query, (domain_name,))
    row = result.fetchone()
    if row is None:
        query = "INSERT INTO tags VALUES (?, ?, ?, ?)"
        pickled_tagdict = pickle_tagdict(tagdict)
        cursor.execute(query, (domain_name, url, date, pickled_tagdict))
    else:
        query = "UPDATE tags SET url=?, date=?, tagdict=? WHERE name=?"
        pickled_tagdict = pickle_tagdict(tagdict)
        cursor.execute(query, (url, date, pickled_tagdict, domain_name))
    connection.commit()
    connection.close()

def retrieve_by_name(domain_name):
    def unpickle_tagdict(tagdict):
        unpickled_tagdict = pickle.loads(tagdict)
        return unpickled_tagdict
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS tags (name text, url text, date text, tagdict text)"
    cursor.execute(create_table)
    query = "SELECT * FROM tags WHERE name=?"
    result = cursor.execute(query, (domain_name,))
    row = result.fetchone()
    if row is not None:
        unpickled_dict = unpickle_tagdict(row[3])
        return {"domain_name": row[0],
                "url": row[1],
                "date": row[2],
                "tagdict": unpickled_dict}
    else:
        return None

def get_alias_dict():
    alias_dict = {}
    try:
        with open("aliases.yaml") as aliases:
            data = yaml.load(aliases)
            for alias, name in data.items():
                alias_dict[alias] = name
        return alias_dict
    except FileNotFoundError:
        return None


count_tags('example.com')


