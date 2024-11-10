

# import os

# API_KEY = os.getenv('55MF7bhBzn95uLzBycJaeClFCy29ktSGW37VaeaztTasBAQSa7KDGrNzongOoPUV') or 'your_actual_api_key'
# API_SECRET = os.getenv('D31Gcp2BlV8OSb67qZ2cp2fqc2Yq9m2fp3Jy4ZQp0KO51kmRwqbxgtlebDUShfKd') or 'your_actual_api_secret'


# Параметры агентов

AGENT_SETTINGS = {
    "risk_tolerance": 0.01,
    "sentiment_threshold": 0.5,
}

API_KEY = "55MF7bhBzn95uLzBycJaeClFCy29ktSGW37VaeaztTasBAQSa7KDGrNzongOoPUV"
API_SECRET = "D31Gcp2BlV8OSb67qZ2cp2fqc2Yq9m2fp3Jy4ZQp0KO51kmRwqbxgtlebDUShfKd"
BASE_URL = "https://api.binance.com"

STRATEGY_PARAMETERS = {
    "risk_reward_ratio": 3,
    "max_loss": 0.01,          # Максимальная потеря (1%)
    "timeframe": "1h",
    "symbol": "BTCUSDT",
    "quantity": 0.001               # Количество для ордера (например, 0.001 BTC)
}

# Параметры для получения топ-200 активов
TOP_N = 200     # Количество топ-активов для анализа