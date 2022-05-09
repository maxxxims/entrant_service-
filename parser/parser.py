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
    if id_vuz[-1] == '':
        id_vuz.remove('')
    #id_vuz = id_vuz[]

    id_vuz = id_vuz[:60]

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
        #print(driver.find_element_by_class_name("title_vuz").text)
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
            #pages = int(WebDriverWait(driver, 100, ignored_exceptions=ignored_exceptions).until(
            #    EC.presence_of_element_located((By.CLASS_NAME, 'nom_end'))).text)

            #time.sleep(5)

            '''try:

                pages = driver.find_elements_by_class_name('nom_end').text
                print(pages)
            except:
                pages = 0
                print('хуй')'''
            '''#print('pages is'+str(pages))
            time.sleep(2)
            pages = int(pages)

            elements = driver.find_elements_by_tag_name("td")
            print(id)
            #print('len elements'+str(len(elements)))
            for el in elements:
                if el.text not in out_data:
                    x['specialization'].append(el.text)
                    print(el.text)
'''
            stop = False
            input_last_page = []
            input_new_page = []
            input_numbers = []
            input_spec = []
            while stop != True:
                try:
                    if driver.find_element_by_class_name('nom_end').text == '1337':     stop = True


                    time.sleep(2)
                    # WebDriverWait(driver, 10000)
                    # WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
                    elements = driver.find_elements_by_tag_name("td")
                    for el in elements:
                        if (el.text not in out_data) and (el.text.find('%')== -1) and (el.text.find('-')== -1):
                            if (el.text not in x['specialization']):
                                input_new_page.append(el.text)
                                if el.text.replace('.', '').replace(' ', '').isdigit() and len(el.text.replace('.', '').replace(' ', '')) == 6:
                                    input_numbers.append(el.text.replace('.', '').replace(' ', ''))

                                #x['specialization'].append(el.text)
                                #print(el.text)

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
            '''print(pages - 1)
            for j in range(pages - 1):
                print("IM HERE BITHES IM WORKINF SLSLFAFDFDASF")
                element = WebDriverWait(driver, 100, ignored_exceptions=ignored_exceptions).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'next1')))
                element.click()
                time.sleep(4)
                # WebDriverWait(driver, 10000)
                #WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
                elements = driver.find_elements_by_tag_name("td")
                for el in elements:
                    if el.text not in out_data:
                        x['specialization'].append(el.text)
                        print(el.text)'''

            if x['specialization'] != []:
                df = df.append(x, ignore_index=True)


    return df

if __name__ == '__main__':
    df = make_df('id_unique.csv')
    #print(df)
    df.to_csv('file_data.csv', encoding='utf-8-sig', sep='|')