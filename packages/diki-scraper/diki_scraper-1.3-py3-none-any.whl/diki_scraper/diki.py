import requests
from bs4 import BeautifulSoup
import re
import contextlib



def translation(word,num = 5, ex_trans = 1):
    
    result = requests.get(f'https://www.diki.pl/slownik-angielskiego?q={word}')
    soup = BeautifulSoup(result.text, 'html.parser')
    div_class = soup.find_all('div','dictionaryEntity')
    meaning_list = []


    for div in div_class:
        with contextlib.suppress(AttributeError):
            if ex_trans == 1 and div.find("span", {"class": "hw"}).text.strip() == word or ex_trans != 1:
                for m in div.find_all('li', re.compile('^meaning\d+')):
                    meaning_list.extend(span.text for span in m.find_all('span', 'hw'))
                        
    if meaning_list is None:
        meaning_list = []

    return meaning_list[:num] 