# ui_tests/fixtures/user_api_fixtures.py

import pytest
import allure
import logging
from api.client import ApiClient  # Убедитесь, что путь к api.client корректен
from data.test_data import generate_random_email, generate_random_password, \
    generate_random_name  # Импортируем из data.test_data

# Настройка логгера для этого модуля фикстур
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Установите нужный уровень логирования
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:  # Избегаем добавления обработчика несколько раз при повторных запусках тестов
    logger.addHandler(handler)


@pytest.fixture(scope="module")
def api_client_for_ui_fixtures():
    """
    Фикстура, предоставляющая экземпляр ApiClient для использования в UI-фикстурах.
    Один экземпляр на модуль, так как он stateless.
    """
    return ApiClient()


@pytest.fixture(scope="function")
def registered_user_for_ui(api_client_for_ui_fixtures):
    """
    Фикстура, регистрирующая пользователя перед UI-тестом и удаляющая его после.
    Возвращает данные пользователя и токен доступа.
    """
    email = generate_random_email()
    password = generate_random_password()
    name = generate_random_name()
    token = None  # Инициализируем токен как None

    with allure.step(f"API: Регистрация пользователя для UI теста: {email}"):
        response = api_client_for_ui_fixtures.register_user(email, password, name)

        # Проверка в фикстуре должна быть минимальной, чтобы убедиться,
        # что она вообще смогла подготовить данные.
        # Ассерты на конкретный статус-код 200 лучше делать в тестовых методах API,
        # если вы тестируете саму регистрацию.
        if response.status_code == 200:
            token = response.json().get("accessToken")
            logger.info(f"Пользователь {email} успешно зарегистрирован через API для UI-теста.")
        else:
            # Если регистрация не удалась, это критическая проблема для фикстуры.
            # Используем pytest.fail, чтобы тест не продолжался с невалидными данными.
            logger.error(
                f"Не удалось зарегистрировать пользователя {email} через API для UI-теста. Статус: {response.status_code}, Ответ: {response.text}")
            pytest.fail(f"Фикстура: Не удалось зарегистрировать пользователя через API. Ответ: {response.text}")

    # Yield позволяет выполнить код до теста и после
    yield email, password, name, token

    with allure.step(f"API: Удаление пользователя после UI теста: {email}"):
        if token:
            response = api_client_for_ui_fixtures.delete_user(token)
            if response.status_code == 202:
                logger.info(f"Пользователь {email} успешно удалён через API после UI-теста.")
            else:
                # Если удаление не 202, это может быть 404 (уже удален) или другая ошибка.
                # Логируем как предупреждение, так как основной тест уже завершен.
                logger.warning(
                    f"Не удалось удалить пользователя {email} через API. Статус: {response.status_code}, Ответ: {response.text}")
            # time.sleep(0.5) - Удален, как плохая практика.
            # Если возникнут проблемы с rate-limit, нужно внедрить retry-логику.
        else:
            logger.info(f"Токен для пользователя {email} не был получен в фикстуре, удаление пропущено.")