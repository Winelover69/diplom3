# ui_tests/pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import allure
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers: # Избегаем добавления обработчика несколько раз
    logger.addHandler(handler)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # base_url остается здесь, так как это корень приложения,
        # от которого строятся все относительные URL.
        self.base_url = "https://stellarburgers.nomoreparties.site"

    @allure.step("Открытие URL: {path}")
    def open(self, path=""):
        """Открывает URL, комбинируя базовый URL и переданный путь."""
        full_url = self.base_url + path
        self.driver.get(full_url)
        logger.info(f"Открыт URL: {full_url}")

    @allure.step("Ожидание и поиск элемента по локатору: {locator}")
    def find_element(self, locator, timeout=10):
        """Ожидает и возвращает WebElement по заданному локатору."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            logger.info(f"Элемент найден по локатору: {locator}")
            return element
        except (TimeoutException, NoSuchElementException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_element_not_found", attachment_type=allure.attachment_type.PNG)
            logger.error(f"Элемент не найден по локатору {locator} за {timeout} секунд: {e}")
            raise AssertionError(f"Элемент не найден по локатору {locator} за {timeout} секунд: {e}")

    @allure.step("Клик по элементу: {locator}")
    def click_element(self, locator, timeout=10):
        """Кликает по элементу по заданному локатору."""
        element = self.find_element(locator, timeout)
        element.click()
        logger.info(f"Выполнен клик по элементу: {locator}")

    @allure.step("Получение текста элемента по локатору: {locator}")
    def get_text(self, locator, timeout=10):
        """Получает текстовое содержимое элемента по заданному локатору."""
        text = self.find_element(locator, timeout).text
        logger.info(f"Получен текст '{text}' с элемента по локатору: {locator}")
        return text

    @allure.step("Ожидание, пока элемент станет видимым: {locator}")
    def wait_for_visibility(self, locator, timeout=10):
        """Ожидает, пока элемент станет видимым по заданному локатору."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            logger.info(f"Элемент по локатору {locator} стал видимым.")
            return element
        except (TimeoutException, NoSuchElementException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_element_not_visible", attachment_type=allure.attachment_type.PNG)
            logger.error(f"Элемент не стал видимым по локатору {locator} за {timeout} секунд: {e}")
            raise AssertionError(f"Элемент не стал видимым по локатору {locator} за {timeout} секунд: {e}")

    @allure.step("Проверка отсутствия элемента: {locator}")
    def wait_for_element_to_be_invisible(self, locator, timeout=10):
        """Ожидает, пока элемент станет невидимым по заданному локатору."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            logger.info(f"Элемент по локатору {locator} стал невидимым.")
            return True
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_element_still_visible", attachment_type=allure.attachment_type.PNG)
            logger.warning(f"Элемент по локатору {locator} остался видимым после {timeout} секунд.")
            return False

    @allure.step("Выполнение drag-and-drop от {source_locator} к {target_locator}")
    def drag_and_drop(self, source_locator, target_locator):
        """Выполняет операцию перетаскивания (drag-and-drop) между двумя локаторами."""
        source_element = self.find_element(source_locator)
        target_element = self.find_element(target_locator)
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_element, target_element).perform()
        logger.info(f"Выполнен drag-and-drop от {source_locator} к {target_locator}.")

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        """Возвращает текущий URL страницы."""
        url = self.driver.current_url
        logger.info(f"Текущий URL: {url}")
        return url

    @allure.step("Ожидание изменения URL на {expected_url_part}")
    def wait_for_url_change(self, expected_url_part, timeout=10):
        """Ожидает, пока текущий URL будет содержать заданную подстроку."""
        try:
            # Если expected_url_part не начинается с '/', добавляем self.base_url
            if not expected_url_part.startswith('/'):
                full_expected_url = self.base_url + expected_url_part
            else:
                full_expected_url = self.base_url + expected_url_part

            WebDriverWait(self.driver, timeout).until(EC.url_contains(full_expected_url))
            logger.info(f"URL изменился на '{full_expected_url}'.")
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_url_not_changed", attachment_type=allure.attachment_type.PNG)
            logger.error(f"URL не изменился на '{full_expected_url}' за {timeout} секунд. Текущий URL: {self.driver.current_url}")
            raise AssertionError(f"URL не изменился на '{full_expected_url}' за {timeout} секунд. Текущий URL: {self.driver.current_url}")