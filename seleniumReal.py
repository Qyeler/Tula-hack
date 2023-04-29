import time
from selenium import webdriver

def getHTML(URL):
    driver = webdriver.Chrome()  # Инициализация браузера
    driver.get(URL)  # Переход на страницу
    # Ждем, пока элемент, содержащий нужный контент, не станет видимым на странице
    time.sleep(3)
    html = driver.page_source  # Получаем HTML-код страницы
    f = open('test.txt', 'w', encoding='utf-8')
    f.write(html)
    driver.quit()  # Закрываем браузер
    return(html)
