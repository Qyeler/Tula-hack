#  Install the Python ScrapingBee library:
# `pip install scrapingbee`
import codecs

from scrapingbee import ScrapingBeeClient
import requests
import chardet

client = ScrapingBeeClient(api_key='1OPDXF9D1ZX7YY0D1B87KZETIX9S4BBCZGM01SQBP3Q13HZTU6F4EFJ1CI2VE7MJK5G5IBPRWKX63IPY')
def getHTML(URL):
    URL='https://market.yandex.ru/search?cvredirect=1&searchContext=&text=iphone+13&suggest_reqid=759213224166835892464853299797782'
    '''
    if(URL[0:31]=='https://www.citilink.ru/search/'):
        f = open('test.txt', 'w', encoding='utf-8')
        response = requests.get(URL)
        html = response.text
        f.write(html)
        return(html)
    else:
    '''
    response = client.get(
        URL,
        params={
            "wait": "1000",
            "stealth_proxy": "true",
            "return_page_source": "true",
            "block_ads": "false",
            'block_resources' : 'False',
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
