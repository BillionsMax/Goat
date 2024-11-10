# test_ticker_24hr.py

import asyncio
from binance import AsyncClient

async def test_ticker_24hr():
    # Используйте реальные API ключи или переменные окружения для безопасности
    client = await AsyncClient.create('55MF7bhBzn95uLzBycJaeClFCy29ktSGW37VaeaztTasBAQSa7KDGrNzongOoPUV', 'D31Gcp2BlV8OSb67qZ2cp2fqc2Yq9m2fp3Jy4ZQp0KO51kmRwqbxgtlebDUShfKd')
    try:
        tickers = await client.ticker_24hr()
        print(tickers[:5])  # Вывод первых 5 тикеров для проверки
    except AttributeError as e:
        print(f"Метод отсутствует: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        await client.close_connection()

asyncio.run(test_ticker_24hr())
