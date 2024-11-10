import pandas as pd
import logging
from datetime import datetime
from binance.client import Client

class DataLoader:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(self.api_key, self.api_secret)

    def load_from_csv(self, file_path):
        """
        Загрузка данных из CSV-файла.
        """
        try:
            data = pd.read_csv(file_path)
            logging.info("Данные загружены из CSV-файла.")
            return data
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных из CSV: {e}")
            return pd.DataFrame()

    def fetch_historical_data(self, symbol, interval, start_date, end_date):
        """
        Загрузка исторических данных с Binance API.
        """
        logging.info(f"Загрузка исторических данных для {symbol} с {start_date} по {end_date} с интервалом {interval}.")
        try:
            # Получение исторических данных
            klines = self.client.get_historical_klines(symbol, interval, start_date, end_date)
            # Преобразование данных в DataFrame
            data = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            # Оставляем только необходимые столбцы
            data = data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            logging.info("Исторические данные успешно загружены.")
            return data
        except Exception as e:
            logging.error(f"Ошибка при загрузке исторических данных: {e}")
            return pd.DataFrame()
