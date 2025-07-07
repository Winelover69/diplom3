# ui_tests/pages/main_page.py

from pages.base_page import BasePage
from utils.locators import MainPageLocators
# import logging # Если вы используете локальный логгер для этой страницы, раскомментируйте

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO) # или DEBUG
# Если вы уже настроили корневой логгер в conftest или где-то еще,
# то этот логгер будет использовать его конфигурацию.

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Уникальный путь для этой страницы
        self.path = "/"
        # Локаторы этой страницы можно сохранить в атрибуте, если нужно,
        # но обычно они доступны через импорт.
        self.locators = MainPageLocators


    @allure.step("Переход на главную страницу")
    def go_to_main_page(self):
        """Переходит на главную страницу и ожидает загрузки заголовка конструктора."""
        self.open(self.path) # Используем self.path
        self.wait_for_visibility(self.locators.BURGER_CONSTRUCTOR_TITLE)
        # logger.info("Переход на главную страницу выполнен.") # Если используете локальный логгер

    @allure.step("Клик по кнопке 'Конструктор'")
    def click_constructor_button(self):
        """Кликает по кнопке 'Конструктор' и ожидает перехода на главную страницу."""
        self.click_element(self.locators.CONSTRUCTOR_BUTTON)
        self.wait_for_url_change(self.path) # URL главной страницы
        # logger.info("Клик по кнопке 'Конструктор' выполнен.")

    @allure.step("Клик по кнопке 'Лента заказов'")
    def click_order_feed_button(self):
        """Кликает по кнопке 'Лента заказов' и ожидает перехода на соответствующую страницу."""
        self.click_element(self.locators.ORDER_FEED_BUTTON)
        self.wait_for_url_change("/feed")
        # logger.info("Клик по кнопке 'Лента заказов' выполнен.")

    @allure.step("Клик по кнопке 'Личный Кабинет'")
    def click_profile_button(self):
        """Кликает по кнопке 'Личный Кабинет' и ожидает перехода на страницу логина."""
        self.click_element(self.locators.PROFILE_BUTTON)
        self.wait_for_url_change("/login")
        # logger.info("Клик по кнопке 'Личный Кабинет' выполнен.")

    @allure.step("Клик по кнопке 'Войти в аккаунт' на главной странице")
    def click_login_on_main_page_button(self):
        """Кликает по кнопке 'Войти в аккаунт' на главной странице и ожидает перехода на страницу логина."""
        self.click_element(self.locators.LOGIN_BUTTON_ON_MAIN_PAGE)
        self.wait_for_url_change("/login")
        # logger.info("Клик по кнопке 'Войти в аккаунт' на главной странице выполнен.")

    @allure.step("Клик по ингредиенту: {ingredient_name}")
    def click_ingredient(self, ingredient_name):
        """Кликает по указанному ингредиенту и ожидает появления модального окна деталей."""
        self.click_element(self.locators.get_ingredient_card_locator(ingredient_name))
        self.wait_for_visibility(self.locators.INGREDIENT_DETAILS_MODAL_TITLE)
        # logger.info(f"Клик по ингредиенту '{ingredient_name}' выполнен.")

    @allure.step("Проверка отображения модального окна деталей ингредиента")
    def is_ingredient_details_modal_displayed(self):
        """Проверяет, отображается ли модальное окно деталей ингредиента."""
        is_displayed = False
        try:
            is_displayed = self.find_element(self.locators.INGREDIENT_DETAILS_MODAL_TITLE, timeout=3).is_displayed()
            # logger.info("Модальное окно деталей ингредиента отображается.")
        except AssertionError:
            # logger.info("Модальное окно деталей ингредиента не отображается.")
            pass # Если элемент не найден, find_element уже логгирует ошибку.
        return is_displayed


    @allure.step("Закрытие модального окна")
    def close_modal(self):
        """Закрывает активное модальное окно."""
        self.click_element(self.locators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_to_be_invisible(self.locators.INGREDIENT_DETAILS_MODAL_TITLE)
        # logger.info("Модальное окно закрыто.")

    @allure.step("Получение значения счетчика ингредиента: {ingredient_name}")
    def get_ingredient_counter_value(self, ingredient_name):
        """Возвращает значение счетчика для указанного ингредиента."""
        counter_locator = self.locators.get_ingredient_counter_locator(ingredient_name)
        value = 0
        try:
            counter_element = self.wait_for_visibility(counter_locator, timeout=2)
            value = int(counter_element.text)
            # logger.info(f"Счетчик ингредиента '{ingredient_name}' равен: {value}")
        except AssertionError:
            # logger.info(f"Счетчик ингредиента '{ingredient_name}' отсутствует или равен 0.")
            pass # Если элемент не найден, find_element уже логгирует ошибку.
        return value

    @allure.step("Добавление ингредиента '{ingredient_name}' в бургер")
    def add_ingredient_to_burger(self, ingredient_name):
        """Перетаскивает ингредиент в область конструктора бургера."""
        source_locator = self.locators.get_ingredient_card_locator(ingredient_name)
        target_locator = self.locators.BURGER_BUILDER_DROP_AREA
        self.drag_and_drop(source_locator, target_locator)
        # logger.info(f"Ингредиент '{ingredient_name}' добавлен в бургер.")

    @allure.step("Клик по кнопке 'Оформить заказ'")
    def click_order_button(self):
        """Кликает по кнопке 'Оформить заказ' и ожидает появления модального окна номера заказа."""
        self.click_element(self.locators.ORDER_BUTTON)
        self.wait_for_visibility(self.locators.ORDER_NUMBER_MODAL_TEXT)
        # logger.info("Клик по кнопке 'Оформить заказ' выполнен.")

    @allure.step("Получение номера заказа из модального окна")
    def get_order_number_from_modal(self):
        """Извлекает номер заказа из модального окна."""
        order_number = self.get_text(self.locators.ORDER_NUMBER_DISPLAY)
        # logger.info(f"Получен номер заказа из модального окна: {order_number}")
        return order_number

    @allure.step("Ожидание исчезновения модального окна с номером заказа")
    def wait_for_order_modal_to_disappear(self):
        """Ожидает, пока модальное окно с номером заказа исчезнет."""
        self.wait_for_element_to_be_invisible(self.locators.ORDER_NUMBER_MODAL_TEXT)
        # logger.info("Модальное окно с номером заказа исчезло.")