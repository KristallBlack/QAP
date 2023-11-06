from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос API ключа возвращает статус 200 и в результате содержится слово key."""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user_successful(email=invalid_email, password=invalid_password):
    """Проверяем негативный тест-кейс, что запрос API ключа с незарегистрированными на платформе данными пользователя
    (email, password) не возвращает статуса = 200, а ответ (результат) сервера не содержит ключа 'key'."""

    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result


def test_get_all_pets_list(filter=''):
    """Проверяем позитивный тест-кейс, что запрос всех питомцев возвращает не пустой список. Для этого сначала получаем api ключ и
    сохраняем в переменную auth_key. Далее используя этого ключ запрашиваем список всех питомцев и проверяем,
    что список не пустой. Доступное значение параметра filter - 'my_pets' либо ''"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


# блок POST-запросов:


def test_add_new_pet_with_valid_data(name='Бука', animal_type='невская маскарадная',
                                     age='6', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно создать карточку питомца с полными (включая фотографию), корректными данными."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_data(name='', animal_type='', age='', pet_photo='images/cat1.jpg'):
    """Проверяем негативный тест-кейс в случае, когда запрос на добавление питомца содержит некорректные
    параметры (обязательные для заполнения пустые значения). Если система отказывает в запросе - негативный тест-кейс
    пройден. Если система все-таки добавляет карточку питомца с невалидными данными - вызываем исключение и создаем
    баг-репорт."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    if status == 200 and 'name' in result:
        raise Exception('Обнаружена ошибка - возможность создания карточки питомца с пустыми полями.')
    else:
        assert status != 200
        assert 'name' not in result

        # GET-запрос:


def test_get_my_pets_list(filter='my_pets'):
    """ Проверяем работу запроса при выбранном параметре фильтра - 'my_pets', который выводит список питомцев,
    добавленных пользователем. Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее,
    используя этот ключ, запрашиваем список своих питомцев и проверяем, что список не пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

    # блок POST-запросов:


def test_update_pet_foto_jpg(pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить фото питомца в ранее созданную карточку в валидном формате
     c расширением xxx.jpg."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_foto(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception('Добавленные вами питомцы в списке отсутствуют.')


def test_update_pet_foto_invalid_bmp(pet_photo='images/cat2.bmp'):
    """Проверяем негативный тест-кейс в случае, когда фото питомца передаётся в невалидном формате графического
    файла c расширением xxx.bmp (в соответствии с требованиями API-документации PetFriends API v1). Если
    система отказывает в запросе - негативный тест-кейс пройден. Если система добавляет в карточку фото
    питомца с некорректным форматом файла - вызываем исключение и создаем баг-репорт."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.update_pet_foto(auth_key, my_pets['pets'][0]['id'], pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if status == 200 and result['pet_photo'] == my_pets['pets'][0]['pet_photo']:
        raise Exception('Error')
    else:
        assert status != 200
        assert result['pet_photo'] != my_pets['pets'][0]['pet_photo']

        # блок POST-запросов:


def test_add_new_pet_simple(name='Боб', animal_type='немецкая овчарка', age=2.2):
    """Проверяем возможность добавления базовых данных о питомце без фото."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_simple_invalid_age_data_type(name='Боб', animal_type='немецкая овчкарка', age='три'):
    """Проверяем негативный тест-кейс в случае, когда передаваемое значение переменной age в запросе имеет строковый
    (str) тип данных, тогда как в соответствии с требованиями API-документации PetFriends API v1 значение параметра age
    должно принимать тип данных числа(number). Если система отказывает в запросе - негативный тест-кейс
    пройден. Если система все-таки создает простую карточку питомца с неверным типом переданных данных - вызываем
    исключение и создаем баг-репорт."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    if status == 200 and result['name'] == name:
        raise Exception('Error')
    else:
        assert status != 200
        assert result['name'] != name


def test_add_new_pet_simple_invalid_breed_data_type(name='Боб', animal_type=543, age=30):
    """Проверяем негативный тест-кейс в случае, когда передаваемое значение переменной animal_type в запросе имеет
    числовой (number) тип данных, тогда как в соответствии с требованиями API-документации PetFriends API v1 значение
    параметра animal_type должно принимать строчный тип данных (string). Если система отказывает в запросе -
    негативный тест-кейс пройден. Если система все-таки создает простую карточку питомца с неверным типом
    переданных данных - вызываем исключение и создаем баг-репорт."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    if status == 200 and result['name'] == name:
        raise Exception('Error')
    else:
        assert status != 200
        assert result['name'] != name


def test_add_new_pet_simple_invalid_age_value(name='Боб', animal_type=123, age='999999999999999999999999'):
    """Проверяем негативный тест-кейс в случае, когда переменная age в запросе передает системе любое
     значение из цифр, что будет не соответствовать реальной продолжительности жизни животного.
    Если система отказывает в запросе - негативный тест-кейс пройден. Если система все-таки создает простую
    карточку питомца с неверным типом переданных данных - вызываем исключение и создаем баг-репорт."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    if status == 200 and result['name'] == name:
        raise Exception('Error')
    else:
        assert status != 200
        assert result['name'] != name

        # DELETE-запрос:


def test_successful_delete_self_pet():
    """Проверяем позитивный тест-кейс на возможность удаления питомца из списка"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Лео", "брауни", "10", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

    # блок PUT-запросов:


def test_successful_update_self_pet_info(name='Superstar', animal_type='туреций ван', age=12.2):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no pets')


def test_update_self_pet_invalid_age_value(name='Рыжий', animal_type='полосатый', age=9999999999999999999):
    """Проверяем негативный тест-кейс в случае, когда переменная age в запросе передает системе любое
    значение из цифр, что будет не соответствовать реальной продолжительности жизни любого животного на земле :).
    Если система отказывает в запросе - негативный тест-кейс пройден. Если система все-таки обновляет карточку
    питомца некорректными данными - вызываем исключение и создаем баг-репорт."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    if status == 200 and result['name'] == name:
        raise Exception('Error')
    else:
        assert status != 200
        assert result['name'] != name


def test_update_self_pet_invalid_breed_data_type(name='Котенок', animal_type=657, age=3):
    """Проверяем негативный тест-кейс в случае, когда передаваемое значение переменной animal_type в запросе имеет
    числовой (number) тип данных, тогда как в соответствии с требованиями API-документации PetFriends API v1 значение
    параметра animal_type должно принимать строчный тип данных (string). Если система отказывает в запросе - негативный
     тест-кейс пройден. Если система обновляет карточку питомца некорректными данными - вызываем исключение
      и создаем баг-репорт."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    if status == 200 and result['name'] == name:
        raise Exception('Error')
    else:
        assert status != 200
        assert result['name'] != name


def test_update_self_pet_invalid_age_data_type(name='Гарфилд', animal_type='толстик', age='три'):
    """Проверяем негативный тест-кейс в случае, когда передаваемое значение переменной age в запросе имеет строковый
    (str) тип данных, тогда как в соответствии с требованиями API-документации PetFriends API v1 значение параметра age
    должно принимать тип данных числа(number). Если система отказывает в запросе - негативный тест-кейс
    пройден. Если система создает простую карточку питомца с неверным типом переданных данных - вызываем
    исключение и создаем баг-репорт."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    if status == 200 and result['name'] == name:
        raise Exception('Error')
    else:
        assert status != 200
        assert result['name'] != name