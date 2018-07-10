import urllib
from pymongo import MongoClient
import json
from bs4 import BeautifulSoup
import sets
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def plot(vocab_list, open_vocab, close_vocab, total_vocab):
    # labels = vocab_list
    vocabs = list()
    for each_vocab in vocab_list:
        vocabs.append(each_vocab)
    fracs = [open_vocab, close_vocab]
    labels = ['close', 'open']
    # explode = (0, 0.05, 0, 0)
    # Make square figures and axes
    the_grid = GridSpec(2, 2)
    plt.subplot(the_grid[0, 0], aspect=1)
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    plt.subplot(the_grid[0, 1], aspect=1)
    plt.show()


def get_vocab_ratio(dataset):
    vocab_list = list()
    # tag_list = list()
    # given a dataset -> export the vocab list
    try:
        client = MongoClient('localhost', 27017)
    except Exception as e:
        raise e
    else:
        db = client['lodcloud']
        ds = db.vocab.find({'dataset': dataset})
        for each_vocab in ds:
            vocab_list.append(each_vocab['vocab'])
        tag_list = get_tags(dataset)
        ratio_of_open_to_close_vocab(vocab_list, dataset, tag_list)

def get_tags(dataset):
    tag_list = list()
    client = MongoClient('localhost', 27017)
    db = client['lodcloud']
    dbs = db.vocab_domain.find({'dataset': dataset})
    for each_tag in dbs:
        print each_tag['tag']
        tag_list.append(each_tag['tag'])
    return tag_list


def ratio_of_open_to_close_vocab(vocab_list, dataset, tags):
    vocab_set = set()
    
    open_vocab_count = 0
    closed_vocab_count = 0

    for each_vocab in vocab_list:
        vocab_set.add(each_vocab)
    total_vocabs = len(vocab_set)
    for each_vocab_in_set in vocab_set:
        flag = _check_prefix_(each_vocab_in_set)

        if flag is True:
            open_vocab_count += 1
        else:
            closed_vocab_count += 1
    
    print 'Dataset : ', dataset
    print 'Open vocabs : ', open_vocab_count
    print 'Closed vocabs : ', closed_vocab_count
    print 'Total Vocabs : ', total_vocabs
    print 'Vocab Tags : ', tags
    print '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
    plot(vocab_list, open_vocab_count, closed_vocab_count, total_vocabs)

# methods starting and ending with _ are methods used by one or more methods and not called from the main
def _check_prefix_(vocab):
    res = __request_prefix__(vocab)
    # open_vocab_count = 0
    # closed_vocab_count = 0
    if res == 'no registered prefix':
        return True
    else:
        return False
    # return open_vocab_count, closed_vocab_count

def __request_prefix__(url):
    if 'http://purl.org/dc/elements/1.0/' in url:
        return 'dc'
    else:
        encode_vocab = urllib.quote_plus(str(url))
        _url = "http://prefix.cc/?q="+encode_vocab
        content = request(_url)
        prefix = parse_vocab_prefix(content)
        return prefix

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

def request(url):
    return urllib.urlopen(url).read()



def main():
    try:
        with open('./cache/dataset_dump.json') as dataset:
            dataset_names = json.load(dataset)
    except Exception as e:
        raise e
    else:
        datasets = dataset_names["datasets"]
        for each_dataset in datasets:
            get_vocab_ratio(each_dataset)
            # get_vocab_ratio('Anti-Beatles')

if __name__ == '__main__':
    main()
