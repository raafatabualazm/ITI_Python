from bs4 import BeautifulSoup
import requests_html
import re

try:
    file = open('phones.csv', 'w')
except:
    print("Error opening file.")


def open_page(link):
    try:
        sess = requests_html.HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'"])
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
                  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        #driver.get(link)
        res = sess.get(link, headers=header)
        js = res.html.render(timeout=30)
        soup = BeautifulSoup(res.html.html)
        return soup
    except Exception as e:
        print(e)

def get_tel(link):
    try:
        page = open_page(link)

    except:
        print("Error opening link")
    try:
        tel_tags = page.find_all('a', class_='about-seller__contact-number about-seller__item atc-type-fiesta atc-type-fiesta--medium')
        for tel in tel_tags:
            if re.match('tel:07\d+', tel['href']) or re.match('tel:\+44\d+', tel['href']):
                file.write(tel['href'] + '\n')

    except:
        print("Error extracting numbers")

def scrap_page(soup):
    links = soup.find_all('a', class_='js-click-handler listing-fpa-link tracking-standard-link')
    for link in links:
        get_tel('https://www.autotrader.co.uk'+link['href'])


try:
    for i in range(1, 50432):
        link = 'https://www.autotrader.co.uk/car-search?advertClassification=standard&postcode=E113LD&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&advertising-location=at_cars&is-quick-search=TRUE&include-delivery-option=on&page={}'.format(i)
        page = open_page(link)
        scrap_page(page)
except Exception as e:
    print(e)

file.close()
print('File Closed!')