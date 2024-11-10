import logging
from utils.data_loader import fetch_historical_data, parse_data


class DataAgent:
    @staticmethod
    def get_data(symbol, timeframe):
        logging.info(f"Запрос исторических данных для {symbol} с временным интервалом {timeframe}")

        try:
            # Получение сырых данных
            raw_data = fetch_historical_data(symbol, timeframe)
            if not raw_data or len(raw_data) < 2:
                raise ValueError(f"Недостаточно данных для {symbol}")

            # Парсинг данных
            parsed_data = parse_data(raw_data)
            logging.debug(f"Полученные данные для {symbol}: {parsed_data[:5]}")  # Лог первых 5 элементов
            logging.info(f"Успешно получено {len(parsed_data)} записей для {symbol}")
            return parsed_data

        except ValueError as ve:
            logging.warning(f"Ошибка с данными для {symbol}: {ve}")
            return []
        except Exception as e:
            logging.error(f"Непредвиденная ошибка при получении данных для {symbol}: {e}")
            return []

# Пример использования
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    data = DataAgent.get_data("BTCUSDT", "1d")
    if data:
        logging.info(f"Данные успешно загружены: {data[:5]}")
    else:
        logging.warning("Данные не были загружены.")
