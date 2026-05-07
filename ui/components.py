import streamlit as st
import plotly.graph_objects as go
from settings import THEME_CONFIG, BEARISH_WORDS, BULLISH_WORDS
from io import StringIO

def render_metric_card(title, value, sub_value=None, trend=None):
    trend_color = THEME_CONFIG['accent_green'] if trend >= 0 else THEME_CONFIG['accent_red']
    trend_text = f"{trend:+.2f}%" if trend is not None else ""
    
    st.markdown(f"""
    <div class='metric-card'>
        <p style='color: {THEME_CONFIG['text_muted']}; font-size: 12px; margin-bottom: 0.25rem;'>{title}</p>
        <p style='color: {THEME_CONFIG['text_primary']}; margin: 0; font-size: 1.75rem; font-weight: 600;'>{value}</p>
        {f"<p style='color: {trend_color}; font-size: 1rem; margin-top: 0.25rem;'>{trend_text}</p>" if trend_text else ""}
        {f"<p style='color: {THEME_CONFIG['text_muted']}; font-size: 11px; margin-top: 0.25rem;'>{sub_value}</p>" if sub_value else ""}
    </div>
    """, unsafe_allow_html=True)

def render_market_cards(overview):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card(
            "上证指数",
            f"{overview['上证指数']['收盘']:.2f}",
            f"成交量: {overview['上证指数']['成交量']/10000:.1f}万手",
            overview['上证指数']['涨跌幅']
        )
    
    with col2:
        render_metric_card(
            "深证成指",
            f"{overview['深证成指']['收盘']:.2f}",
            f"成交量: {overview['深证成指']['成交量']/10000:.1f}万手",
            overview['深证成指']['涨跌幅']
        )
    
    with col3:
        render_metric_card(
            "创业板指",
            f"{overview['创业板指']['收盘']:.2f}",
            f"成交量: {overview['创业板指']['成交量']/10000:.1f}万手",
            overview['创业板指']['涨跌幅']
        )

