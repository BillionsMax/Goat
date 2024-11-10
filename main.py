from strategies.goat_strategy import GOATStrategy
from utils.data_loader import fetch_historical_data, parse_data
from utils.risk_management import apply_risk_management
from utils.trade_executor import execute_order
import config
import requests
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataAgent:
    def __init__(self):
        pass

    def get_data(self, symbol, timeframe):
        try:
            raw_data = fetch_historical_data(symbol, timeframe)
            if not raw_data or len(raw_data) < 2:
                raise ValueError(f"Недостаточно данных для {symbol}")
            return parse_data(raw_data)
        except Exception as e:
            logging.error(f"Ошибка при получении данных для {symbol}: {e}")
            return []  # Возвращаем пустой список в случае ошибки


class TradingAgent:
    def __init__(self):
        self.strategy = GOATStrategy(
            risk_reward_ratio=config.STRATEGY_PARAMETERS["risk_reward_ratio"],
            max_loss=config.STRATEGY_PARAMETERS["max_loss"]
        )

    def generate_signal(self, data):
        return self.strategy.generate_signal(data)

    def calculate_levels(self, last_close):
        stop_loss = self.strategy.calculate_stop_loss(last_close)
        take_profit = self.strategy.calculate_take_profit(last_close)
        return stop_loss, take_profit


class RiskAgent:
    def calculate_risk(self, balance, last_close, stop_loss):
        return apply_risk_management(balance, last_close, stop_loss)


class ExecutorAgent:
    def execute_trade(self, symbol, side, quantity):
        execute_order(symbol, side, quantity)


class MonitoringAgent:
    def __init__(self):
        self.positions = {}

    def update_position(self, symbol, side, quantity):
        if side == "BUY":
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        elif side == "SELL":
            self.positions[symbol] = self.positions.get(symbol, 0) - quantity
        if self.positions[symbol] == 0:
            del self.positions[symbol]

    def log_positions(self):
        logging.info(f"Текущие позиции: {self.positions}")


def get_top_200_symbols():
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
        logging.info("Список топ-200 криптовалют успешно загружен.")
        return symbols
    else:
        logging.error("Ошибка при получении данных с CoinGecko API")
        return []


def process_trade(symbol, signal, last_close, trading_agent, risk_agent, executor_agent, monitoring_agent):
    stop_loss, take_profit = trading_agent.calculate_levels(last_close)
    direction = "BUY" if signal == "buy" else "SELL"
    logging.info(f"{direction} {symbol} at {last_close}, Stop Loss at {stop_loss}, Take Profit at {take_profit}")

    quantity = risk_agent.calculate_risk(1000, last_close, stop_loss)
    if quantity > 0:
        executor_agent.execute_trade(symbol, direction, quantity)
        monitoring_agent.update_position(symbol, direction, quantity)
        logging.info(f"Сделка {direction} выполнена: символ={symbol}, объем={quantity}")
    else:
        logging.warning(f"Объем сделки для {symbol} равен нулю, сделка не выполнена.")


def main():
    data_agent = DataAgent()
    trading_agent = TradingAgent()
    risk_agent = RiskAgent()
    executor_agent = ExecutorAgent()
    monitoring_agent = MonitoringAgent()

    symbols = get_top_200_symbols()

    for symbol in symbols:
        logging.info(f"Анализируем {symbol}...")

        try:
            data = data_agent.get_data(symbol, config.STRATEGY_PARAMETERS["timeframe"])
            if not data:
                logging.warning(f"Данные не были загружены для {symbol}. Пропуск.")
                continue
        except Exception as e:
            logging.error(f"Неожиданная ошибка при загрузке данных для {symbol}: {e}")
            continue

        try:
            signal = trading_agent.generate_signal(data)
            last_close = data[-1]['close']
        except Exception as e:
            logging.error(f"Ошибка при генерации сигнала для {symbol}: {e}")
            continue

        if signal in ["buy", "sell"]:
            process_trade(symbol, signal, last_close, trading_agent, risk_agent, executor_agent, monitoring_agent)
        else:
            logging.info(f"Hold {symbol}")

        monitoring_agent.log_positions()
        time.sleep(1)


if __name__ == "__main__":
    main()
