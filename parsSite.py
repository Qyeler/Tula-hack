import json
import time
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumReal import getHTML, getHTMLozon


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
            i['name']=str(i['name']).lower()
            ret.append(i)
    return (ret)


def ozonpars(HTML):
    text = HTML
    fl = {"answer": []}
    cnt = 0
    if "l9k km0" in text:
        res = [i for i in range(len(text)) if text.startswith("l9k km0", i)]
        for i in res:
            strt = text.find("/product/", i)
            end = text.find('"', strt + 1)
            link = "https://ozon.ru" + text[strt:end]
            end = text.find("?", text.find("k0m", end + 1))
            strt = text.find(">", end - 10, end)
            price=findprice(link).replace('\u2009','')
            strt = text.find("<span>", text.find("em4 me4 em5 em7 tsBodyL yj4", end))
            end = text.find("<", strt + 1)
            name = text[strt + 6:end]
            if not price.isdigit():
                continue
            fl["answer"].append({"name": name, "link": link, "price": price})
            cnt += 1
            if cnt == 5:
                break
    else:
        res = [i for i in range(len(text)) if text.startswith("tile-hover-target ", i)]
        print(res)
        for i in res:
            strt = text.find("/product/", i - 1000, i)
            end = text.find('"', strt + 1)
            link = "https://ozon.ru" + text[strt:end]
            strt = text.find("<span>", text.find("em4 me4 em5 em7 tsBodyL yj4", end))
            end = text.find("<", strt + 1)
            name = text[strt + 6:end]
            price=findprice(link).replace('\u2009','')
            if not price.isdigit():
                continue
            fl["answer"].append({"name": name.lower(), "link": link, "price": str(int(price))})
            cnt += 1
            if cnt == 5:
                break
    print(fl['answer'])
    return(fl['answer'])

def findprice(URL):
    HTML=getHTMLozon(URL)
    fst=HTML.find('class="nn8 n8n"><span>')
    scnd=HTML.find('</span>',fst)
    ans=HTML[fst+22:scnd-2]

    return(ans)
def insert_text(text, your_input):
    for sim in str(text):
        your_input.send_keys(sim)
        time.sleep(0.1)


def try_connect_site(url,driver):
    try:
        driver.get(url)
        return 1
    except Exception:
        return 0


def pritserupars(url):
    opts = Options()
    opts.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
    driver = webdriver.Chrome(options=opts)

    if try_connect_site(url,driver):
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        targets = []
        price = []
        try:
            driver.find_element(by=By.XPATH,
                                value='/html/body/div/div/div/main/div[4]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[3]').click()
            sleep(2)
            driver.get(driver.current_url + '/?products-sort=price-asc')
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
            costil["answer"].append({"name":targets[i].lower(),"price":(price[i][:-2].replace(" ","")),"link":driver.current_url})
        return costil['answer']
    else:
        return {'name': [],
                'price': [],
                "link": []}
def parswld(HTML):
    text = HTML
    fl = {"answer": []}
    cnt = 0
    strt = 0
    end = 0
    res = [i for i in range(len(text)) if text.startswith("product-card__wrapper", i)]
    for i in res:
        print(text.find('href="', i))
        strt = text.find('href="', i) + 6
        end = text.find('"', strt)

        link = text[strt:end]

        strt = text.find("price__lower-price", end) + 20
        end = text.find("?", strt)
        price = text[strt:end]
        for j in range(len(price)):
            if price[j] != " ":
                price = price[j:]
                break
        price = "".join(price.split("&nbsp;"))
        strt = text.find('"', text.find("product-card__name", end)) + 18
        end = text.find('"', strt)
        name = text[strt:end]
        for j in range(len(name)):
            if name[j] == ">":
                name = name[j + 1:]
                break
        for j in range(len(name)):
            if name[j] == "<":
                name = name[:j]
                break
        fl["answer"].append({"name": name, "link": link, "price": price})
    ret=[]
    for i in range(len(fl['answer'])):
        fl['answer'][i]['price'] = fl['answer'][i]['price'][0:price.find(" ") - 1]
        while not str(fl['answer'][i]['price']).isdigit() and len(str(fl['answer'][i]['price']))!=0:
            fl['answer'][i]['price'] = fl['answer'][i]['price'][0:-1]
        ret.append((fl['answer'][i]))
    return(ret)