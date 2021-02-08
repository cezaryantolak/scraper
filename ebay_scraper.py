import requests
from bs4 import BeautifulSoup
import pandas as pd


def DisplayOptions(options):
    for i in range(len(options)):
        print("{} - {}".format(i+1, options[i]))
 
    choice = int(input('Select option above or press enter to exit: '))
    choice_type = options[choice-1]
    
    return choice_type

choice='x'
options = ['kruggerand', 'eagle', 'maple', 'philharmonic']
choicetype = DisplayOptions(options)


def get_data(choicetype):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={choicetype}+gold+1oz&_sacat=39482&LH_TitleDesc=0&rt=nc&LH_Sold=1&LH_Complete=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {'title': item.find('h3', {'class': 's-item__title'}).text,
                   'soldprice': float(item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',','').strip()), 
                   'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class': 'POSITIVE'}).text, 
                   'link': item.find('a', {'class': 's-item__link'})['href']}
        productslist.append(product)
    return productslist

def output(productslist, choicetype):
    productsdf = pd.DataFrame(productslist)
    productsdf.to_csv(choicetype + 'output.csv', index = False)
    print('Saved to CSV')

soup = get_data(choicetype)
productslist = parse(soup)
output(productslist, choicetype)

    

