# ui_tests/pages/login_page.py

from pages.base_page import BasePage
from utils.locators import LoginPageLocators
# import logging

# logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.path = "/login"
        self.locators = LoginPageLocators

    @allure.step("Переход на страницу логина")
    def go_to_login_page(self):
        """Переходит на страницу логина и ожидает загрузки заголовка."""
        self.open(self.path)
        self.wait_for_visibility(self.locators.LOGIN_TITLE)
        # logger.info("Переход на страницу логина выполнен.")

    @allure.step("Ввод Email")
    def enter_email(self, email):
        """Вводит Email в соответствующее поле."""
        self.find_element(self.locators.EMAIL_INPUT).send_keys(email)
        # logger.info(f"Введен Email: {email}")

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        """Вводит пароль в соответствующее поле."""
        self.find_element(self.locators.PASSWORD_INPUT).send_keys(password)
        # logger.info("Введен пароль (скрыто).")

    @allure.step("Клик по кнопке 'Войти'")
    def click_login_button(self):
        """Кликает по кнопке 'Войти' и ожидает перехода на главную страницу."""
        self.click_element(self.locators.LOGIN_BUTTON)
        self.wait_for_url_change("/") # Ожидаем редирект на главную страницу
        # logger.info("Клик по кнопке 'Войти' выполнен. Ожидается редирект на главную.")