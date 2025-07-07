import pytest
import allure
from ui_tests.pages.main_page import MainPage
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.register_page import RegisterPage
from ui_tests.pages.order_feed_page import OrderFeedPage


# Если у вас есть другие импорты Page Objects, добавьте их здесь
# from ui_tests.pages.profile_page import ProfilePage


@allure.epic("UI Stellar Burgers")
@allure.feature("Main Page Functionality")
class TestMainPageFunctionality:

    @allure.title("Переход по клику на 'Конструктор'")
    @allure.description("Проверяет, что клик по кнопке 'Конструктор' на других страницах возвращает на главную.")
    def test_constructor_button_redirects_to_main_page(self, driver):
        main_page = MainPage(driver)

        with allure.step("Переход на страницу 'Лента заказов'"):
            main_page.open("/feed")  # Используем open с относительным путем
            # Убеждаемся, что мы на ленте заказов
            assert "feed" in main_page.get_current_url()

        with allure.step("Клик по кнопке 'Конструктор'"):
            main_page.click_constructor_button()  # Этот метод уже содержит wait_for_url_change("/")

        with allure.step("Проверка, что текущий URL - главная страница"):
            # Вместо driver.current_url используем метод из Page Object
            assert main_page.get_current_url() == main_page.base_url + main_page.path
            # Или, что более надёжно, если click_constructor_button не содержит проверку URL:
            # main_page.wait_for_url_change(main_page.path) # Проверяем изменение URL
            # assert main_page.get_current_url() == main_page.base_url + main_page.path

    @allure.title("Переход по клику на 'Лента заказов'")
    @allure.description("Проверяет, что клик по кнопке 'Лента заказов' переводит на соответствующую страницу.")
    def test_order_feed_button_redirects_to_feed_page(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)  # Создаем объект для страницы ленты заказов

        with allure.step("Переход на главную страницу"):
            main_page.go_to_main_page()  # Открываем главную страницу через Page Object

        with allure.step("Клик по кнопке 'Лента заказов'"):
            main_page.click_order_feed_button()  # Этот метод уже содержит wait_for_url_change("/feed")

        with allure.step("Проверка, что текущий URL - страница 'Лента заказов'"):
            # Используем get_current_url() из Page Object
            assert order_feed_page.get_current_url() == order_feed_page.base_url + order_feed_page.path
            # Или более надежно:
            # order_feed_page.wait_for_url_change(order_feed_page.path)
            # assert order_feed_page.get_current_url() == order_feed_page.base_url + order_feed_page.path

    @allure.title("Клик по ингредиенту открывает модальное окно с деталями")
    @allure.description("Проверяет, что при клике на ингредиент открывается модальное окно с его деталями.")
    def test_click_ingredient_opens_modal(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()

        with allure.step("Клик по первому ингредиенту 'Флюоресцентная булка R2-D3'"):
            # Убедитесь, что 'Флюоресцентная булка R2-D3' соответствует названию на сайте
            main_page.click_ingredient("Флюоресцентная булка R2-D3")

        with allure.step("Проверка, что модальное окно деталей ингредиента отображается"):
            assert main_page.is_ingredient_details_modal_displayed()

        with allure.step("Закрытие модального окна"):
            main_page.close_modal()
            assert not main_page.is_ingredient_details_modal_displayed()

    @allure.title("Добавление ингредиента в бургер через drag-and-drop увеличивает счетчик")
    @allure.description("Проверяет, что перетаскивание ингредиента в конструктор увеличивает его счетчик.")
    def test_drag_and_drop_ingredient_increases_counter(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()

        ingredient_name = "Мясо бессмертных моллюсков Protostomia"  # Пример ингредиента
        initial_counter_value = main_page.get_ingredient_counter_value(ingredient_name)

        with allure.step(f"Перетаскивание ингредиента '{ingredient_name}' в конструктор"):
            main_page.add_ingredient_to_burger(ingredient_name)

        with allure.step("Проверка, что счетчик ингредиента увеличился"):
            updated_counter_value = main_page.get_ingredient_counter_value(ingredient_name)
            assert updated_counter_value == initial_counter_value + 1

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверяет успешное создание заказа авторизованным пользователем.")
    def test_create_order_authorized_user(self, driver, registered_user_for_ui):
        email, password, _, token = registered_user_for_ui  # Получаем данные зарегистрированного пользователя
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        with allure.step("Авторизация пользователя"):
            login_page.go_to_login_page()
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login_button()
            # Убедимся, что мы на главной странице после логина
            assert main_page.get_current_url() == main_page