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
import re

out_data = "Процент нарушений требований по размещению общей информации об образовательной организации- 0 % Процент нарушений требований по размещению информации в ФИС ГИА и приема- 8 %Процент нарушений требований по соответствию информации на сайте образовательной организации и в ФИС ГИА и приема- 0 %Итоговый процент нарушений- 1 %Группа АИС \"Мониторинг\"- 1Количество не снятых с контроля предписаний- 0"

link = 'https://map.obrnadzor.gov.ru/application/university'

def parser_vuz_id():
    driver = webdriver.Chrome()
    driver.get(link)
    button = driver.find_element_by_class_name("form_submit")
    button.click()
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
    if id_vuz[-1] == '':
        id_vuz.remove('')
    #id_vuz = id_vuz[]

    #id_vuz = id_vuz[:3000]
    #id_vuz = id_vuz[3000:6000]
    #id_vuz = id_vuz[6000:7000]
    #id_vuz = id_vuz[7000 : -2]

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
             'Населённый пункт:': '', 'Форма собственности:': '', 'Адрес:': '', 'Лицензия: №': '', 'specialization': []}
        for key, value in zip(keys, values):
            if key.text in x.keys():
                if x['Населённый пункт:'] == '':
                    for el in x['Адрес:'].split(','):
                        if el.find('г.') >= 0 or el.find('город')>=0:
                            x['Населённый пункт:'] = el
                            break

                x[key.text] = value.text

        if x['Лицензия: №'].find('(Бессрочная)') >= 0:

            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

            button = driver.find_element_by_id("monitoring")
            button.click()

            stop = False
            input_last_page = []
            input_new_page = []
            input_numbers = []
            input_spec = []
            while stop != True:
                try:
                    time.sleep(0.5)
                    if driver.find_element_by_class_name('nom_end').text == '1337':     stop = True

                    time.sleep(2)

                    elements = driver.find_elements_by_tag_name("td")
                    for el in elements:
                        if (el.text not in out_data) and (el.text.find('%')== -1) and (el.text.find('-')== -1):
                            if (el.text not in x['specialization']):
                                input_new_page.append(el.text)
                                if el.text.replace('.', '').replace(' ', '').isdigit() and len(el.text.replace('.', '').replace(' ', '')) == 6:
                                    input_numbers.append(el.text.replace('.', '').replace(' ', ''))


                    if input_new_page == input_last_page:
                        stop = True
                    else:
                        x['specialization'].extend(input_numbers)
                        input_last_page = input_new_page
                        input_numbers = []
                        input_new_page = []

                    element = driver.find_element_by_class_name('next1')
                    element.click()
                    time.sleep(2)

                except:
                    stop = True
            if x['specialization'] != []:
                df = df.append(x, ignore_index=True)
            print(id)

    driver.stop_client()
    driver.close()
    driver.quit()
    return df


def get_codes(n):
    data = {'':''}
    url = 'https://map.obrnadzor.gov.ru/application/university/view/6721'
    driver = webdriver.Chrome()
    driver.get(url)
    button = driver.find_element_by_id("monitoring")
    button.click()

    next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
    next_page.click()

    time.sleep(2)
    print('hi')
    next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
    next_page.click()
    time.sleep(2)

    for i in range(min(1337,n)):
        elements = driver.find_elements_by_tag_name("td")
        last_element = ''
        for el in elements:
            if (el.text not in out_data) and (el.text.find('%') == -1) and (el.text.find('-') == -1):
                #print(el.text)
                element = el.text.replace('.','')
                if(element.replace(' ', '').isdigit() and (len(element)>=5)):
                    element = element.replace(' ', '')
                    if not element in data.keys():
                        data[element] = ''
                        last_element = element

                else:
                    if data[last_element] == '' and element != '':
                        data[last_element] = element



        next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'prew1')))
        next_page.click()
        time.sleep(1)
    time.sleep(1)

    return data

def get_all_codes():
    d = get_codes(1337 - 75)
    with open('text.txt', 'w') as file:
        for key, value in d.items():
            if key != '':
                file.write(f'{key}, {value}\n')

        file.close()


if __name__ == '__main__':
    parser_vuz_id()
    df = make_df('id_unique.csv')
    df.to_csv('file_data4.csv', encoding='utf-8-sig', sep='|')
    get_all_codes()


