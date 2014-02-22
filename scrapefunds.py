#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib2 import urlopen
import locale
from datetime import datetime

from fundtables import Funds, FundTimeSeries
import dbconfig

def get_fund_info(section_url):
	locale.setlocale(locale.LC_ALL, 'sv_SE.UTF8')
	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")

	fundinfo = {}

	fundquery = Funds.select()

	dbconfig.database.set_autocommit(False)

	for tr in soup.findAll("tr", class_=False):
		alltd = tr.findAll("td")
		name = alltd[0].string
		currency = alltd[2].string
		value = locale.atof(alltd[1].string)
		valuedate = datetime.strptime(alltd[3].string, '%Y-%m-%d').date()

		try:
			fund = fundquery.where(Funds.name == name).get()
		except Funds.DoesNotExist:
			fund = Funds.create(
				name = name,
				currency = currency,
				start_date = valuedate
			)
		timeseries = FundTimeSeries.create(
			fund = fund,
			date = valuedate,
			value = value
		)
	
	dbconfig.database.commit()
	dbconfig.database.set_autocommit(True)

url = "file:///home/mats/Downloads/onefund.xls"
get_fund_info(url)
