# ui_tests/pages/order_feed_page.py

from pages.base_page import BasePage
from utils.locators import OrderFeedPageLocators
from selenium.webdriver.common.by import By  # Понадобится для find_elements, так как это множественный поиск
import allure
import logging

# Настройка логгера (если она не централизована через conftest)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Установите нужный уровень логирования
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)


class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init > (driver)
        self.path = "/feed"
        self.locators = OrderFeedPageLocators

    @allure.step("Переход на страницу 'Лента заказов'")
    def go_to_order_feed_page(self):
        """Переходит на страницу 'Лента заказов' и ожидает загрузки заголовка."""
        self.open(self.path)
        self.wait_for_visibility(self.locators.ORDER_FEED_TITLE)
        logger.info("Переход на страницу 'Лента заказов' выполнен.")

    @allure.step("Получение значения счетчика 'Выполнено за всё время'")
    def get_total_orders_counter(self):
        """Возвращает значение счетчика 'Выполнено за всё время'."""
        counter_value = int(self.get_text(self.locators.TOTAL_ORDERS_COUNTER))
        logger.info(f"Значение счетчика 'Выполнено за всё время': {counter_value}")
        return counter_value

    @allure.step("Получение значения счетчика 'Выполнено за сегодня'")
    def get_today_orders_counter(self):
        """Возвращает значение счетчика 'Выполнено за сегодня'."""
        counter_value = int(self.get_text(self.locators.TODAY_ORDERS_COUNTER))
        logger.info(f"Значение счетчика 'Выполнено за сегодня': {counter_value}")
        return counter_value

    @allure.step("Получение списка номеров заказов в разделе 'В работе'")
    def get_orders_in_progress_numbers(self):
        """Возвращает список номеров заказов, находящихся в разделе 'В работе'."""
        # --- ИСПРАВЛЕНО ЗДЕСЬ ---
        # Ожидаем, что хотя бы один элемент из списка "В работе" появится.
        # Используем метод из BasePage для ожидания видимости.
        self.wait_for_visibility(self.locators.ANY_ORDER_IN_PROGRESS)

        # После того, как элемент стал видимым (страница загрузилась),
        # можно безопасно найти все элементы.
        # Здесь мы используем self.driver.find_elements, т.к. BasePage предоставляет
        # find_element для одиночного элемента, а здесь нужен список.
        # Если бы BasePage имел метод вроде 'find_elements_multiple', то использовали бы его.
        order_elements = self.driver.find_elements(By.XPATH, self.locators.ORDERS_IN_PROGRESS_LIST_XPATH_RAW)
        # --- КОНЕЦ ИСПРАВЛЕНИЯ ---

        orders = [elem.text.replace("#", "") for elem in order_elements if elem.text.strip()]
        logger.info(f"Номера заказов в разделе 'В работе': {orders}")
        return orders

    @allure.step("Клик по первому заказу в ленте")
    def click_first_order_in_feed(self):
        """Кликает по первому заказу в ленте и ожидает появления деталей."""
        self.click_element(self.locators.FIRST_ORDER_IN_FEED)
        self.wait_for_visibility(self.locators.ORDER_DETAILS_MODAL_TITLE)
        logger.info("Клик по первому заказу в ленте выполнен.")

    @allure.step("Получение номера первого заказа в ленте")
    def get_first_order_number_in_feed(self):
        """Возвращает номер первого заказа в ленте."""
        # Поскольку мы уже ожидаем видимость элементов в get_orders_in_progress_numbers,
        # здесь можно просто получить текст первого элемента.
        order_number_element = self.find_element(self.locators.FIRST_ORDER_IN_FEED_NUMBER)
        order_number = order_number_element.text.replace("#", "")
        logger.info(f"Номер первого заказа в ленте: {order_number}")
        return order_number

    @allure.step("Проверка отображения модального окна деталей заказа")
    def is_order_details_modal_displayed(self):
        """Проверяет, отображается ли модальное окно деталей заказа."""
        is_displayed = False
        try:
            is_displayed = self.find_element(self.locators.ORDER_DETAILS_MODAL_TITLE, timeout=3).is_displayed()
            logger.info("Модальное окно деталей заказа отображается.")
        except AssertionError:
            logger.info("Модальное окно деталей заказа не отображается.")
        return is_displayed

    @allure.step("Закрытие модального окна деталей заказа")
    def close_order_details_modal(self):
        """Закрывает модальное окно деталей заказа."""
        self.click_element(self.locators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_to_be_invisible(self.locators.ORDER_DETAILS_MODAL_TITLE)
        logger.info("Модальное окно деталей заказа закрыто.")