import pytest
import requests
import os

BASE_URL = "http://localhost:8008"

def is_ci_environment():
    # Проверяем, запущены ли тесты в CI/CD среде #
    return os.getenv('GITHUB_ACTIONS') == 'true'

class TestCurrencyConverterAPI:
    # Тесты для API конвертера валют #

    def test_root_endpoint(self):
        # Тест корневого эндпоинта #
        if is_ci_environment():
            pytest.skip("Skipping API test in CI environment - server not available")

        response = requests.get(BASE_URL)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data

    def test_convert_currency_success(self):
        # Тест успешной конвертации валют #
        if is_ci_environment():
            pytest.skip("Skipping API test in CI environment - server not available")

        response = requests.get(f"{BASE_URL}/convert?from_currency=USD&to_currency=EUR&amount=100")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert data["data"]["from_currency"] == "USD"
        assert data["data"]["to_currency"] == "EUR"
        assert data["data"]["amount"] == 100.0

    def test_convert_currency_invalid_currency(self):
        # Тест конвертации с несуществующей валютой #
        if is_ci_environment():
            pytest.skip("Skipping API test in CI environment - server not available")

        response = requests.get(f"{BASE_URL}/convert?from_currency=USD&to_currency=XYZ&amount=100")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] == False
        assert "error" in data
        assert data["error"]["code"] == "CURRENCY_NOT_FOUND"

    def test_get_history_success(self):
        # Тест получения истории операций #
        if is_ci_environment():
            pytest.skip("Skipping API test in CI environment - server not available")

        requests.get(f"{BASE_URL}/convert?from_currency=USD&to_currency=EUR&amount=100")

        response = requests.get(f"{BASE_URL}/history")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "operations" in data["data"]

    def test_get_currencies_success(self):
        # Тест получения списка валют #
        if is_ci_environment():
            pytest.skip("Skipping API test in CI environment - server not available")

        response = requests.get(f"{BASE_URL}/currencies")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "currencies" in data["data"]
        assert "USD" in data["data"]["currencies"]

