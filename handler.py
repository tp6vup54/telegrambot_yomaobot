import vars
import requests
from bs4 import BeautifulSoup

def getPttIndexPage(sub_url):
	re = requests.get(vars.ptt_url + sub_url)
	soup = BeautifulSoup(re.text.encode('utf-8'), 'html.parser')
	#maxpage = 
	print(soup)

def cat():
	print('cat')
	pass

def girl():
	getPttIndexPage(vars.ptt_beauty_init)
	pass