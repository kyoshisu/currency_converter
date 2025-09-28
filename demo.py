from converter import CurrencyConverter

def main():
    # Создаем экземпляр конвертера #
    print("=== Демонстрация работы конвертера валют ===\n")
    
    try:
        converter = CurrencyConverter("exchange_rates.csv")
        
        # Демонстрация конвертации #
        print("1. Конвертация 100 USD в EUR:")
        result1 = converter.convert("USD", "EUR", 100)
        print(f"   Результат: {result1['amount']} {result1['from_currency']} = {result1['result']} {result1['to_currency']}")
        print(f"   Курс: 1 {result1['from_currency']} = {result1['rate']} {result1['to_currency']}")
        
        print("\n2. Конвертация 50 EUR в GBP:")
        result2 = converter.convert("EUR", "GBP", 50)
        print(f"   Результат: {result2['amount']} {result2['from_currency']} = {result2['result']} {result2['to_currency']}")
        
        print("\n3. Конвертация 10000 JPY в USD:")
        result3 = converter.convert("JPY", "USD", 10000)
        print(f"   Результат: {result3['amount']} {result3['from_currency']} = {result3['result']} {result3['to_currency']}")
        
        # Демонстрация истории операций #
        print("\n4. История операций (все):")
        history = converter.get_history()
        for i, op in enumerate(history, 1):
            print(f"   {i}. {op['timestamp'][11:19]} | {op['amount']} {op['from_currency']} → {op['result']} {op['to_currency']}")
        
        print("\n5. Доступные валюты:")
        print(f"   {', '.join(converter.get_available_currencies())}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
