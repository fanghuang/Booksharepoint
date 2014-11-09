from google.appengine.api import urlfetch
import lxml.html

def get_options():
	url = "http://bookstore.rose-hulman.edu/SelectTermDept.aspx"
	resp = urlfetch.fetch(url)
	if resp.status_code == 200:
		tree = lxml.html.fromstring(resp.content) 
	
		deptSelector = tree.get_element_by_id("ctl00_ctl00_Content_Content_courseSelect_ddlDept")
		options = [option.text.strip() for option in deptSelector.findall('option')]
		return options
	
def gen_html():
	output = ""
	count = 0
	for option in get_options():
		item = '<a class="list-group-item'
		if count == 0:
			item += ' active">All Departments</a>'
		else:
			item += '">' + option + '</a>'
		output += item + "\n"
		count += 1
	return output

if __name__ == '__main__':
	print gen_html()