# ui_tests/pages/register_page.py

from pages.base_page import BasePage
from utils.locators import RegisterPageLocators
# import logging

# logger = logging.getLogger(__name__)

class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.path = "/register"
        self.locators = RegisterPageLocators

    @allure.step("Переход на страницу регистрации")
    def go_to_register_page(self):
        """Переходит на страницу регистрации и ожидает загрузки заголовка."""
        self.open(self.path)
        self.wait_for_visibility(self.locators.REGISTER_TITLE)
        # logger.info("Переход на страницу регистрации выполнен.")

    @allure.step("Ввод имени: {name}")
    def enter_name(self, name):
        """Вводит имя в соответствующее поле."""
        self.find_element(self.locators.NAME_INPUT).send_keys(name)
        # logger.info(f"Введено имя: {name}")

    @allure.step("Ввод Email: {email}")
    def enter_email(self, email):
        """Вводит Email в соответствующее поле."""
        self.find_element(self.locators.EMAIL_INPUT).send_keys(email)
        # logger.info(f"Введен Email: {email}")

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        """Вводит пароль в соответствующее поле."""
        self.find_element(self.locators.PASSWORD_INPUT).send_keys(password)
        # logger.info("Введен пароль (скрыто).")

    @allure.step("Клик по кнопке 'Зарегистрироваться'")
    def click_register_button(self):
        """Кликает по кнопке 'Зарегистрироваться' и ожидает перехода на страницу логина."""
        self.click_element(self.locators.REGISTER_BUTTON)
        self.wait_for_url_change("/login")
        # logger.info("Клик по кнопке 'Зарегистрироваться' выполнен. Ожидается редирект на страницу логина.")

    @allure.step("Проверка отображения ошибки 'Некорректный пароль'")
    def is_invalid_password_error_displayed(self):
        """Проверяет, отображается ли сообщение об ошибке некорректного пароля."""
        is_displayed = False
        try:
            is_displayed = self.find_element(self.locators.INVALID_PASSWORD_ERROR, timeout=3).is_displayed()
            # logger.info("Ошибка 'Некорректный пароль' отображается.")
        except AssertionError:
            # logger.info("Ошибка 'Некорректный пароль' не отображается.")
            pass
        return is_displayed

    @allure.step("Клик по ссылке 'Войти'")
    def click_login_link(self):
        """Кликает по ссылке 'Войти' и ожидает перехода на страницу логина."""
        self.click_element(self.locators.LOGIN_LINK)
        self.wait_for_url_change("/login")
        # logger.info("Клик по ссылке 'Войти' выполнен.")