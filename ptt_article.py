import random
from util import get_soup
from vars import vars

class ptt_article():
    def __init__(self, url):
        self.url = url
        print('article url: ' + url)
        self.soup = get_soup(url, is_sub = False)

    def get_random_image(self):
        image_list = [('http:' + i['src']) if 'http' != i['src'][:4] else i['src'] for i in self.soup.findAll('img', {'src' : True})]
        if len(image_list) == 0:
            return None
        return image_list[random.randint(0, len(image_list) - 1)]
