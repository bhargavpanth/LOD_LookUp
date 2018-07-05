import urllib
from bs4 import BeautifulSoup

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


def main():
	global prefix
	url = 'http://lov.okfn.org/dataset/lov/vocabs?&page='
	for counter in range(1, 44):
		_url = url + str(counter)
		content = request(_url)
		parse(content)

	print prefix


if __name__ == '__main__':
	main()
