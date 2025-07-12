
import random
import string

def generate_random_email():
    """Генерирует случайный email для тестового пользователя."""
    return f"test_ui_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@example.com"

def generate_random_password():
    """Генерирует случайный пароль для тестового пользователя."""
    return "pass" + ''.join(random.choices(string.digits, k=4))

def generate_random_name():
    """Генерирует случайное имя для тестового пользователя."""
    return "Name" + ''.join(random.choices(string.ascii_letters, k=5))

# Можете добавить сюда другие тестовые данные, если необходимо
INVALID_INGREDIENT_HASHES = ["invalid_hash_1", "invalid_hash_2"] # Пример для API тестов