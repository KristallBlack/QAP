# ЗАДАНИЕ 30.3.1
# ЯВНЫЕ ОЖИДАНИЯ

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def test_photo_availability(go_to_my_pets):
    '''Проверка того, что на странице "Мои питомцы" хотя бы у половины питомцев есть фото'''

    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))

    # Сохранение элементов статистики в переменную "statistic"
    statistic = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')

    # Сохранение элементов с атрибутом "img" в переменную "images"
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    # Получение количества питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Нахождение половины от количества питомцев
    half = number // 2

    # Нахождение количества питомцев с фотографией
    number_of_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_of_photos += 1

    # Проверка того, что количество питомцев с фотографией больше или равно половине количества питомцев
    assert number_of_photos >= half
    print(f'Количество фото: {number_of_photos}')
    print(f'Половина от числа питомцев: {half}')