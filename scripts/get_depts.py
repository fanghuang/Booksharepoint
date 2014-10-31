import requests
from bs4 import BeautifulSoup

def main():
	r = requests.get("http://bookstore.rose-hulman.edu/SelectTermDept.aspx")
	if (r.status_code == 200):
		c = r.content
		soup = BeautifulSoup(c)
		deptSelector = soup.body.find(id="ctl00_ctl00_Content_Content_courseSelect_ddlDept")
		count = 0
		for option in deptSelector.findAll("option"):
			item = '<a class="list-group-item'
			if count == 0:
				item += ' active">All Departments</a>'
			else:
				item += '">' + option.text.strip() + '</a>'
			print item
			count += 1

if __name__ == '__main__':
	main()