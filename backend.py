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

curr_sec = ''
events_text = []
births_text = []
deaths_text = []
prepend_txt = ''
for element in match_elements:
    element_text = element.get_text()
    element_text = re.sub('(BC)|(AD)|(\(.*?\d+.*?\))|\[\d+\]', '', element_text.replace(str(randyear), '????'))
    if element_text == 'Events' and curr_sec == '':
        curr_sec = 'Events'
        continue
    elif element_text == 'References' and curr_sec == 'Deaths':
        curr_sec = ''
        continue
    elif element_text == 'Births' and curr_sec == 'Events':
        curr_sec = 'Births'
        continue
    elif element_text == 'Deaths' and curr_sec == 'Births':
        curr_sec = 'Deaths'
        continue
    elif element.name == 'h2':
        curr_sec = ''
        continue
    if '\n' in element_text:
        continue
    if curr_sec == 'Events':
        events_text.append(element_text)
    elif curr_sec == 'Births':
        births_text.append('Born on this year: ' + element_text)
    elif curr_sec == 'Deaths':
        deaths_text.append('Died on this year: ' + element_text)
for clue in events_text:
    print(clue)
for clue in births_text:
    print(clue)
for clue in deaths_text:
    print(clue)