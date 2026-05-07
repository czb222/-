import akshare as ak
import pandas as pd
import time

def get_stock_data():
    try:
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        return stock_zh_a_spot_df
    except Exception as e:
        print(f"获取实时行情数据失败: {e}")
        return None

def get_stock_hist(symbol):
    try:
        stock_df = ak.stock_zh_a_daily(symbol=symbol, adjust="qfq")
        return stock_df
    except Exception as e:
        print(f"获取股票 {symbol} 历史数据失败: {e}")
        return None

def filter_stocks():
    print("正在获取A股实时行情数据...")
    stock_data = get_stock_data()
    
    if stock_data is None:
        print("网络请求失败，请检查网络连接后重试")
        return
    
    print(f"共获取到 {len(stock_data)} 只股票")
    print("正在筛选符合条件的股票...")
    
    results = []
    
    for _, row in stock_data.iterrows():
        code = row['代码']
        name = row['名称']
        price = row['最新价']
        change = row['涨跌幅']
        volume = row['成交量']
        
        if pd.isna(code) or pd.isna(name) or pd.isna(price) or pd.isna(change) or pd.isna(volume):
            continue
        
        if 'ST' in name:
            continue
        
        if code.startswith('688'):
            continue
        
        if 3 <= change <= 9:
            hist_data = get_stock_hist(code)
            
            if hist_data is None or len(hist_data) < 10:
                continue
            
            hist_data = hist_data.tail(10)
            ma5 = hist_data['close'].rolling(5).mean().iloc[-1]
            ma10 = hist_data['close'].rolling(10).mean().iloc[-1]
            vol_ma5 = hist_data['volume'].rolling(5).mean().iloc[-1]
            
            if pd.isna(ma5) or pd.isna(ma10) or pd.isna(vol_ma5):
                continue
            
            if price >= ma5 and ma5 > ma10:
                if vol_ma5 > 0 and volume >= 2 * vol_ma5:
                    vol_ratio = volume / vol_ma5
                    results.append({
                        '代码': code,
                        '名称': name,
                        '现价': price,
                        '涨跌幅': change,
                        '成交量倍数': round(vol_ratio, 2)
                    })
                    print(f"找到符合条件的股票: {code} {name}")
        
        time.sleep(0.1)
    
    if results:
        print("\n" + "="*60)
        print("符合条件的股票列表")
        print("="*60)
        print(f"{'代码':<10} {'名称':<10} {'现价':<8} {'涨跌幅':<8} {'成交量倍数':<12}")
        print("-"*60)
        for stock in results:
            print(f"{stock['代码']:<10} {stock['名称']:<10} {stock['现价']:<8.2f} {stock['涨跌幅']:<8.2f}% {stock['成交量倍数']:<12.2f}")
        print("="*60)
    else:
        print("\n未找到符合条件的股票")

if __name__ == "__main__":
    filter_stocks()