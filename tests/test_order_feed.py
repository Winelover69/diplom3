import pytest
import allure
from pages.main_page import MainPage # Обновленный импорт
from pages.login_page import LoginPage # Обновленный импорт
from pages.feed_page import OrderFeedPage # Обновленный импорт
from config import BASE_URL # Импортируем BASE_URL
# from ui_tests.pages.profile_page import ProfilePage # Если используется, оставить

@allure.epic("UI Stellar Burgers")
@allure.feature("Order Feed Functionality")
class TestOrderFeed:

    @allure.title("Заказ авторизованного пользователя появляется в общей ленте")
    @allure.description(
        "Проверяет, что после создания авторизованным пользователем заказа он появляется в общей ленте.")
    def test_authorized_order_appears_in_feed(self, driver, registered_user_for_ui):
        email, password, _, _ = registered_user_for_ui # token не используется в UI тестах напрямую
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Авторизация пользователя"):
            login_page.open_login_page() # Используем новый метод open_login_page
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login_button_on_form() # Используем новый метод click_login_button_on_form
            # Проверяем, что произошел редирект на главную страницу после логина
            assert main_page.get_current_url() == BASE_URL, \
                f"URL после логина не соответствует ожидаемому: {main_page.get_current_url()}"

        with allure.step("Получение начального значения счетчика 'Выполнено за всё время'"):
            # Перед созданием заказа, переходим на ленту, чтобы получить начальное значение
            order_feed_page.open_feed_page() # Используем новый метод open_feed_page
            initial_total_orders = order_feed_page.get_total_orders_count() # Используем новый метод
            allure.attach(f"Начальное значение 'Выполнено за всё время': {initial_total_orders}", name="Начальный счетчик", attachment_type=allure.attachment_type.TEXT)
            # Возвращаемся на главную для создания заказа
            main_page.open(BASE_URL) # Открываем главный URL

        with allure.step("Добавление ингредиентов и создание заказа"):
            # Здесь должны быть методы для добавления ингредиентов в ConstructorPage,
            # а не в MainPage. Предполагаем, что main_page сейчас является ConstructorPage.
            # Для чистоты примера, использую существующие методы:
            main_page.add_ingredient_to_burger("Краторная булка N-200i") # Этот метод должен быть в ConstructorPage
            main_page.add_ingredient_to_burger("Соус Spicy-X")         # Этот метод должен быть в ConstructorPage
            main_page.click_order_button()                             # Кнопка оформления заказа на MainPage/ConstructorPage
            order_number = main_page.get_order_number_from_modal()     # Этот метод должен быть в ConstructorPage
            main_page.close_modal()                                    # Этот метод должен быть в ConstructorPage
            main_page.wait_for_order_modal_to_disappear()              # Этот метод должен быть в ConstructorPage
            assert order_number.isdigit() and int(order_number) > 0, "Не удалось получить корректный номер заказа."
            allure.attach(f"Создан заказ №{order_number}", name="Номер созданного заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Переход на страницу 'Лента заказов' и проверка обновления счетчиков"):
            order_feed_page.open_feed_page() # Снова открываем ленту
            updated_total_orders = order_feed_page.get_total_orders_count() # Получаем обновленное значение
            allure.attach(f"Обновленное значение 'Выполнено за всё время': {updated_total_orders}", name="Обновленный счетчик", attachment_type=allure.attachment_type.TEXT)
            assert updated_total_orders == initial_total_orders + 1, "Счетчик 'Выполнено за всё время' не увеличился на 1."

            # Проверяем, что номер заказа появился в общей ленте
            # Мы ожидаем, что заказ будет, поэтому ждем его появления.
            order_feed_page.wait_for_any_order_in_progress() # Ждем, что хотя бы один заказ появится
            orders_in_feed = order_feed_page.get_orders_in_progress_numbers() # Получаем список всех заказов
            assert order_number in orders_in_feed, \
                f"Заказ #{order_number} не появился в общей ленте заказов. Актуальные заказы: {orders_in_feed}"

    @allure.title("Заказ авторизованного пользователя появляется в 'Истории заказов' в Личном Кабинете")
    @allure.description(
        "Проверяет, что после создания авторизованным пользователем заказа он появляется в 'Истории заказов'.")
    def test_authorized_order_appears_in_profile_history(self, driver, registered_user_for_ui):
        email, password, _, _ = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver) # Используем для проверки URL, пока нет ProfilePage

        # Предположим, у вас есть ProfilePage, тогда:
        # profile_page = ProfilePage(driver)

        with allure.step("Авторизация пользователя"):
            login_page.open_login_page()
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login_button_on_form()
            assert main_page.get_current_url() == BASE_URL, \
                f"URL после логина не соответствует ожидаемому: {main_page.get_current_url()}"

        with allure.step("Добавление ингредиентов и создание заказа"):
            # Предполагаем методы ConstructorPage, как и выше.
            main_page.add_ingredient_to_burger("Краторная булка N-200i")
            main_page.add_ingredient_to_burger("Соус Spicy-X")
            main_page.click_order_button()
            order_number = main_page.get_order_number_from_modal()
            main_page.close_modal()
            main_page.wait_for_order_modal_to_disappear()
            assert order_number.isdigit() and int(order_number) > 0, "Не удалось получить корректный номер заказа."
            allure.attach(f"Создан заказ №{order_number}", name="Номер созданного заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Переход в 'Личный Кабинет' -> 'История заказов'"):
            main_page.click_personal_cabinet_button() # Используем click_personal_cabinet_button из MainPage
            # Теперь ожидаем, что URL будет содержать '/account/orders'
            # Вместо wait_for_url_change("/account/orders")
            order_feed_page.wait_for_url_contains(f"{BASE_URL}account/orders") # Используем wait_for_url_contains из BasePage
            assert order_feed_page.get_current_url() == f"{BASE_URL}account/orders", \
                f"URL после перехода в историю заказов не соответствует ожидаемому: {order_feed_page.get_current_url()}"

        with allure.step("Проверка, что номер заказа появился в 'Истории заказов'"):
            # Проверяем наличие заказа в истории. Предполагаем, что OrderFeedPage
            # может работать с элементами истории заказа или же будет ProfilePage.
            # Пока используем методы OrderFeedPage, как если бы это был тот же механизм ленты.
            order_feed_page.wait_for_any_order_in_progress() # Ждем, что хотя бы один заказ появится
            orders_in_history = order_feed_page.get_orders_in_progress_numbers() # Получаем список
            assert order_number in orders_in_history, \
                f"Заказ #{order_number} не появился в истории заказов пользователя. Найдены: {orders_in_history}"

    @allure.title("Заказы из общей ленты открывают модальное окно с деталями")
    @allure.description("Проверяет, что при клике на заказ в общей ленте открывается модальное окно с его деталями.")
    def test_order_in_feed_opens_modal(self, driver):
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.open_feed_page()

        # Тест предполагает, что в ленте УЖЕ ЕСТЬ заказы.
        # Если их нет, то get_orders_in_progress_numbers выбросит исключение (TimeoutException)
        # через wait_for_presence_of_all_elements в BasePage, и тест упадет.
        # Это правильное поведение, указывающее на проблему с предусловиями теста.
        with allure.step("Получение номера первого заказа в ленте"):
            orders_in_feed = order_feed_page.get_orders_in_progress_numbers() # Этот метод сам ожидает наличия элементов
            assert len(orders_in_feed) > 0, "В ленте заказов отсутствуют элементы для проверки модального окна."
            first_order_number = orders_in_feed[0]
            allure.attach(f"Найден первый заказ в ленте: {first_order_number}", name="Первый заказ", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Клик по первому заказу в ленте"):
            # click_first_order_in_feed уже ожидает появления модалки
            order_feed_page.click_first_order_in_feed()

        with allure.step("Проверка, что модальное окно деталей заказа отображается"):
            # is_order_details_modal_displayed уже использует is_element_present
            assert order_feed_page.is_order_details_modal_displayed(), \
                "Модальное окно деталей заказа не отображается после клика по заказу."

        with allure.step("Закрытие модального окна деталей заказа"):
            order_feed_page.close_order_details_modal()
            # Проверяем, что модальное окно исчезло, используя метод, который возвращает True/False
            assert not order_feed_page.is_order_details_modal_displayed(), \
                "Модальное окно деталей заказа не закрылось."

    @allure.title("Заказ авторизованного пользователя отображается в разделе 'В работе' в общей ленте")
    @allure.description(
        "Проверяет, что созданный авторизованным пользователем заказ отображается в разделе 'В работе' в общей ленте заказов.")
    def test_authorized_order_appears_in_in_progress_section(self, driver, registered_user_for_ui):
        email, password, _, _ = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Авторизация пользователя"):
            login_page.open_login_page()
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login_button_on_form()
            assert main_page.get_current_url() == BASE_URL, \
                f"URL после логина не соответствует ожидаемому: {main_page.get_current_url()}"

        with allure.step("Добавление ингредиентов и создание заказа"):
            # Предполагаем методы ConstructorPage
            main_page.add_ingredient_to_burger("Краторная булка N-200i")
            main_page.add_ingredient_to_burger("Соус Spicy-X")
            main_page.click_order_button()
            order_number = main_page.get_order_number_from_modal()
            main_page.close_modal()
            main_page.wait_for_order_modal_to_disappear()
            assert order_number.isdigit() and int(order_number) > 0, "Не удалось получить корректный номер заказа."
            allure.attach(f"Создан заказ №{order_number}", name="Номер созданного заказа", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Переход на страницу 'Лента заказов'"):
            order_feed_page.open_feed_page()

        with allure.step(f"Проверка, что заказ #{order_number} появился в секции 'В работе'"):
            # Мы ожидаем, что заказ появится, поэтому ждем его.
            order_feed_page.wait_for_any_order_in_progress() # Ждем, что хоть какой-то заказ появится
            orders_in_progress = order_feed_page.get_orders_in_progress_numbers() # Получаем список всех заказов
            assert order_number in orders_in_progress, \
                f"Заказ #{order_number} не найден в списке 'В работе'. Найдены: {orders_in_progress}"