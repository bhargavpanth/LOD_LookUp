import urllib
from bs4 import BeautifulSoup

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
        else:
            return prefix

def main():
    encode_vocab = urllib.quote_plus('http://www.aktors.org/ontology/portal')
    _url = "http://prefix.cc/?q="+encode_vocab
    print _url
    content = request(_url)
    prefix = parse_vocab_prefix(content)
    print prefix

if __name__ == '__main__':
    main()
