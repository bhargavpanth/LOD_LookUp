import urllib
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

# http://prefix.cc/?q=http%3A%2F%2Fwww.aktors.org%2Fontology%2Fportal

def request(url):
    return urllib.urlopen(url).read()


def parse_vocab_prefix(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
    except Exception as e:
        print e
    else:
        try:
            prefix = soup.find('h1').getText()
        except Exception as ex:
            print 'no prefix found'
            return None
        else:
            return prefix


def find_prefix(url, count, dataset):
    encode_vocab = urllib.quote_plus(str(url))
    _url = "http://prefix.cc/?q="+encode_vocab
    # print _url
    content = request(_url)
    prefix = parse_vocab_prefix(content)
    print dataset , ' --> ' ,  prefix , ' --> ' , count


def connect_mongodb(dataset_name):
    try:
        client = MongoClient('localhost', 27017)
    except Exception as e:
        print 'Unable to connect to MongoDD - Ensure the collection name - [vocab] exists within db name - [lodcloud] dataset with <dataset, vocab, count>'
        raise e
    else:
        db = client['lodcloud']
        dataset = db.vocab.find({'dataset': str(dataset_name)})
        for each_entry in dataset:
            find_prefix(each_entry['vocab'], each_entry['count'], dataset_name)
        

def main():
    try:
        with open('./cache/dataset_dump.json') as vocab_file:
            json_content = json.load(vocab_file)
    except Exception as e:
        print 'dataset_dump.json file is not existing in the cache - run cache scripts to download the dataset_dump cache'
        raise e
    else:
        datasets = json_content["datasets"]
        for each_dataset in datasets:
            connect_mongodb(each_dataset)


if __name__ == '__main__':
    main()
