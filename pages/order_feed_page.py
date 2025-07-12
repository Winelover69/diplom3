# pages/order_feed_page.py
from pages.base_page import BasePage
from utils.locators import OrderFeedPageLocators
import allure
import logging
from config import BASE_URL  # Импортируем BASE_URL

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)


class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Указываем полный URL для этой страницы, используя BASE_URL из config
        self.url = f"{BASE_URL}feed"
        self.locators = OrderFeedPageLocators

    @allure.step("Переход на страницу 'Лента заказов'")
    def open_feed_page(self):
        """Переходит на страницу 'Лента заказов' и ожидает загрузки заголовка."""
        self.open(self.url)
        # Используем обновленный метод из BasePage
        self.wait_for_visibility_of_element(self.locators.FEED_TITLE)
        logger.info("Переход на страницу 'Лента заказов' выполнен.")

    @allure.step("Получение значения счетчика 'Выполнено за всё время'")
    def get_total_orders_count(self):
        """Возвращает значение счетчика 'Выполнено за всё время'."""
        # Используем обновленный метод из BasePage
        counter_value = int(self.get_element_text(self.locators.TOTAL_ORDERS_COUNTER_VALUE))
        logger.info(f"Значение счетчика 'Выполнено за всё время': {counter_value}")
        return counter_value

    @allure.step("Получение значения счетчика 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        """Возвращает значение счетчика 'Выполнено за сегодня'."""
        # Используем обновленный метод из BasePage
        counter_value = int(self.get_element_text(self.locators.TODAY_ORDERS_COUNTER_VALUE))
        logger.info(f"Значение счетчика 'Выполнено за сегодня': {counter_value}")
        return counter_value

    @allure.step("Получение списка номеров заказов в разделе 'В работе'")
    def get_orders_in_progress_numbers(self):
        """Возвращает список номеров заказов, находящихся в разделе 'В работе'."""
        # Используем метод из BasePage для ожидания присутствия всех элементов
        # и получения их текста.
        order_elements_texts = self.get_elements_text_list(self.locators.ORDERS_IN_PROGRESS_LIST)
        orders = [elem.replace("#", "") for elem in order_elements_texts if elem.strip()]
        logger.info(f"Номера заказов в разделе 'В работе': {orders}")
        return orders

    @allure.step("Ожидание появления хотя бы одного заказа в разделе 'В работе'")
    def wait_for_any_order_in_progress(self):
        """Ожидает появления хотя бы одного заказа в списке 'В работе'."""
        # Используем wait_for_visibility_of_element из BasePage
        self.wait_for_visibility_of_element(self.locators.ANY_ORDER_IN_PROGRESS)
        logger.info("Хотя бы один заказ в разделе 'В работе' отобразился.")

    @allure.step("Клик по первому заказу в ленте")
    def click_first_order_in_feed(self):
        """Кликает по первому заказу в ленте и ожидает появления деталей."""
        self.click_element(self.locators.FIRST_ORDER_IN_FEED)
        # Используем обновленный метод из BasePage
        self.wait_for_visibility_of_element(self.locators.ORDER_DETAILS_MODAL_TITLE)
        logger.info("Клик по первому заказу в ленте выполнен.")

    @allure.step("Получение номера первого заказа в ленте")
    def get_first_order_number_in_feed(self):
        """Возвращает номер первого заказа в ленте."""
        # Используем обновленный метод из BasePage
        order_number_text = self.get_element_text(self.locators.FIRST_ORDER_IN_FEED_NUMBER)
        order_number = order_number_text.replace("#", "")
        logger.info(f"Номер первого заказа в ленте: {order_number}")
        return order_number

    @allure.step("Проверка отображения модального окна деталей заказа")
    def is_order_details_modal_displayed(self):
        """Проверяет, отображается ли модальное окно деталей заказа."""
        # Используем is_element_present из BasePage, который возвращает True/False
        # и уже инкапсулирует try/except, чтобы Page Object был чище.
        is_displayed = self.is_element_present(self.locators.ORDER_DETAILS_MODAL_TITLE)
        if is_displayed:
            logger.info("Модальное окно деталей заказа отображается.")
        else:
            logger.info("Модальное окно деталей заказа не отображается.")
        return is_displayed

    @allure.step("Закрытие модального окна деталей заказа")
    def close_order_details_modal(self):
        """Закрывает модальное окно деталей заказа."""
        self.click_element(self.locators.MODAL_CLOSE_BUTTON)
        # Используем обновленный метод из BasePage
        self.wait_for_invisibility_of_element(self.locators.ORDER_DETAILS_MODAL_TITLE)
        logger.info("Модальное окно деталей заказа закрыто.")