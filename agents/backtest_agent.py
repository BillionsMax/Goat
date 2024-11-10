import pandas as pd
import logging
from agents.data_agent import DataAgent
from agents.trading_agent import TradingAgent
from agents.risk_agent import RiskAgent

class BacktestAgent:
    def __init__(self):
        self.data_agent = DataAgent()
        self.trading_agent = TradingAgent()
        self.risk_agent = RiskAgent()
        self.initial_balance = 10000  # Начальный баланс для бэктестинга
        self.balance = self.initial_balance
        self.positions = []

    def backtest(self, symbol, timeframe, start_date, end_date):
        # Загрузка исторических данных за заданный период
        logging.info(f"Загрузка исторических данных для {symbol} с {start_date} по {end_date}")
        data = self.data_agent.get_data(symbol, timeframe)
        df = pd.DataFrame(data)
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]

        for index, row in df.iterrows():
            last_close = row['close']
            try:
                signal = self.trading_agent.generate_signal(df.iloc[:index + 1])
            except Exception as e:
                logging.error(f"Ошибка при генерации сигнала для {symbol}: {e}")
                continue

            if signal == "buy":
                stop_loss, take_profit = self.trading_agent.calculate_levels(last_close)
                quantity = round(self.risk_agent.calculate_risk(self.balance, last_close, stop_loss), 4)
                self.positions.append((symbol, "BUY", quantity, last_close))
                self.balance -= quantity * last_close
                logging.info(f"Buy {symbol} at {last_close}, Stop Loss at {stop_loss}, Take Profit at {take_profit}")
            elif signal == "sell" and self.positions:
                for position in self.positions:
                    if position[1] == "BUY":
                        profit = (last_close - position[3]) * position[2]
                        self.balance += position[2] * last_close + profit
                        logging.info(f"Sell {symbol} at {last_close}, Profit: {profit}")
                        self.positions.remove(position)

        logging.info(f"Итоговый баланс после бэктестинга: {self.balance}")