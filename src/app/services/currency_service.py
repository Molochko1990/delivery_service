import requests


def get_usd_exchange_rate() -> float:
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js', timeout=10)
    response.raise_for_status()

    data = response.json()
    usd_info = data.get('Valute', {}).get('USD', {})
    return usd_info.get('Value', 0.0)
