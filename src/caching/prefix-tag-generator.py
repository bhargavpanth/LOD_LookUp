import urllib
from bs4 import BeautifulSoup
import json
import io

# http://lov.okfn.org/dataset/lov/vocabs/

prefix_list = list()
dump_list = list()

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
    global dump_list
    try:
        soup = BeautifulSoup(page, 'html.parser')
    except Exception as e:
        raise
    else:
        try:
            for each_tag in soup.findAll('a', {'class': 'tag'}):
                tags.append(each_tag.getText())
        except Exception as e:
            print 'no tags found for vocab', pf
    data = {'prefix': pf, 'tags': tags}
    dump_list.append(data)


def json_dump():
    global dump_list
    with open('./cache/prefix-tag_dump.json', 'w+') as tags_dump:
        dump = json.dumps(dump_list, indent=4, sort_keys=True,
                              separators=(',', ': '), ensure_ascii=False)
        tags_dump.write(dump)
        print 'prefix and tag pair dumped'

def main():
    count = 1
    global prefix_list
    url = 'http://lov.okfn.org/dataset/lov/vocabs/'
    for each_prefix in prefix_list:
        print 'prefix ', count, ' of', len(prefix_list), ' processing...'
        _url = url + str(each_prefix)
        content = request(_url)
        extract(content, str(each_prefix))
        count += 1
    print 'extraction of all prefixes and tags completed... Dumping the data in cache'
    json_dump()

if __name__ == '__main__':
    main()

# print prefix_list
