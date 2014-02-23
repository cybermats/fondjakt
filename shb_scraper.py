#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib2 import urlopen, quote
import locale
from datetime import datetime

from fundtables import Funds, FundTimeSeries
import dbconfig
import re

def generate_onefund_url(identifier, end_date):
	baseurl = "http://web.msse.se/shb/sv.se/history/onefund.xls"

	fundidattr = "fundid=" + identifier
	startdateattr = "startdate=2009-02-22%2000%3a00%3a00"
	enddateattr = "enddate=" + end_date.date().isoformat() + "%2000%3a00%3a00"

	attributes = fundidattr + "&" + startdateattr + "&" + enddateattr

	return baseurl + "?" + attributes

def get_fund_ids(section_url):
	locale.setlocale(locale.LC_ALL, 'sv_SE.UTF8')
	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")

	idlist = []

	slctTag = soup.find("select", id="FundId")
	options = slctTag.findAll("option")
	for option in options:
		val = option["value"]
		if val != "":
			idlist.append(val)
	return idlist


def get_fund_info(section_url):
	print section_url
	locale.setlocale(locale.LC_ALL, 'sv_SE.UTF8')
	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")

	regex = re.compile(r"[^0-9,]")

	fundinfo = {}

	fundquery = Funds.select()

	dbconfig.database.set_autocommit(False)

	for tr in soup.findAll("tr", class_=False):
		alltd = tr.findAll("td")
		name = alltd[0].string
		currency = alltd[2].string
		valuestr = regex.sub("", alltd[1].string)
		value = locale.atof(valuestr)
		valuedate = datetime.strptime(alltd[3].string, '%Y-%m-%d').date()

		try:
			fund = fundquery.where(Funds.name == name).get()
		except Funds.DoesNotExist:
			print "Create: " + name
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

historyurl = "file:///home/mats/Downloads/shb-history-front.html"
fundinfourl = "file:///home/mats/Downloads/onefund.xls"


#get_fund_info(fundinfourl)
ids = get_fund_ids(historyurl)
end_date = datetime(2014, 2, 22)
#ids = ["0P0000KXNT"]
failures = []
for id in ids:
	print id
	url = generate_onefund_url(id, end_date)
	try:
		get_fund_info(url)
	except:
		failures.append(id)

print "Finished."
print failures

