import random
import re
from util import get_soup
from vars import vars

class ptt_article():
    def __init__(self, url):
        self.url = url
        print('article url: ' + url)
        self.soup = get_soup(url, is_sub=False)

    def get_random_image(self):
        p = re.compile('http.+jpg$|http.+png$|http.+jpeg$')
        images = []
        for i in self.soup.findAll('a', {'href': True}):
            if p.match(i['href']):
                images.append(i['href'])
        if not images:
            return None
        return images[random.randint(0, len(images) - 1)]
