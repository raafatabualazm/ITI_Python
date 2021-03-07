import requests
from bs4 import BeautifulSoup
import re

try:
    file = open('data.csv', 'w')
except:
    print("Error loading file")

def open_link(link):
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
                  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        sess = requests.Session()
        res = sess.get(link, headers = header)
        return res.json()
    except Exception  as e:
        print(e)

def open_page(link):
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
                  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        sess = requests.Session()
        res = sess.get(link, headers=header)
        soup = BeautifulSoup(res.text)
        return soup
    except:
        print("Error getting main page.")

def get_numbers(links):
    j = open_link(links)
    try:
        tel1 = j['seller']['primaryContactNumber']
        if not re.match('\(07\d+\)\s+\d+', tel1) and not re.match('\(\+44\d+\)\s+\d+', tel1):
            tel1 = ""
    except:
        tel1 = ""

    try:
        tel2 = j['seller']['secondaryContactNumber']
        if not re.match('\(07\d+\)\s+\d+', tel2) and not re.match('\(\+44\d+\)\s+\d+', tel2):
            tel2 = ""
    except:
        tel2 = ""
    try:
        is_private = j['seller']['isTradeSeller']
    except:
        is_private = ""
    if tel1 == "" and tel2 == "":
        return
    else:
        file.write(str(is_private) + ',' + tel1 + ',' + tel2 + '\n')

def scrap_page(soup):
    links = soup.find_all('a', class_='js-click-handler listing-fpa-link tracking-standard-link')
    for link in links:
        num = re.findall('\/car-details\/(\d+)\?',link['href'])[0]
        get_numbers('https://www.autotrader.co.uk/json/fpa/initial/{}?advertising-location=at_cars&guid=036dad4d-4b54-4bfe-af66-735910fc5b81&include-delivery-option=on&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&page=1&postcode=e113ld&radius=1501&sort=relevance'.format(num))

try:
    for i in range(1, 50432):
        link = 'https://www.autotrader.co.uk/car-search?advertClassification=standard&postcode=E113LD&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&advertising-location=at_cars&is-quick-search=TRUE&include-delivery-option=on&page={}'.format(i)
        page = open_page(link)
        scrap_page(page)
except Exception as e:
    print(e)

file.close()
print('File Closed!')
