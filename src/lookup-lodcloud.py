import urllib
from pymongo import MongoClient
import sets
from bs4 import BeautifulSoup


def get_vocabs(dataset):
    vocab_list = list()
    # given a dataset -> export the vocab list
    try:
        client = MongoClient('localhost', 27017)
    except Exception as e:
        raise e
    else:
        db = client['lodcloud']
        ds = db.vocab.find({'dataset': dataset})
        # ds = db.domain_vocab.find({'dataset': dataset})
        for each_vocab in ds:
            vocab_list.append(each_vocab['vocab'])
            # print each_vocab['tag']
        return vocab_list

def ratio_of_open_to_close_vocab(dataset, vocab_list):
    vocab_set = set()
    for each_vocab in vocab_list:
        vocab_set.add(each_vocab)
    for each_vocab_in_set in vocab_set:
        flag = _check_prefix_(each_vocab_in_set)
    
# methods starting and ending with _ are methods used by one or more methods and not called from the main
def _check_prefix_(vocab):
    flag = bool()

    return flag


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


def __request_prefix__(url):
    if 'http://purl.org/dc/elements/1.0/' in url:
        return str('dc')
    else:
        encode_vocab = urllib.quote_plus(str(url))
        _url = "http://prefix.cc/?q="+encode_vocab
        content = request(_url)
        prefix = parse_vocab_prefix(content)
        # print dataset , ' --> ' ,  prefix , ' --> ' , count
        return prefix

def main():
    get_vocabs('Anti-Beatles')

if __name__ == '__main__':
    main()
