import pandas as pd
import numpy as np
from settings import STRATEGY_CONFIG
from data.market_data import get_stock_list, get_stock_history

def filter_stocks(
    min_change=STRATEGY_CONFIG['min_change'],
    max_change=STRATEGY_CONFIG['max_change'],
    min_volume_ratio=STRATEGY_CONFIG['min_volume_ratio']
):
    stock_data = get_stock_list()
    
    if stock_data is None:
        return None
    
    filtered = stock_data[
        (stock_data['涨跌幅'] > min_change) &
        (stock_data['涨跌幅'] < max_change) &
        (stock_data['量比'] > min_volume_ratio) &
        (~stock_data['名称'].str.contains('ST')) &
        (~stock_data['代码'].str.startswith('688')) &
        (~stock_data['代码'].str.startswith('8'))
    ]
    
    filtered = filtered[['代码', '名称', '最新价', '涨跌幅', '量比', '成交量', '成交额', '换手率']]
    filtered = filtered.rename(columns={
        '代码': '股票代码',
        '名称': '股票名称',
        '最新价': '现价',
        '涨跌幅': '涨跌幅(%)',
        '量比': '量比',
        '成交量': '成交量(手)',
        '成交额': '成交额(万)',
        '换手率': '换手率(%)'
    })
    
    return filtered

def run_backtest(days=30):
    stock_list = get_stock_list()
    if stock_list is None:
        return None
    
    all_stocks = stock_list[
        (~stock_list['名称'].str.contains('ST')) &
        (~stock_list['代码'].str.startswith('688')) &
        (~stock_list['代码'].str.startswith('8'))
    ]['代码'].unique()
    
    results = []
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=days + 20)
    
    for stock_code in all_stocks[:50]:
        try:
            history = get_stock_history(stock_code)
            if history is None or len(history) < 15:
                continue
            
            history['date'] = pd.to_datetime(history['date'])
            history = history[(history['date'] >= start_date) & (history['date'] <= end_date)]
            
            if len(history) < 10:
                continue
            
            history['ma5'] = history['close'].rolling(5).mean()
            history['ma10'] = history['close'].rolling(10).mean()
            history['pct_change'] = history['close'].pct_change() * 100
            
            for i in range(4, len(history)-1):
                row = history.iloc[i]
                next_row = history.iloc[i+1]
                
                ma5 = row['ma5']
                ma10 = row['ma10']
                close = row['close']
                pct_change = row['pct_change']
                
                volume = row['volume']
                vol_ma5 = history['volume'].iloc[i-4:i+1].mean()
                
                if close >= ma5 and ma5 > ma10:
                    if pct_change > STRATEGY_CONFIG['min_change'] and pct_change < STRATEGY_CONFIG['max_change']:
                        if vol_ma5 > 0 and volume >= STRATEGY_CONFIG['min_volume_ratio'] * vol_ma5:
                            date = row['date'].strftime('%Y-%m-%d')
                            next_day_return = (next_row['close'] - row['close']) / row['close'] * 100
                            results.append({
                                'date': date,
                                'code': stock_code,
                                'return': next_day_return
                            })
        except Exception as e:
            continue
    
    if len(results) == 0:
        return None
    
    results_df = pd.DataFrame(results)
    
    daily_returns = results_df.groupby('date')['return'].mean().sort_index()
    cumulative_return = (1 + daily_returns / 100).cumprod() * 100 - 100
    
    drawdown = cumulative_return.cummax() - cumulative_return
    max_drawdown = drawdown.max()
    
    winning_trades = len(results_df[results_df['return'] > 0])
    total_trades = len(results_df)
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    avg_win = results_df[results_df['return'] > 0]['return'].mean()
    avg_loss = abs(results_df[results_df['return'] <= 0]['return'].mean())
    profit_ratio = avg_win / avg_loss if avg_loss > 0 else 0
    
    return {
        'results_df': results_df,
        'daily_returns': daily_returns,
        'cumulative_return': cumulative_return,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_ratio': profit_ratio,
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'avg_win': avg_win,
        'avg_loss': avg_loss
    }

def calculate_risk_management(buy_price, position_amount, current_price):
    stop_loss_price = buy_price * (1 - STRATEGY_CONFIG['stop_loss_pct'] / 100)
    take_profit_price = buy_price * (1 + STRATEGY_CONFIG['take_profit_pct'] / 100)
    
    if current_price is None:
        current_price = buy_price
    
    profit_loss = (current_price - buy_price) * (position_amount / buy_price)
    profit_loss_pct = (current_price - buy_price) / buy_price * 100
    is_stop_loss = current_price <= stop_loss_price
    
    return {
        'stop_loss_price': stop_loss_price,
        'take_profit_price': take_profit_price,
        'current_price': current_price,
        'profit_loss': profit_loss,
        'profit_loss_pct': profit_loss_pct,
        'is_stop_loss': is_stop_loss
    }
