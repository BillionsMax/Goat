from strategies.goat_strategy import GOATStrategy
from utils.data_loader import fetch_historical_data, parse_data
from utils.risk_management import apply_risk_management
from utils.trade_executor import execute_order
import config
import requests
import time


def get_top_200_symbols():
    # Получение списка топ-200 криптовалют по рыночной капитализации с CoinGecko API
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 200,
        'page': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        symbols = [coin['symbol'].upper() + 'USDT' for coin in data if coin['symbol'].upper() != 'USDT']
        return symbols
    else:
        print("Ошибка при получении данных с CoinGecko API")
        return []


def main():
    # Получение списка топ-200 монет для анализа
    symbols = get_top_200_symbols()

    for symbol in symbols:
        print(f"Анализируем {symbol}...")

        # Загрузка исторических данных
        try:
            raw_data = fetch_historical_data(symbol, config.STRATEGY_PARAMETERS["timeframe"])
            # Проверка, что данные корректные и не пустые
            if not raw_data or len(raw_data) < 2:
                print(f"Недостаточно данных для {symbol}")
                continue
            data = parse_data(raw_data)
        except ValueError as e:
            print(f"Ошибка при обработке данных для {symbol}: {e}")
            continue
        except Exception as e:
            print(f"Неожиданная ошибка при обработке данных для {symbol}: {e}")
            continue

        # Инициализация стратегии
        goat = GOATStrategy(
            risk_reward_ratio=config.STRATEGY_PARAMETERS["risk_reward_ratio"],
            max_loss=config.STRATEGY_PARAMETERS["max_loss"]
        )

        # Генерация сигнала
        try:
            signal = goat.generate_signal(data)
            last_close = data[-1]['close']
        except Exception as e:
            print(f"Ошибка при генерации сигнала для {symbol}: {e}")
            continue

        # Определение стоп-лосса и тейк-профита
        if signal == "buy":
            stop_loss = goat.calculate_stop_loss(last_close)
            take_profit = goat.calculate_take_profit(last_close)
            print(f"Buy {symbol} at {last_close}, Stop Loss at {stop_loss}, Take Profit at {take_profit}")
            # Пример сделки
            execute_order(symbol, "BUY", quantity=0.01)  # указать подходящее количество
        elif signal == "sell":
            stop_loss = goat.calculate_stop_loss(last_close)
            take_profit = goat.calculate_take_profit(last_close)
            print(f"Sell {symbol} at {last_close}, Stop Loss at {stop_loss}, Take Profit at {take_profit}")
            # Пример сделки
            execute_order(symbol, "SELL", quantity=0.01)
        else:
            print(f"Hold {symbol}")

        # Пауза для предотвращения частых запросов к API
        time.sleep(1)


if __name__ == "__main__":
    main()


---------------------------------------------------------------------

