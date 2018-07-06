import urllib
import json

def request(url):
    return urllib.urlopen(url).read()

def dump(con):
    content = list()
    with open('./cache/lod-cloud.json', 'w+') as lod_dump:
        lod_dump.write(con)
        print 'lod-cloud dumped'

def main():
    url = 'http://lod-cloud.net/lod-data.json'
    con = request(url)
    dump(con)


if __name__ == '__main__':
    main()
