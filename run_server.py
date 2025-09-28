# Скрипт для запуска HTTP-сервера #

import uvicorn
from server import app

if __name__ == "__main__":
    print("🚀 Starting Currency Converter API Server...")
    print("📍 Server URL: http://localhost:8008")
    print("📚 API Documentation: http://localhost:8008/docs")
    print("🛣️  Available endpoints:")
    print("   GET /convert?from=USD&to=EUR&amount=100")
    print("   GET /history?limit=10")
    print("   GET /currencies")
    print("   GET /docs - Interactive API documentation")
    print("⏹️  Press Ctrl+C to stop the server\n")

    uvicorn.run("server:app", host="0.0.0.0", port=8008, reload=False)
