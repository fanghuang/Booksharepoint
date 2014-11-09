#import requests
from bs4 import BeautifulSoup
import urllib3
http = urllib3.PoolManager()


def get_options():
	#r = requests.get("http://bookstore.rose-hulman.edu/SelectTermDept.aspx")
	r = http.request('GET', 'http://bookstore.rose-hulman.edu/SelectTermDept.aspx')
	if (r.status_code == 200):
		c = r.content
		soup = BeautifulSoup(c)
		deptSelector = soup.body.find(id="ctl00_ctl00_Content_Content_courseSelect_ddlDept")
		options = [option.text.strip() for option in deptSelector.findAll("option")]
		return options
	
def gen_html():
	count = 0
	for option in get_options():
		item = '<a class="list-group-item'
		if count == 0:
			item += ' active">All Departments</a>'
		else:
			item += '">' + option + '</a>'
		print item
		count += 1

if __name__ == '__main__':
	gen_html()
