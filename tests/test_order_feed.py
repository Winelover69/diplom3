# ui_tests/tests/test_order_feed.py

import pytest
import allure
from ui_tests.pages.main_page import MainPage
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.order_feed_page import OrderFeedPage


# from ui_tests.pages.profile_page import ProfilePage # Если используется

@allure.epic("UI Stellar Burgers")
@allure.feature("Order Feed Functionality")
class TestOrderFeed:

    @allure.title("Заказ авторизованного пользователя появляется в общей ленте")
    @allure.description(
        "Проверяет, что после создания авторизованным пользователем заказа он появляется в общей ленте.")
    def test_authorized_order_appears_in_feed(self, driver, registered_user_for_ui):
        email, password, _, token = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Авторизация пользователя"):
            login_page.go_to_login_page()
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login_button()
            assert main_page.get_current_url() == main_page.base_url + main_page.path

        with allure.step("Получение начального значения счетчика 'Выполнено за всё время'"):
            # Перед созданием заказа, переходим на ленту, чтобы получить начальное значение
            order_feed_page.go_to_order_feed_page()
            initial_total_orders = order_feed_page.get_total_orders_counter()
            # Возвращаемся на главную для создания заказа
            main_page.go_to_main_page()

        with allure.step("Добавление ингредиентов и создание заказа"):
            main_page.add_ingredient_to_burger("Краторная булка N-200i")
            main_page.add_ingredient_to_burger("Соус Spicy-X")
            main_page.click_order_button()
            order_number = main_page.get_order_number_from_modal()
            main_page.close_modal()
            main_page.wait_for_order_modal_to_disappear()
            assert order_number.isdigit() and int(order_number) > 0, "Не удалось получить корректный номер заказа."

        with allure.step("Переход на страницу 'Лента заказов' и проверка обновления счетчиков"):
            order_feed_page.go_to_order_feed_page()
            updated_total_orders = order_feed_page.get_total_orders_counter()
            assert updated_total_orders == initial_total_orders + 1, "Счетчик 'Выполнено за всё время' не увеличился."

            # --- ИСПРАВЛЕНО ЗДЕСЬ ---
            # Проверяем, что номер заказа появился в общей ленте через метод Page Object
            order_feed_page.wait_for_order_number_in_feed(order_number)
            # Добавим дополнительный assert для явной проверки
            assert order_feed_page.is_order_number_present_in_feed(order_number), \
                f"Заказ #{order_number} не появился в общей ленте заказов."
            # --- КОНЕЦ ИСПРАВЛЕНИЯ ---

    @allure.title("Заказ авторизованного пользователя появляется в 'Истории заказов' в Личном Кабинете")
    @allure.description(
        "Проверяет, что после создания авторизованным пользователем заказа он появляется в 'Истории заказов'.")
    def test_authorized_order_appears_in_profile_history(self, driver, registered_user_for_ui):
        email, password, name, token = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)  # Для получения номера заказа в ленте, если нужно

        # Предположим, у вас есть ProfilePage
        # profile_page = ProfilePage(driver)

        with allure.step("Авторизация пользователя"):
            login_page.go_to_login_page()
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login_button()
            assert main_page.get_current_url() == main_page.base_url + main_page.path

        with allure.step("Добавление ингредиентов и создание заказа"):
            main_page.add_ingredient_to_burger("Краторная булка N-200i")
            main_page.add_ingredient_to_burger("Соус Spicy-X")
            main_page.click_order_button()
            order_number = main_page.get_order_number_from_modal()
            main_page.close_modal()
            main_page.wait_for_order_modal_to_disappear()
            assert order_number.isdigit() and int(order_number) > 0, "Не удалось получить корректный номер заказа."

        with allure.step("Переход в 'Личный Кабинет' -> 'История заказов'"):
            main_page.click_profile_button()  # Предполагаем, что этот метод ведет в профиль
            # Если у вас есть ProfilePage, то здесь будет:
            # profile_page.go_to_profile_page()
            # profile_page.click_order_history()
            # Здесь должно быть ожидание загрузки истории заказов

            # Временно, пока нет ProfilePage:
            # Ожидаем, что текущий URL изменится на /account/orders
            order_feed_page.wait_for_url_change("/account/orders")
            assert order_feed_page.get_current_url() == order_feed_page.base_url + "/account/orders"

        with allure.step("Проверка, что номер заказа появился в 'Истории заказов'"):
            # Предположим, что у вас есть метод в ProfilePage или OrderFeedPage для этой проверки
            # Пока нет ProfilePage, используем OrderFeedPage для проверки видимости элемента,
            # но это не идеально с точки зрения ответственности Page Object.
            # Если появится ProfilePage, перенести туда.
            order_feed_page.wait_for_order_number_in_feed(order_number)  # Повторно используем метод
            assert order_feed_page.is_order_number_present_in_feed(order_number), \
                f"Заказ #{order_number} не появился в истории заказов пользователя."

    @allure.title("Заказы из общей ленты открывают модальное окно с деталями")
    @allure.description("Проверяет, что при клике на заказ в общей ленте открывается модальное окно с его деталями.")
    def test_order_in_feed_opens_modal(self, driver):
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.go_to_order_feed_page()

        with allure.step("Получение номера первого заказа в ленте (если есть)"):
            first_order_number = None
            try:
                # Убедимся, что заказы присутствуют
                orders_in_feed = order_feed_page.get_orders_in_progress_numbers()  # Этот метод может быть пустым, если нет заказов
                if orders_in_feed:
                    first_order_number = orders_in_feed[0]
                    logger.info(f"Найден первый заказ в ленте: {first_order_number}")
                else:
                    pytest.skip("Нет заказов в ленте для проверки модального окна.")
            except AssertionError:  # Если get_orders_in_progress_numbers упадет из-за отсутствия элементов
                pytest.skip("Нет заказов в ленте для проверки модального окна.")

        with allure.step("Клик по первому заказу в ленте"):
            order_feed_page.click_first_order_in_feed()  # Этот метод уже ждет модалку

        with allure.step("Проверка, что модальное окно деталей заказа отображается"):
            assert order_feed_page.is_order_details_modal_displayed()

        with allure.step("Закрытие модального окна деталей заказа"):
            order_feed_page.close_order_details_modal()
            assert not order_feed_page.is_order_details_modal_displayed()  # Явный assert на исчезновение

    @allure.title("Заказ авторизованного пользователя отображается в разделе 'В работе' в общей ленте")
    @allure.description(
        "Проверяет, что созданный авторизованным пользователем заказ отображается в разделе 'В работе' в общей ленте заказов.")
    def test_authorized_order_appears_in_in_progress_section(self, driver, registered_user_for_ui):
        email, password, _, token = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Авторизация пользователя"):
            login_page.go_to_login_page()
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login_button()
            assert main_page.get_current_url() == main_page.base_url + main_page.path

        with allure.step("Добавление ингредиентов и создание заказа"):
            main_page.add_ingredient_to_burger("Краторная булка N-200i")
            main_page.add_ingredient_to_burger("Соус Spicy-X")
            main_page.click_order_button()
            order_number = main_page.get_order_number_from_modal()
            main_page.close_modal()
            main_page.wait_for_order_modal_to_disappear()
            assert order_number.isdigit() and int(order_number) > 0, "Не удалось получить корректный номер заказа."

        with allure.step("Переход на страницу 'Лента заказов'"):
            order_feed_page.go_to_order_feed_page()

        with allure.step(f"Проверка, что заказ #{order_number} появился в секции 'В работе'"):
            # Используем get_orders_in_progress_numbers для получения списка
            # и явно проверяем наличие нашего заказа
            order_feed_page.wait_for_order_number_in_feed(order_number)  # Убедимся, что он появился
            orders_in_progress = order_feed_page.get_orders_in_progress_numbers()
            assert order_number in orders_in_progress, \
                f"Заказ #{order_number} не найден в списке 'В работе'. Найдены: {orders_in_progress}"