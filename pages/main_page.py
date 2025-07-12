from .base_page import BasePage
from utils.locators import MainPageLocators
import allure
from config import BASE_URL  # Импортируем BASE_URL из конфига


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Полный URL для главной страницы
        self.url = BASE_URL
        self.locators = MainPageLocators

    @allure.step("Переход на главную страницу")
    def open_main_page(self):
        """Переходит на главную страницу и ожидает загрузки заголовка конструктора."""
        self.open(self.url)  # Используем self.url
        self.wait_for_visibility_of_element(self.locators.BURGER_CONSTRUCTOR_TITLE)

    @allure.step("Клик по кнопке 'Конструктор'")
    def click_constructor_button(self):
        """Кликает по кнопке 'Конструктор' и ожидает перехода на главную страницу."""
        self.click_element(self.locators.CONSTRUCTOR_BUTTON)
        self.wait_for_url_contains(self.url)  # URL главной страницы

    @allure.step("Клик по кнопке 'Лента заказов'")
    def click_order_feed_button(self):
        """Кликает по кнопке 'Лента заказов' и ожидает перехода на соответствующую страницу."""
        self.click_element(self.locators.ORDER_FEED_BUTTON)
        self.wait_for_url_contains(f"{BASE_URL}feed")

    @allure.step("Клик по кнопке 'Личный Кабинет'")
    def click_personal_cabinet_button(self):
        """Кликает по кнопке 'Личный Кабинет' и ожидает перехода на страницу логина."""
        self.click_element(self.locators.PERSONAL_CABINET_BUTTON)  # Предполагаем, что локатор тоже изменен
        self.wait_for_url_contains(f"{BASE_URL}login")

    @allure.step("Клик по кнопке 'Войти в аккаунт' на главной странице")
    def click_login_on_main_page_button(self):
        """Кликает по кнопке 'Войти в аккаунт' на главной странице и ожидает перехода на страницу логина."""
        self.click_element(self.locators.LOGIN_BUTTON_ON_MAIN_PAGE)
        self.wait_for_url_contains(f"{BASE_URL}login")

    @allure.step("Клик по ингредиенту: {ingredient_name}")
    def click_ingredient(self, ingredient_name):
        """Кликает по указанному ингредиенту и ожидает появления модального окна деталей."""
        self.click_element(self.locators.get_ingredient_card_locator(ingredient_name))
        self.wait_for_visibility_of_element(self.locators.INGREDIENT_DETAILS_MODAL_TITLE)

    @allure.step("Проверка отображения модального окна деталей ингредиента")
    def is_ingredient_details_modal_displayed(self):
        """Проверяет, отображается ли модальное окно деталей ингредиента."""
        # Используем метод из BasePage, который уже возвращает True/False
        return self.is_element_present(self.locators.INGREDIENT_DETAILS_MODAL_TITLE)

    @allure.step("Закрытие модального окна")
    def close_modal(self):
        """Закрывает активное модальное окно."""
        self.click_element(self.locators.MODAL_CLOSE_BUTTON)
        self.wait_for_invisibility_of_element(self.locators.INGREDIENT_DETAILS_MODAL_TITLE)

    @allure.step("Получение значения счетчика ингредиента: {ingredient_name}")
    def get_ingredient_counter_value(self, ingredient_name):
        """Возвращает значение счетчика для указанного ингредиента. Возвращает 0, если счетчик отсутствует."""
        counter_locator = self.locators.get_ingredient_counter_locator(ingredient_name)

        # Проверяем наличие элемента, чтобы не получить ошибку, если счетчика нет
        if self.is_element_present(counter_locator, timeout=1):  # Короткий таймаут для проверки наличия
            return int(self.get_element_text(counter_locator))
        return 0  # Если счетчика нет, возвращаем 0

    @allure.step("Добавление ингредиента '{ingredient_name}' в бургер")
    def add_ingredient_to_burger(self, ingredient_name):
        """Перетаскивает ингредиент в область конструктора бургера."""
        source_locator = self.locators.get_ingredient_card_locator(ingredient_name)
        target_locator = self.locators.BURGER_BUILDER_DROP_AREA
        self.drag_and_drop(source_locator, target_locator)

    @allure.step("Клик по кнопке 'Оформить заказ'")
    def click_order_button(self):
        """Кликает по кнопке 'Оформить заказ' и ожидает появления модального окна номера заказа."""
        self.click_element(self.locators.ORDER_BUTTON)
        self.wait_for_visibility_of_element(self.locators.ORDER_NUMBER_MODAL_TEXT)

    @allure.step("Получение номера заказа из модального окна")
    def get_order_number_from_modal(self):
        """Извлекает номер заказа из модального окна."""
        return self.get_element_text(self.locators.ORDER_NUMBER_DISPLAY)

    @allure.step("Ожидание исчезновения модального окна с номером заказа")
    def wait_for_order_modal_to_disappear(self):
        """Ожидает, пока модальное окно с номером заказа исчезнет."""
        self.wait_for_invisibility_of_element(self.locators.ORDER_NUMBER_MODAL_TEXT)