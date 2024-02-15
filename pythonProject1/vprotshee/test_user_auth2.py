import pytest
import requests


class TestUserAuth:
    def test_auth_user(self):
        data = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        # Отправляем POST-запрос для аутентификации пользователя
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        # Проверяем наличие необходимых данных в первом ответе
        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no csrf token headers in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        # Извлекаем необходимые данные для использования во втором запросе
        auth_sid = response1.cookies.get("auth_sid")
        token = response1.cookies.get("x-csrf-token")
        user_id_from_auth_method = response1.json()["user_id"]

        # Отправляем GET-запрос для проверки аутентификации пользователя
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверяем наличие user_id во втором ответе
        assert "user_id" in response2.json(), "There is no user id in the second response"
        user_id_from_check_method = response2.json()["user_id"]
        print(user_id_from_check_method)

        # Проверяем, что user_id из первого и второго ответов совпадают
        assert user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

    exclude_params = [
        ("no_cookies"),
        ("no_token")
    ]
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
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
        auth_sid = response1.cookies.get("auth_sid")
        token = response1.cookies.get("x-csrf-token")

        if condition == "no_cookies":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": token}
            )
        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                headers={"auth_sid": auth_sid}
            )

        assert "user_id" in response2.json(), "There is no user id in the second response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"
