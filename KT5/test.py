
import requests
import pytest
import allure

from pydantic import BaseModel, Field, ConfigDict


class User(BaseModel):
    id: int
    username: str
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: str
    password: str
    phone: str
    user_status: int = Field(default=1, alias='userStatus')


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str | None = Field(default=None, alias='firstName')
    last_name: str | None = Field(default=None, alias='lastName')
    email: str | None = None
    phone: str | None = None
    user_status: int | None = Field(default=None, alias='userStatus')


class Order(BaseModel):
    id: int
    pet_id: int = Field(alias='petId')
    quantity: int
    ship_date: str = Field(alias='shipDate')
    status: str
    complete: bool


class Api:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    @allure.step('Отправка {method} запроса: {endpoint}')
    def request(self, method, endpoint, body=None, params=None):
        response = self.session.request(
            method=method,
            url=f'{self.base_url}/{endpoint.lstrip("/")}',
            json=body,
            params=params,
            timeout=15
        )

        allure.attach(
            response.request.url,
            name='Request URL',
            attachment_type=allure.attachment_type.TEXT
        )

        if body:
            allure.attach(
                str(body),
                name='Request Body',
                attachment_type=allure.attachment_type.JSON
            )

        try:
            response_body = response.json()
        except ValueError:
            response_body = response.text

        allure.attach(
            str(response_body),
            name='Response Body',
            attachment_type=allure.attachment_type.JSON
            if isinstance(response_body, dict)
            else allure.attachment_type.TEXT
        )

        return response.status_code, response_body

    def post(self, endpoint, body):
        return self.request('POST', endpoint, body=body)

    def get(self, endpoint, params=None):
        return self.request('GET', endpoint, params=params)

    def put(self, endpoint, body):
        return self.request('PUT', endpoint, body=body)

    def delete(self, endpoint):
        return self.request('DELETE', endpoint)


@pytest.fixture(scope='session')
def api():
    return Api('https://petstore.swagger.io/v2')


@pytest.fixture
def test_user():
    return User(
        id=1001,
        username='test_user',
        firstName='Test',
        lastName='User',
        email='test@example.com',
        password='password',
        phone='1234567890',
        userStatus=1
    )


@pytest.fixture
def test_order():
    return Order(
        id=1,
        petId=1,
        quantity=2,
        shipDate='2024-01-01T00:00:00.000Z',
        status='placed',
        complete=False
    )


@allure.feature('Users')
class TestUsers:

    @allure.title('Создание пользователя')
    @allure.story('Create user')
    def test_create_user(self, api, test_user):
        status, body = api.post(
            'user',
            test_user.model_dump(by_alias=True)
        )

        assert status == 200

    @allure.title('Получение пользователя по username')
    @allure.story('Get user')
    def test_get_user_by_name(self, api, test_user):
        status, body = api.get(f'user/{test_user.username}')

        assert status == 200

        user = UserResponse.model_validate(body)

        assert user.username == test_user.username

    @allure.title('Авторизация пользователя')
    @allure.story('Login user')
    def test_login_user(self, api):
        status, body = api.get(
            'user/login',
            params={
                'username': 'test_user_qa',
                'password': 'password'
            }
        )

        assert status == 200
        assert isinstance(body, dict)

    @allure.title('Выход пользователя из системы')
    @allure.story('Logout user')
    def test_logout_user(self, api):
        status, body = api.get('user/logout')
        assert status == 200


@allure.feature('Store')
class TestStore:
    @allure.title('Получение инвентаря магазина')
    @allure.story('Get inventory')
    def test_get_inventory(self, api):
        status, body = api.get('store/inventory')

        assert status == 200
        assert isinstance(body, dict)

    @allure.title('Создание заказа')
    @allure.story('Create order')
    def test_place_order(self, api, test_order):
        status, body = api.post(
            'store/order',
            test_order.model_dump(
                by_alias=True,
                mode='json'
            )
        )

        assert status == 200
        assert body['id'] == test_order.id
        assert body['status'] == test_order.status

    @allure.title('Получение заказа по ID')
    @allure.story('Get order')
    def test_get_order_by_id(self, api, test_order):
        status, body = api.get(
            f'store/order/{test_order.id}'
        )

        assert status == 200
        assert body['id'] == test_order.id

    @allure.title('Удаление заказа')
    @allure.story('Delete order')
    def test_delete_order(self, api, test_order):
        status, body = api.delete(f'store/order/{test_order.id}')
        assert status == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--alluredir=allure-results'])