# ЗАДАНИЕ 30.5.1
# ЯВНЫЕ ОЖИДАНИЯ

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password


def test_show_my_pets():
    '''Проверка того, что переход на страницу "Мои питомцы" осуществляется'''

    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email')))

    # Ввод эл.почты
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'pass')))

    # Ввод пароля
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))

    # Клик по кнопке "Войти"
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы')))

    # Клик по ссылке "Мои питомцы"
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    # Проверка того, что переход на страницу "Мои питомцы" осуществлен
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'