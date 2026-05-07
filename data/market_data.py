import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from settings import CACHE_CONFIG
import streamlit as st

@st.cache_data(ttl=CACHE_CONFIG['market_ttl'])
def get_market_overview():
    try:
        sh_index = ak.stock_zh_index_daily(symbol="sh000001").tail(1)
        sz_index = ak.stock_zh_index_daily(symbol="sz399001").tail(1)
        cy_index = ak.stock_zh_index_daily(symbol="sz399006").tail(1)
        
        return {
            "上证指数": {
                "收盘": sh_index['close'].values[0] if len(sh_index) > 0 else 0,
                "涨跌幅": sh_index['change'].values[0] if len(sh_index) > 0 else 0,
                "成交量": sh_index['volume'].values[0] if len(sh_index) > 0 else 0
            },
            "深证成指": {
                "收盘": sz_index['close'].values[0] if len(sz_index) > 0 else 0,
                "涨跌幅": sz_index['change'].values[0] if len(sz_index) > 0 else 0,
                "成交量": sz_index['volume'].values[0] if len(sz_index) > 0 else 0
            },
            "创业板指": {
                "收盘": cy_index['close'].values[0] if len(cy_index) > 0 else 0,
                "涨跌幅": cy_index['change'].values[0] if len(cy_index) > 0 else 0,
                "成交量": cy_index['volume'].values[0] if len(cy_index) > 0 else 0
            }
        }
    except Exception as e:
        st.error(f"获取大盘数据失败: {e}")
        return None

@st.cache_data(ttl=CACHE_CONFIG['stock_list_ttl'])
def get_stock_list():
    try:
        return ak.stock_zh_a_spot()
    except Exception as e:
        st.error(f"获取股票列表失败: {e}")
        return None

@st.cache_data(ttl=CACHE_CONFIG['stock_history_ttl'])
def get_stock_history(symbol):
    try:
        df = ak.stock_zh_a_daily(symbol=symbol, adjust="qfq")
        df['ma5'] = df['close'].rolling(5).mean()
        df['ma10'] = df['close'].rolling(10).mean()
        df['ma20'] = df['close'].rolling(20).mean()
        return df
    except Exception as e:
        st.error(f"获取股票 {symbol} 历史数据失败: {e}")
        return None

@st.cache_data(ttl=CACHE_CONFIG['news_ttl'])
def get_stock_news(symbol):
    try:
        news = ak.stock_news(symbol=symbol)
        return news.head(5)
    except Exception as e:
        return None

def get_stock_realtime_price(code):
    try:
        stock_data = get_stock_list()
        if stock_data is None:
            return None
        stock = stock_data[stock_data['代码'] == code]
        if len(stock) > 0:
            return stock['最新价'].values[0]
        return None
    except Exception as e:
        return None

def get_stock_name(code):
    try:
        stock_data = get_stock_list()
        if stock_data is None:
            return code
        stock = stock_data[stock_data['代码'] == code]
        if len(stock) > 0:
            return stock['名称'].values[0]
        return code
    except Exception as e:
        return code
