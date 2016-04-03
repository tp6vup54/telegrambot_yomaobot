import requests
from bs4 import BeautifulSoup
import vars

def get_soup(url, is_sub = True):
	if is_sub:
		re = requests.get(vars.ptt_url + url + vars.url_ending).content
	else:
		re = requests.get(url).content
	return BeautifulSoup(re, 'html5lib')