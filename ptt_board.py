import random
from util import get_soup
from ptt_page import ptt_page
from vars import vars

class ptt_board():
	def __init__(self, name):
		self.name = name
		if not self.valid:
			return
		self.get_max_page_index()

	def getValid(self):
		return True if self.name in vars.init_url.keys() else False
	valid = property(getValid)

	def get_max_page_index(self):
		soup = get_soup(vars.init_url[self.name])
		maxpage = soup.find('div', {'class' : 'btn-group pull-right'}).findAll('a')[1]['href'].replace(vars.url_ending, '')
		self.max_page_index = int(maxpage[maxpage.index('index') + 5:]) + 1

	def get_random_page(self):
		page = str(random.randint(1, self.max_page_index))
		print('page: ' + page)
		return ptt_page(vars.init_url[self.name] + page)