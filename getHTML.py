#  Install the Python ScrapingBee library:
# `pip install scrapingbee`
import codecs

from scrapingbee import ScrapingBeeClient
import requests
import chardet

client = ScrapingBeeClient(api_key='JOYURIUORBC4I6128F9V8FKVF39MNOL65A06MPOJE5B6MADSLOFSQI9MDYXWQPV0XQYU48DX3P6J5U5O')
def getHTML(URL):
    URL='https://market.yandex.ru/search?cvredirect=1&searchContext=&text=iphone+14&suggest_reqid=759213224166835892405885879951824'
    response = client.get(
        URL,
        params={
            "wait": "1000",
            "stealth_proxy": "true",
            "return_page_source": "true",
            "block_ads": "false",
            'block_resources' : 'false',
            "premium_proxy": "true",
            "json_response": "true",
            'country_code':'ru'
        },  headers={
        }
    )
    f = open('test.txt', 'w', encoding='utf-8')
    read=response.content.decode('utf-8')
    f.write(read)
    print('Response HTTP Status Code: ', response.status_code)
    if(response.status_code==200):
        return(response.content)
    else:
        return(-1)
