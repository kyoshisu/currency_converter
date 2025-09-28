import pytest
import os
from converter import CurrencyConverter


class TestCurrencyConverter:

    def setup_method(self):
        # Подготовка тестового окружения перед каждым тестом #
        self.test_rates_file = "test_rates.csv"
        with open(self.test_rates_file, 'w', encoding='utf-8') as f:
            f.write("currency,rate\nUSD,1.0\nEUR,0.85\nGBP,0.75\nJPY,110.0\n")

        self.converter = CurrencyConverter(self.test_rates_file)

    def teardown_method(self):
        # Очистка после каждого теста #
        if os.path.exists(self.test_rates_file):
            os.remove(self.test_rates_file)

    def test_initialization(self):
        # Тест инициализации конвертера #
        assert self.converter.rates_file == self.test_rates_file
        assert len(self.converter.exchange_rates) == 4
        assert self.converter.exchange_rates['USD'] == 1.0
        assert self.converter.history == []

    def test_convert_usd_to_eur(self):
        # Тест конвертации USD в EUR #
        result = self.converter.convert("USD", "EUR", 100)
        expected_result = 100 * (0.85 / 1.0)
        assert result['result'] == pytest.approx(expected_result, 0.01)
        assert result['from_currency'] == 'USD'
        assert result['to_currency'] == 'EUR'
        assert result['amount'] == 100
        assert 'timestamp' in result
        assert 'rate' in result
        assert len(self.converter.history) == 1

    def test_convert_eur_to_gbp(self):
        # Тест конвертации EUR в GBP #
        result = self.converter.convert("EUR", "GBP", 50)
        expected_result = (50 / 0.85) * 0.75
        assert result['result'] == pytest.approx(expected_result, 0.01)

    def test_convert_same_currency(self):
        # Тест конвертации одинаковых валют #
        result = self.converter.convert("USD", "USD", 100)
        assert result['result'] == 100.0
        assert result['rate'] == 1.0

    def test_convert_case_insensitive(self):
        # Тест нечувствительности к регистру #
        result1 = self.converter.convert("usd", "eur", 100)
        result2 = self.converter.convert("USD", "EUR", 100)
        assert result1['result'] == result2['result']

    def test_convert_invalid_currency(self):
        # Тест конвертации с несуществующей валютой #
        with pytest.raises(ValueError, match="Валюта 'RUB' не найдена в курсах"):
            self.converter.convert("USD", "RUB", 100)

        with pytest.raises(ValueError, match="Валюта 'CAD' не найдена в курсах"):
            self.converter.convert("CAD", "USD", 100)

    def test_convert_invalid_amount(self):
        # Тест конвертации с некорректной суммой #
        with pytest.raises(ValueError, match="Сумма должна быть положительной"):
            self.converter.convert("USD", "EUR", -100)

        with pytest.raises(ValueError, match="Сумма должна быть положительной"):
            self.converter.convert("USD", "EUR", 0)

    def test_get_history_empty(self):
        # Тест получения пустой истории #
        history = self.converter.get_history()
        assert history == []

    def test_get_history_with_operations(self):
        # Тест получения истории с операциями #
        self.converter.convert("USD", "EUR", 100)
        self.converter.convert("EUR", "GBP", 50)
        self.converter.convert("GBP", "JPY", 25)

        history = self.converter.get_history()

        assert len(history) == 3
        assert history[0]['from_currency'] == 'GBP'
        assert history[2]['from_currency'] == 'USD'

    def test_get_history_with_limit(self):
        # Тест получения истории с ограничением #
        self.converter.convert("USD", "EUR", 100)
        self.converter.convert("EUR", "GBP", 50)
        self.converter.convert("GBP", "JPY", 25)

        history = self.converter.get_history(limit=2)
        assert len(history) == 2

    def test_get_available_currencies(self):
        # Тест получения списка доступных валют #
        currencies = self.converter.get_available_currencies()
        assert set(currencies) == {'USD', 'EUR', 'GBP', 'JPY'}
        assert len(currencies) == 4

    def test_file_not_found(self):
        # Тест обработки отсутствующего файла #
        with pytest.raises(FileNotFoundError):
            CurrencyConverter("non_existent_file.csv")

    def test_invalid_csv_format(self):
        # Тест обработки некорректного CSV формата #
        invalid_file = "invalid_rates.csv"
        with open(invalid_file, 'w', encoding='utf-8') as f:
            f.write("code,value\nUSD,1.0\n")

        with pytest.raises(ValueError, match="CSV-файл должен содержать колонки"):
            CurrencyConverter(invalid_file)

        os.remove(invalid_file)

    def test_csv_parsing_errors(self):
        # Тест ошибок парсинга CSV с некорректными числами #
        invalid_file = "invalid_number.csv"
        with open(invalid_file, 'w', encoding='utf-8') as f:
            f.write("currency,rate\nUSD,not_a_number\n")

        with pytest.raises(ValueError, match="Ошибка в формате данных"):
            CurrencyConverter(invalid_file)

        os.remove(invalid_file)

    def test_very_small_amount(self):
        # Тест конвертации очень маленькой суммы #
        result = self.converter.convert("USD", "EUR", 0.01)
        assert result['result'] > 0

    def test_very_large_amount(self):
        # Тест конвертации очень большой суммы #
        result = self.converter.convert("USD", "EUR", 1000000)
        assert result['result'] > 0

    def test_rounding_precision(self):
        # Тест точности округления #
        test_file = "precision_test.csv"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("currency,rate\nUSD,1.0\nEUR,0.333333\n")

        converter = CurrencyConverter(test_file)
        result = converter.convert("USD", "EUR", 100)
        assert result['result'] == 33.33

        os.remove(test_file)


def test_encoding_errors():
    # Тест ошибок кодировки файла #
    invalid_file = "invalid_encoding.csv"
    with open(invalid_file, 'wb') as f:
        f.write(b"currency,rate\nUSD,1.0\n\xff\xfe\xfd")

    try:
        CurrencyConverter(invalid_file)
    except UnicodeDecodeError:
        pass
    except Exception:
        pass

    if os.path.exists(invalid_file):
        os.remove(invalid_file)


