import requests
import sys
from bs4 import BeautifulSoup
from vars import vars

def get_soup(url, is_sub=True):
    if is_sub:
        re = requests.get(vars.ptt_url + url + vars.url_ending).content
    else:
        re = requests.get(url).content
    return BeautifulSoup(re, 'html5lib')
