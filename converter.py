import csv
from datetime import datetime
from typing import List, Dict, Optional


class CurrencyConverter:
    # Класс для конвертации валют и ведения истории операций #

    def __init__(self, rates_file: str = "exchange_rates.csv"):
        # Инициализация конвертера #
        self.rates_file = rates_file
        self.exchange_rates = {}
        self.history = []
        self.load_rates()

    def load_rates(self) -> None:
        # Загружает курсы валют из CSV-файла #
        try:
            with open(self.rates_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    currency = row['currency'].upper()
                    rate = float(row['rate'])
                    self.exchange_rates[currency] = rate
            print(f"Загружены курсы для валют: {list(self.exchange_rates.keys())}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл с курсами валют '{self.rates_file}' не найден")
        except KeyError:
            raise ValueError("CSV-файл должен содержать колонки 'currency' и 'rate'")
        except ValueError as e:
            raise ValueError(f"Ошибка в формате данных CSV-файла: {e}")

    def convert(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, any]:
        # Конвертирует сумму из одной валюты в другую #
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency not in self.exchange_rates:
            raise ValueError(f"Валюта '{from_currency}' не найдена в курсах")
        if to_currency not in self.exchange_rates:
            raise ValueError(f"Валюта '{to_currency}' не найдена в курсах")

        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        from_rate = self.exchange_rates[from_currency]
        to_rate = self.exchange_rates[to_currency]

        result = (amount / from_rate) * to_rate

        operation = {
            'timestamp': datetime.now().isoformat(),
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'result': round(result, 2),
            'rate': round(to_rate / from_rate, 6)
        }

        self.history.append(operation)

        return operation

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, any]]:
        # Возвращает историю операций конвертации #
        recent_history = list(reversed(self.history))
        if limit:
            return recent_history[:limit]
        return recent_history

    def get_available_currencies(self) -> List[str]:
        # Возвращает список доступных валют #
        return list(self.exchange_rates.keys())


