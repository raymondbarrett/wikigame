import requests
import random
from bs4 import BeautifulSoup
import re

minyear = -50
maxyear = 2022

randyear = 0
while not randyear:
    randyear = random.randint(minyear, maxyear)
yearstr = 'AD_' + str(randyear) if randyear > 0 else (str(-1*randyear) + '_BC')

wiki = requests.get('https://en.wikipedia.org/api/rest_v1/page/html/' + yearstr, headers={'Api-User-Agent': 'raymondtbarrett@gmail.com'})
print('Year: ' + yearstr)
print(wiki.status_code)

soup = BeautifulSoup(wiki.text, 'html.parser')
match_elements = soup.find_all(re.compile('(li)|(h2)'))

incl = False
clues_text = []
for element in match_elements:
    element_text = element.get_text()
    if element_text == 'Events':
        incl = True
        continue
    elif element_text == 'References':
        incl = False
        continue
    elif element.name == 'h2':
        continue
    if '\n' in element_text:
        continue
    if incl:
        clues_text.append(element_text)
print(clues_text)