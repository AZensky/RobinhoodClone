from flask import Blueprint, jsonify
import datetime
import time

import os
import requests

finnhub_routes = Blueprint('finnhub', __name__)

FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

# API route to get stock data for a specific company
# Example output: https://finnhub.io/docs/api/quote
@finnhub_routes.route('/stock-data/<symbol>')
def fetch_stock_data(symbol):
    res = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}')
    data = res.json()
    return data

# API route to get all current market news
# Example output: https://finnhub.io/api/v1/news?category=general&token=cbu2r6iad3i96b4mbifg
@finnhub_routes.route('/market-news')
def fetch_market_news():
    res = requests.get(f'https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}')
    data = res.json()
    return jsonify(data)

# API route to get a specific company's news articles.
# Example output: https://finnhub.io/api/v1/company-news?symbol=AAPL&from=2021-09-01&to=2021-09-09&token=cbu2r6iad3i96b4mbifg
@finnhub_routes.route('/company/<symbol>/news')
def fetch_company_news(symbol):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
    week_ago_str = week_ago.strftime('%Y-%m-%d')

    res = requests.get(f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from={week_ago_str}&to={today}&token={FINNHUB_API_KEY}')
    data = res.json()
    return jsonify(data)

# API route to get a specific stock's tick data TODAY.
# Documentation with examples output: https://finnhub.io/docs/api/stock-tick
@finnhub_routes.route('/today-tick/<symbol>')
def fetch_today_tick_data(symbol):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    res = requests.get(f'https://tick.finnhub.io/api/v1/stock/tick?symbol={symbol}&date={today}&limit=500&skip=0&format=json&token={FINNHUB_API_KEY}')
    data = res.json()
    return jsonify(data)

# API route to get a specific stock's candlestick data for the past month. Candlestick data consist of closing and opening prices for selected timeframe, along with the timestamp in unix form. We should probably use closing prices for consistency.
# Example output: https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=D&from=1572651390&to=1575243390&token=cbu2r6iad3i96b4mbifg
@finnhub_routes.route('/candlestick-data/one-month/<symbol>')
def fetch_month_candlestick_data(symbol):
    today = datetime.datetime.today()
    one_month_ago = today - datetime.timedelta(days=30)

    unix_today = int(time.mktime(today.timetuple()))
    unix_one_month_ago = int(time.mktime(one_month_ago.timetuple()))

    res = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&from={unix_one_month_ago}&to={unix_today}&token={FINNHUB_API_KEY}')
    data = res.json()
    print('DATTTAAA', data)
    return jsonify(data)

# API route to get a specific stock's candlestick data for the past week. Candlestick data consist of closing and opening prices for selected timeframe, along with the timestamp in unix form. We should probably use closing prices for consistency.
# Example output: https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=D&from=1572651390&to=1575243390&token=cbu2r6iad3i96b4mbifg
@finnhub_routes.route('/candlestick-data/week/<symbol>')
def fetch_week_candlestick_data(symbol):
    today = datetime.datetime.today()
    one_week_ago = today - datetime.timedelta(days=7)

    unix_today = int(time.mktime(today.timetuple()))
    unix_one_week_ago = int(time.mktime(one_week_ago.timetuple()))

    res = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=60&from={unix_one_week_ago}&to={unix_today}&token={FINNHUB_API_KEY}')
    data = res.json()
    return jsonify(data)


# API route to get company data
@finnhub_routes.route('/company-data/<symbol>')
def fetch_company_data(symbol):
    res = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}')
    data = res.json()
    return data