def render_kline_chart(history, stock_code, stock_name):
    fig = go.Figure(data=[go.Candlestick(
        x=history['date'],
        open=history['open'],
        high=history['high'],
        low=history['low'],
        close=history['close'],
        name='K线',
        increasing_line_color=THEME_CONFIG['accent_green'],
        decreasing_line_color=THEME_CONFIG['accent_red'],
        increasing_fillcolor=f"rgba({int(THEME_CONFIG['accent_green'][1:], 16) >> 16}, {(int(THEME_CONFIG['accent_green'][1:], 16) >> 8) & 0xFF}, {int(THEME_CONFIG['accent_green'][1:], 16) & 0xFF}, 0.1)",
        decreasing_fillcolor=f"rgba({int(THEME_CONFIG['accent_red'][1:], 16) >> 16}, {(int(THEME_CONFIG['accent_red'][1:], 16) >> 8) & 0xFF}, {int(THEME_CONFIG['accent_red'][1:], 16) & 0xFF}, 0.1)"
    )])
    
    fig.add_trace(go.Scatter(
        x=history['date'],
        y=history['ma5'],
        mode='lines',
        name='5日均线',
        line=dict(color=THEME_CONFIG['accent_blue'], width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=history['date'],
        y=history['ma10'],
        mode='lines',
        name='10日均线',
        line=dict(color=THEME_CONFIG['accent_yellow'], width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=history['date'],
        y=history['ma20'],
        mode='lines',
        name='20日均线',
        line=dict(color='#a855f7', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f"{stock_code} {stock_name} K线图",
        xaxis_title='日期',
        yaxis_title='价格',
        height=550,
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 26, 0.8)',
        plot_bgcolor='rgba(17, 24, 39, 0.8)',
        font=dict(color=THEME_CONFIG['text_primary']),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_news_section(news):
    if news is None or len(news) == 0:
        st.markdown(f"<p style='color: {THEME_CONFIG['text_muted']};'>暂无最新资讯</p>", unsafe_allow_html=True)
        return
    
    for _, row in news.iterrows():
        title = row['title']
        time = row['time']
        
        sentiment = 'neutral'
        for word in BEARISH_WORDS:
            if word in title:
                sentiment = 'bearish'
                break
        if sentiment == 'neutral':
            for word in BULLISH_WORDS:
                if word in title:
                    sentiment = 'bullish'
                    break
        
        color = THEME_CONFIG['text_muted']
        icon = '📋'
        if sentiment == 'bearish':
            color = THEME_CONFIG['accent_red']
            icon = '🔴'
        elif sentiment == 'bullish':
            color = THEME_CONFIG['accent_green']
            icon = '🟢'
        
        st.markdown(f"""
        <div style='background-color: {THEME_CONFIG['card_bg']}; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem; border-left: 3px solid {color};'>
            <div style='display: flex; align-items: flex-start; gap: 0.75rem;'>
                <span>{icon}</span>
                <div>
                    <p style='color: {color}; margin: 0; font-size: 14px;'>{title}</p>
                    <p style='color: {THEME_CONFIG['text_muted']}; font-size: 11px; margin-top: 0.25rem;'>{time}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_stop_loss_alert():
    st.markdown("""
    <div class='warning-alert blink-animation'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <span style='font-size: 2rem;'>⚠️</span>
            <div>
                <h3 style='color: var(--accent-red); margin: 0; font-size: 1.25rem;'>触发止损线</h3>
                <p style='color: var(--text-secondary); margin: 0.25rem 0 0 0;'>建议立即卖出！</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_risk_management_panel(buy_price, position_amount, risk_data):
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, {THEME_CONFIG['card_bg']}, #253040); border-radius: 12px; padding: 1rem; border: 1px solid {THEME_CONFIG['border_color']};'>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;'>
            <div>
                <p style='color: {THEME_CONFIG['text_muted']}; font-size: 11px; margin-bottom: 0.25rem;'>止损价 (-5%)</p>
                <p style='color: {THEME_CONFIG['accent_red']}; font-size: 1.25rem; font-weight: 600;'>{risk_data['stop_loss_price']:.2f}</p>
            </div>
            <div>
                <p style='color: {THEME_CONFIG['text_muted']}; font-size: 11px; margin-bottom: 0.25rem;'>止盈价 (+5%)</p>
                <p style='color: {THEME_CONFIG['accent_green']}; font-size: 1.25rem; font-weight: 600;'>{risk_data['take_profit_price']:.2f}</p>
            </div>
            <div>
                <p style='color: {THEME_CONFIG['text_muted']}; font-size: 11px; margin-bottom: 0.25rem;'>现价</p>
                <p style='color: {THEME_CONFIG['text_primary']}; font-size: 1.25rem; font-weight: 600;'>{risk_data['current_price']:.2f}</p>
            </div>
            <div>
                <p style='color: {THEME_CONFIG['text_muted']}; font-size: 11px; margin-bottom: 0.25rem;'>浮动盈亏</p>
                <p style='color: {THEME_CONFIG['accent_green'] if risk_data['profit_loss'] >= 0 else THEME_CONFIG['accent_red']}; font-size: 1.25rem; font-weight: 600;'>{risk_data['profit_loss']:+.2f}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_backtest_summary(backtest_result):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            "累计收益率",
            f"{backtest_result['cumulative_return'].iloc[-1]:+.2f}%",
            trend=backtest_result['cumulative_return'].iloc[-1]
        )
    
    with col2:
        render_metric_card(
            "最大回撤",
            f"{backtest_result['max_drawdown']:.2f}%",
            trend=-abs(backtest_result['max_drawdown'])
        )
    
    with col3:
        render_metric_card(
            "胜率",
            f"{backtest_result['win_rate']:.1f}%",
            trend=backtest_result['win_rate'] - 50
        )
    
    with col4:
        render_metric_card(
            "盈亏比",
            f"{backtest_result['profit_ratio']:.2f}",
            trend=backtest_result['profit_ratio'] - 1
        )

def render_cumulative_return_chart(cumulative_return, time_range):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=cumulative_return.index,
        y=cumulative_return.values,
        mode='lines',
        name='累计收益',
        line=dict(color=THEME_CONFIG['accent_green'], width=3)
    ))
    
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=THEME_CONFIG['text_muted'],
        name='基准线'
    )
    
    fig.update_layout(
        title=f"{time_range} 策略回测收益曲线",
        xaxis_title='日期',
        yaxis_title='累计收益率 (%)',
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 26, 0.8)',
        plot_bgcolor='rgba(17, 24, 39, 0.8)',
        font=dict(color=THEME_CONFIG['text_primary'])
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_download_button(dataframe, filename="data.csv"):
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="📥 下载 CSV",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )
