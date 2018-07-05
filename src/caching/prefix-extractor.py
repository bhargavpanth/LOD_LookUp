import urllib
from bs4 import BeautifulSoup
import json
import io

prefix = list()


def request(url):
	return urllib.urlopen(url).read()


def parse(page):
	# parse <span> <a>
	global prefix
	try:
		soup = BeautifulSoup(page, 'html.parser')
	except Exception as e:
		raise
		print 'unable to fetch ', page
	else:
		for each_prefix in soup.findAll('span', {'class': 'prefix'}):
			prefix.append(each_prefix.getText())

def json_dump():
    global prefix
    with open('./cache/prefix_dump.json', 'w+') as dump_file:
        data = {'prefix': prefix}
        json_str = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        dump_file.write(json_str)


def main():
    global prefix
    url = 'http://lov.okfn.org/dataset/lov/vocabs?&page='
    for counter in range(1, 44):
        _url = url + str(counter)
        content = request(_url)
        parse(content)
    print 'Obtained all vocabulary prefixes from http://lov.okfn.org'
    json_dump()



if __name__ == '__main__':
	main()
