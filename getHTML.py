#  Install the Python ScrapingBee library:
# `pip install scrapingbee`
from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='5YXRIIN5991ZNAPP091D2F26E4FZO0DCJFMWLIQZRI8PNX9BOPG4K7TPJ6R6GT6ROI56CL1VW9EP8Q8H')
def getHTML(URL):
    URL='https://market.yandex.ru/search?cvredirect=1&searchContext=&text=iphone+13'
    response = client.get(
        URL,
        params={
            "screenshot": "true",
            "wait": "10",
            "return_page_source": "true",
            "block_ads": "true",
            "premium_proxy": "true",
            "json_response": "true",
            'country_code':'ru'
        },  headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'X-Amzn-Trace-Id': 'Root=1-644ccfd6-417619e2388e4cb8191ab5dc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36',
        }
    )
    if(response.status_code==200):
        print('Response HTTP Response Body: ', response.content)
    else:
        print("ERROR")
