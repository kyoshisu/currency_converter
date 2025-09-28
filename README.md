### 🔗 Swagger
**[📖 OpenAPI on SwaggerHub](https://app.swaggerhub.com/apis/tyumgu/currency-converter/1.0.0#/)**

### Основные эндпоинты

- **GET** `/convert?from=USD&to=EUR&amount=100` - Конвертация валют
- **GET** `/history?limit=5` - История операций конвертации
- **GET** `/currencies` - Список доступных валют

### Примеры использования

```bash
# Конвертация 100 USD в EUR
curl "http://localhost:8008/convert?from=USD&to=EUR&amount=100"

# Получение последних 5 операций
curl "http://localhost:8008/history?limit=5"

# Получение списка валют
curl "http://localhost:8008/currencies"