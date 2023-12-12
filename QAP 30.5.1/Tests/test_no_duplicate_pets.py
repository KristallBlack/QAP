# ЗАДАНИЕ 30.3.1
# ЯВНЫЕ ОЖИДАНИЯ

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def test_no_duplicate_pets(go_to_my_pets):
    '''Проверка того, что на странице "Мои питомцы" нет повторяющихся имен питомцев'''

    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    # Сохранение элементов с данными о питомцах в переменную "pet_data"
    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Перебираются данные из переменной "pet_data"
    # Сохраняются имя, возраст и порода, остальное меняется на пустую строку и разделяется по пробелу
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваются имя, возраст и порода
    # Получившиеся склееные слова добавляются в строку и между ними вставляется пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    # Получение списка из строки "line"
    list_line = line.split(' ')

    # Превращение списка в множество
    set_list_line = set(list_line)

    # Нахождение количества элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитается количество элементов множества
    result = a - b

    # Если количество элементов == 0, то карточки с одинаковыми данными отсутствуют
    assert result == 0