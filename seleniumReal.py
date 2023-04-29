import time
from selenium import webdriver

def getHTML(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(3)
    html = driver.page_source
    f = open('test.txt', 'w', encoding='utf-8')
    f.write(html)
    driver.quit()
    return(html)


