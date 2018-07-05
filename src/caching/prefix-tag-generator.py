import urllib
from bs4 import BeautifulSoup
import json

# http://lov.okfn.org/dataset/lov/vocabs/

prefix_list = list()

try:
    with open('./cache/prefix_dump.json') as prefix:
        json_prefix_file = json.load(prefix)
except Exception as e:
    raise
    print 'prefix_dump.json file does not exist. Run prefix-extractor.py first to generate the prefix_dump.json file'
else:
    prefix_set = json_prefix_file["prefix"]
    for each_prefix in prefix_set:
        prefix_list.append(each_prefix)

def request(url):
    return urllib.urlopen(url).read()

# print prefix_list
