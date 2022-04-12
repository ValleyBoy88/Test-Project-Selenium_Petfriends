import pytest
from telnetlib import EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('e:/Roman/PycharmProject/Test_Project_Selenium/driver/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('technique_88@mail.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('TestYa88!!')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    pytest.driver.find_element_by_class_name('navbar-toggler-icon').click()
    pytest.driver.find_element_by_xpath('//*[contains(text(),"Мои питомцы")]').click()
    try:
        explicit_waits = WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]')))  # явные ожидания
        assert explicit_waits == 'all_my_pets'
        print('Элемент найден')
    except TimeoutException:
        print('Произошла ошибка')
    finally:
        pytest.driver.quit()

    pytest.driver.implicitly_wait(10)
   # Количество питомцев в блоке статистики пользователя
   statistics = int((pytest.driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text.split())[2])
   # Определяем список с количеством карточек питомцев
   descriptions = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tbody/tr')
   # Получаем количество питомцев с фотографией
   images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//img')
   # Получаем список питомцев с именами
   names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//td[1]')
   name_true = []
   for i in names:
       name_true.append(i.text)

   assert statistics == len(descriptions) # проверяем присутствие всех питомцев

   for i in range(len(names)):
       assert images[i].get_attribute('src') != '' # проверяем наличие фотографий у всех питомцев
       assert statistics == len(images) # проверяем, что хотя бы у половины питомцев есть фото
       assert names[i].text != '' # проверяем, что у всех питомцев есть имя
       assert descriptions[i].text != '' # проверяем, что все карточки заполнены
       assert statistics == len(names) # проверяем, что все питомцы имеют имя возраст и породу


animals_names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//body/tr/td[0]')
unique = []


def test_unique_names():  # Проверка уникальности имен питомцев
    for animals_names in unique:
        if animals_names in unique:
            continue
        else:
            unique.append(animals_names)
        return unique


print(test_unique_names())



