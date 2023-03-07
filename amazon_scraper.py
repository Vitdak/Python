import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

search_query = 'lithuanian gifts'.replace(' ', '+')
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

items = []
for i in range (1, 11):
    print ('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = bs(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
    for result in results:
        product_name = result.h2.text
        try:
            rating = result.find('i', {'class' : 'a-icon'}).text
            rating_count = result.find('span', {'aria-label' : True}).text
        except AttributeError:
            continue

        try:
            price_whole = result.find('span', {'class': 'a-price-whole'}).text
            price_fraction = result.find('span', {'class': 'a-price-fraction'}).text
            price = float(price_whole + price_fraction)
            product_url = 'https://amazon.com' + result.h2.a['href']
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue
    sleep(1.5)

df = pd.DataFrame(items, columns=['product', 'rating', 'rating count', 'price', 'product url'])
df.to_csv('{0}.csv'.format(search_query), index = False)

