import random
from util import get_soup
from ptt_article import ptt_article
from vars import vars

class ptt_page():
	def __init__(self, page_sub_url):
		self.soup = get_soup(page_sub_url)

	def get_random_article(self, lower_bound = 50):
		article_list = []
		raw_article_list = self.soup.findAll('div', {'class' : 'r-ent'})
		for a in raw_article_list:
			if self.check_if_candidate(a.find('div', {'class' : 'nrec'}).getText(), lower_bound):
				article_list.append(self.get_page_url(a))
		if len(article_list) == 0:
			return None
		return ptt_article(vars.ptt_url + article_list[random.randint(0, len(article_list) - 1)])

	def check_if_candidate(self, popularity, lower_bound):
		if vars.popularity_excep[0] in popularity:
			return True
		if vars.popularity_excep[1] in popularity or popularity == '':
			return False
		p = int(popularity)
		return p >= lower_bound

	def get_page_url(self, raw):
		href = raw.find('a', {'href' : True})
		if not href:
			return None
		return href['href']