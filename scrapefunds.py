from bs4 import BeautifulSoup
from urllib2 import urlopen
import locale
from datetime import datetime

BASE_URL = ""

def get_fund_info(section_url):
	locale.setlocale(locale.LC_ALL, 'sv_SE.UTF8')
	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")

	something = []
	for tr in soup.findAll("tr", class_=False):
		alltd = tr.findAll("td")
		something.append({'name' : alltd[0].string,
			'value' : locale.atof(alltd[1].string),
			'ccy' : alltd[2].string,
			'date' : datetime.strptime(alltd[3].string, '%Y-%m-%d').date()})

	return something


url = "file:///home/mats/Downloads/onefund.xls"
myvar = get_fund_info(url)
print myvar