from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import allure
import logging
# Импортируем BASE_URL из config.py только в тех местах, где он действительно нужен (например, в тестах или конкретных Page Objects)
# В самом BasePage он не нужен.
from config import TIMEOUT # TIMEOUT используется здесь для общих ожиданий

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
        # base_url удален из BasePage. Он будет определяться в файле config.py
        # и использоваться в Page Objects, которым нужен полный URL.

    @allure.step("Открытие URL: {url}")
    def open(self, url):
        """Открывает заданный URL."""
        self.driver.get(url)
        logger.info(f"Открыт URL: {url}")

    @allure.step("Ожидание присутствия элемента по локатору: {locator}")
    def wait_for_presence_of_element(self, locator, timeout=TIMEOUT):
        """Ожидает присутствия элемента в DOM и возвращает WebElement."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            logger.info(f"Элемент найден по локатору: {locator}")
            return element
        except TimeoutException as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_element_not_present", attachment_type=allure.attachment_type.PNG)
            logger.error(f"Элемент не появился в DOM по локатору {locator} за {timeout} секунд: {e}")
            raise

    @allure.step("Ожидание видимости элемента по локатору: {locator}")
    def wait_for_visibility_of_element(self, locator, timeout=TIMEOUT):
        """Ожидает видимости элемента на странице и возвращает WebElement."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            logger.info(f"Элемент по локатору {locator} стал видимым.")
            return element
        except TimeoutException as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_element_not_visible", attachment_type=allure.attachment_type.PNG)
            logger.error(f"Элемент не стал видимым по локатору {locator} за {timeout} секунд: {e}")
            raise

    @allure.step("Ожидание присутствия всех элементов по локатору: {locator}")
    def wait_for_presence_of_all_elements(self, locator, timeout=TIMEOUT):
        """Ожидает присутствия всех элементов в DOM по заданному локатору и возвращает список WebElement'ов."""
        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
            logger.info(f"Найдены элементы по локатору: {locator}")
            return elements
        except TimeoutException as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_elements_not_present", attachment_type=allure.attachment_type.PNG)
            logger.error(f"Элементы не появились в DOM по локатору {locator} за {timeout} секунд: {e}")
            raise

    @allure.step("Клик по элементу: {locator}")
    def click_element(self, locator, timeout=TIMEOUT):
        """Кликает по элементу по заданному локатору, предварительно дожидаясь его видимости."""
        element = self.wait_for_visibility_of_element(locator, timeout)
        element.click()
        logger.info(f"Выполнен клик по элементу: {locator}")

    @allure.step("Получение текста элемента по локатору: {locator}")
    def get_element_text(self, locator, timeout=TIMEOUT):
        """Получает текстовое содержимое элемента по заданному локатору, предварительно дожидаясь его видимости."""
        text = self.wait_for_visibility_of_element(locator, timeout).text
        logger.info(f"Получен текст '{text}' с элемента по локатору: {locator}")
        return text

    @allure.step("Проверка отсутствия элемента на странице: {locator}")
    def wait_for_invisibility_of_element(self, locator, timeout=TIMEOUT):
        """Ожидает, пока элемент станет невидимым или исчезнет из DOM по заданному локатору."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            logger.info(f"Элемент по локатору {locator} стал невидимым/отсутствующим.")
            return True
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_element_still_visible", attachment_type=allure.attachment_type.PNG)
            logger.warning(f"Элемент по локатору {locator} остался видимым после {timeout} секунд.")
            return False # Возвращаем False, так как это может быть частью сценария, где мы проверяем отсутствие

    @allure.step("Выполнение drag-and-drop от {source_locator} к {target_locator}")
    def perform_drag_and_drop(self, source_locator, target_locator, timeout=TIMEOUT):
        """Выполняет операцию перетаскивания (drag-and-drop) между двумя локаторами."""
        source_element = self.wait_for_presence_of_element(source_locator, timeout)
        target_element = self.wait_for_presence_of_element(target_locator, timeout)
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
    def wait_for_url_contains(self, expected_url_part, timeout=TIMEOUT):
        """Ожидает, пока текущий URL будет содержать заданную подстроку."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(expected_url_part))
            logger.info(f"URL изменился и содержит '{expected_url_part}'.")
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_url_not_changed", attachment_type=allure.attachment_type.PNG)
            logger.error(f"URL не изменился на '{expected_url_part}' за {timeout} секунд. Текущий URL: {self.driver.current_url}")
            raise