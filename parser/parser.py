import requests
from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import numpy as np
import pandas as pd



link = 'https://map.obrnadzor.gov.ru/application/university'

def parser_vuz_id():
    driver = webdriver.Chrome()
    driver.get(link)
    #driver.find_element_by_xpath("//input[@value = \'Найти\']").click()
    button = driver.find_element_by_class_name("form_submit")
    button.click()
    #element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'next1')))
    #element.click()
    #WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'click_vuz_k')))
    #WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
    #elements = driver.find_elements_by_tag_name('tr')
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    with open('id.csv', 'w+') as file:

        for i in range(686):
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
            elements = driver.find_elements_by_tag_name('tr')
            for element in elements:
                if element.get_attribute("id_vuz"):
                    file.write(str(element.get_attribute("id_vuz"))+';')
            time.sleep(2)

            next_page = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, 'next1')))
            next_page.click()

    file.close()




def make_df(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            id_vuz = line.split(';')
    print(id_vuz)
    if id_vuz[-1] == '':
        id_vuz.remove('')
    #id_vuz = id_vuz[]
    print(id_vuz)
    col = ['id', 'Название', 'Регион:', 'Населённый пункт:', 'Форма собственности:', 'Адрес:', 'Лицензия: №']
    df = pd.DataFrame(columns=col)
    url = 'https://map.obrnadzor.gov.ru/application/university/view/'
    driver = webdriver.Chrome()


    for id in id_vuz:
        driver.get(url + str(id))
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'descript')))
        keys = driver.find_elements_by_class_name("descript")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'vuz_value')))
        values = driver.find_elements_by_class_name("vuz_value")
        x = {'id': str(id), 'Название': driver.find_element_by_class_name("title_vuz").text, 'Регион:': '',
             'Населённый пункт:': '', 'Форма собственности:': '', 'Адрес:': '', 'Лицензия: №': ''}
        #print(driver.find_element_by_class_name("title_vuz").text)
        for key, value in zip(keys, values):
            if key.text in x.keys():
                if x['Населённый пункт:'] == '':
                    for el in x['Адрес:'].split(','):
                        if el.find('г.') >= 0:
                            x['Населённый пункт:'] = el
                            break

                x[key.text] = value.text

        if x['Лицензия: №'].find('(Бессрочная)') >= 0:
            df = df.append(x, ignore_index=True)


    return df

if __name__ == '__main__':
    df = make_df('test.csv')
    print(df)
    df.to_csv('file1.csv', encoding='utf-8-sig', sep='|')