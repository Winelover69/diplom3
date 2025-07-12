from pages.base_page import BasePage
from utils.locators import LoginPageLocators
import allure
from config import BASE_URL # Импортируем BASE_URL из конфига для формирования полного URL страницы

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Полный URL для страницы логина
        self.url = f"{BASE_URL}login"
        self.locators = LoginPageLocators

    @allure.step("Переход на страницу логина")
    def open_login_page(self):
        """Переходит на страницу логина и ожидает загрузки заголовка."""
        self.open(self.url)
        # Используем новый метод для ожидания видимости
        self.wait_for_visibility_of_element(self.locators.LOGIN_BUTTON_ON_FORM)

    @allure.step("Ввод Email: {email}")
    def enter_email(self, email):
        """Вводит Email в соответствующее поле."""
        # Используем новый метод для ожидания присутствия
        self.wait_for_presence_of_element(self.locators.EMAIL_INPUT).send_keys(email)

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        """Вводит пароль в соответствующее поле."""
        # Используем новый метод для ожидания присутствия
        self.wait_for_presence_of_element(self.locators.PASSWORD_INPUT).send_keys(password)

    @allure.step("Клик по кнопке 'Войти'")
    def click_login_button_on_form(self):
        """Кликает по кнопке 'Войти' и ожидает перехода на главную страницу."""
        # Используем click_element, который уже включает ожидание видимости
        self.click_element(self.locators.LOGIN_BUTTON_ON_FORM)
        # Ожидаем, что URL будет содержать базовый после логина (редирект на главную)
        self.wait_for_url_contains(BASE_URL)

    @allure.step("Выполнение авторизации с Email: {email}")
    def login(self, email, password):
        """Выполняет полную процедуру авторизации."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button_on_form()