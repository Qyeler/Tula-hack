import json
import time
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
driver = webdriver.Chrome(options=opts)


def ctlpars(HTML):
    # f = open("message1.txt","r",encoding="utf-8")
    text = HTML
    fl = {"answer": []}
    res = [i for i in range(len(text)) if text.startswith("data-meta-product-id", i)]
    for i in res[0:10]:
        j = text.find("/product", i)
        strt = j
        end = text.find('"', strt + 1)
        link = "https://www.citilink.ru/" + text[strt:end - 1]
        strt = text.find('title=', end) + 7
        end = text.find('"', strt + 1)
        name = text[strt:end]
        strt = text.find("data-meta-price", end) + 17
        end = text.find('"', strt + 1)
        price = text[strt:end]
        fl["answer"].append({"name": name, "link": link, "price": price})
    ret = []
    for i in fl['answer']:
        if (str(i['price']).isdigit()):
            ret.append(i)
    return (ret)


def ozonpars(HTML):
    return (0)

def insert_text(text, your_input):
    for sim in str(text):
        your_input.send_keys(sim)
        time.sleep(0.1)


def try_connect_site(url):
    try:
        driver.get(url)
        return 1
    except Exception:
        return 0


def pritserupars(url):
    if try_connect_site(url):
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        targets = []
        price = []
        try:
            driver.find_element(by=By.XPATH,
                                value='/html/body/div/div/div/main/div[4]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[3]').click()
            sleep(2)
            for i in range(1, 11):
                try:
                    targets.append(driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div/div/div/main/div[4]/div[2]/div[4]/div[1]/div[1]/div/div/div[{i}]/div[1]/div[2]/div[1]/div[1]/a').text)
                    price.append(driver.find_element(by=By.XPATH,
                                                     value=f'/html/body/div/div/div/main/div[4]/div[2]/div[4]/div[1]/div[1]/div/div/div[{i}]/div[2]/div[2]/div/a/span').text)
                except Exception as e:
                    pass
        except Exception as e:
            for i in range(1, 11):
                try:
                    # '/html/body/div/div/div/main/div[4]/div[2]/div[2]/div[2]/div[2]/div/div[{i}]/a[2]/span'
                    price.append(driver.find_element(by=By.XPATH,
                                                     value=f'/html/body/div/div/div/main/div[4]/div[2]/div[2]/div[2]/div[2]/div/div[{i}]/a[2]/span').text)
                    targets.append(driver.find_element(by=By.XPATH,
                                                       value=f'/html/body/div/div/div/main/div[4]/div[2]/div[2]/div[2]/div[2]/div/div[{i}]/div[1]/a/div').text)
                except Exception as e:
                    pass
    #ans{answer:[name price link]}
        costil={"answer":[]}
        for i in range(len(targets)):
            costil["answer"].append({"name":targets[i],"price":(price[i][:-2].replace(" ","")),"link":driver.current_url})
        return costil['answer']
    else:
        return {'name': [],
                'price': [],
                "link": []}
