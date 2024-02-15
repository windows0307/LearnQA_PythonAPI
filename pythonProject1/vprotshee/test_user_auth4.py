import pytest
import requests
from lib.base_case import BaseCase

class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookies"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # Отправляем POST-запрос для аутентификации пользователя
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        # Проверяем наличие необходимых данных в первом ответе
        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no csrf token headers in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        # Извлекаем необходимые данные для использования во втором запросе
        self.auth_sid = response1.cookies.get("auth_sid")
        self.token = response1.cookies.get("x-csrf-token")
        self.user_id_from_auth_method = response1.json()["user_id"]

    def test_auth_user(self):
        # Отправляем GET-запрос для проверки аутентификации пользователя
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        # Проверяем наличие user_id во втором ответе
        assert "user_id" in response2.json(), "There is no user id in the second response"
        user_id_from_check_method = response2.json()["user_id"]
        print(user_id_from_check_method)

        # Проверяем, что user_id из первого и второго ответов совпадают
        assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookies":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     headers={"x-csrf-token": self.token}
                                     )
        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     headers={"auth_sid": self.auth_sid}
                                     )

        assert "user_id" in response2.json(), "There is no user id in the second response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"
