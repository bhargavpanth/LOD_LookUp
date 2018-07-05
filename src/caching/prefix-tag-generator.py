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

def extract(page, pf):
    tags = list()
    try:
        soup = BeautifulSoup(page, 'html.parser')
    except Exception as e:
        raise
    else:
        try:
            for each_tag in soup.findAll('a', {'class': 'tag'}):
                tags.append(each_tag)
        except Exception as e:
            print 'no tags found for vocab', pf

def main():
    global prefix_list
    url = 'http://lov.okfn.org/dataset/lov/vocabs/'
    for each_prefix in prefix_list:
        _url = url + str(each_prefix)
        content = request(_url)
        extract(content, str(each_prefix))

# print prefix_list
