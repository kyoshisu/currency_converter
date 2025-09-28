from fastapi import FastAPI, HTTPException
from converter import CurrencyConverter
from typing import Optional

app = FastAPI(
    title="Currency Converter API",
    description="RESTful API service for currency conversion",
    version="1.0.0"
)

# Инициализируем конвертер #
converter = CurrencyConverter("exchange_rates.csv")

@app.get("/")
async def root():
    # Корневой эндпоинт для проверки работы сервера #
    return {
        "message": "Currency Converter API is running!",
        "endpoints": {
            "/convert": "Convert currency (GET /convert?from_currency=USD&to_currency=EUR&amount=100)",
            "/history": "Get conversion history (GET /history?limit=10)", 
            "/currencies": "Get available currencies (GET /currencies)",
            "/docs": "API documentation"
        }
    }

@app.get("/convert")
async def convert_currency(from_currency: str, to_currency: str, amount: float):
    # Конвертирует сумму из одной валюты в другую #
    try:
        result = converter.convert(from_currency.upper(), to_currency.upper(), amount)
        return {
            "success": True,
            "data": result
        }
    except ValueError as e:
        error_message = str(e)
        if "не найдена" in error_message or "not found" in error_message.lower():
            return {
                "success": False,
                "error": {
                    "code": "CURRENCY_NOT_FOUND",
                    "message": error_message,
                    "details": f"Available currencies: {', '.join(converter.get_available_currencies())}"
                }
            }
        else:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_AMOUNT",
                    "message": error_message,
                    "details": "Amount must be a positive number"
                }
            }

@app.get("/history")
async def get_history(limit: Optional[int] = None):
    # Возвращает историю операций конвертации #
    history = converter.get_history(limit)
    return {
        "success": True,
        "data": {
            "operations": history,
            "total_count": len(converter.history)
        }
    }

@app.get("/currencies")
async def get_currencies():
    # Возвращает список доступных валют #
    currencies = converter.get_available_currencies()
    return {
        "success": True,
        "data": {
            "currencies": currencies,
            "total_currencies": len(currencies)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8008, reload=True)
