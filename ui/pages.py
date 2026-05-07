import streamlit as st
import pandas as pd
from data.market_data import get_market_overview, get_stock_history, get_stock_realtime_price, get_stock_name, get_stock_news
from strategies.stock_picker import filter_stocks, run_backtest, calculate_risk_management
from ui.components import (
    render_market_cards,
    render_kline_chart,
    render_news_section,
    render_stop_loss_alert,
    render_risk_management_panel,
    render_backtest_summary,
    render_cumulative_return_chart,
    render_download_button
)
from settings import THEME_CONFIG

def page_market_overview():
    st.markdown("<h1 class='header-gradient'>📊 大盘概览</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {THEME_CONFIG['text_secondary']}; margin-bottom: 2rem;'>实时跟踪三大指数走势，把握市场脉搏</p>", unsafe_allow_html=True)
    
    overview = get_market_overview()
    if overview is None:
        st.error("网络请求失败，请检查网络连接后重试")
        return
    
    render_market_cards(overview)

def page_stock_picker():
    st.markdown("<h1 class='header-gradient'>🔍 智能选股</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {THEME_CONFIG['text_secondary']}; margin-bottom: 2rem;'>基于量化策略筛选优质标的，把握短线机会</p>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"<h3 style='color: {THEME_CONFIG['accent_blue']}; margin-bottom: 1rem;'>⚙️ 选股参数</h3>", unsafe_allow_html=True)
        
        min_change = st.slider("最小涨幅(%)", 0, 5, 3, 0.5, help="筛选的最小涨幅")
        max_change = st.slider("最大涨幅(%)", 5, 10, 9, 0.5, help="筛选的最大涨幅")
        min_volume_ratio = st.slider("最小量比", 1.0, 3.0, 1.5, 0.1, help="量比指标，衡量成交量活跃度")
        run_button = st.button("🚀 开始选股", type="primary")
    
    if run_button:
        with st.spinner("正在获取股票数据..."):
            filtered = filter_stocks(min_change, max_change, min_volume_ratio)
        
        if filtered is None:
            st.error("网络请求失败，请检查网络连接后重试")
            return
        
        st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;'>
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 0.75rem 1.5rem; border-radius: 20px;'>
                <span style='color: white; font-weight: 600;'>找到 {len(filtered)} 只符合条件的股票</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            render_download_button(filtered, "quantstock_selected.csv")
        
        st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
        st.dataframe(
            filtered,
            hide_index=True,
            column_config={
                '现价': st.column_config.NumberColumn(format="%.2f"),
                '涨跌幅(%)': st.column_config.NumberColumn(format="%.2f"),
                '量比': st.column_config.NumberColumn(format="%.2f"),
                '成交量(手)': st.column_config.NumberColumn(format="%.0f"),
                '成交额(万)': st.column_config.NumberColumn(format="%.0f"),
                '换手率(%)': st.column_config.NumberColumn(format="%.2f")
            },
            height=600
        )
        st.markdown("</div>", unsafe_allow_html=True)

def page_stock_detail():
    st.markdown("<h1 class='header-gradient'>📈 个股详情</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {THEME_CONFIG['text_secondary']}; margin-bottom: 2rem;'>深入分析个股走势，做出明智决策</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        stock_code = st.text_input("输入股票代码", "000001", help="如：000001（平安银行）、600519（贵州茅台）")
        
        if st.button("🔍 查询", use_container_width=True):
            with st.spinner("正在获取股票数据..."):
                history = get_stock_history(stock_code)
            
            if history is None or len(history) == 0:
                st.error("未找到该股票数据，请检查股票代码是否正确")
                return
            
            stock_name = get_stock_name(stock_code)
            
            st.session_state['stock_history'] = history
            st.session_state['stock_name'] = stock_name
            st.session_state['stock_code'] = stock_code
        
        if 'stock_code' in st.session_state:
            st.subheader(f"{st.session_state['stock_code']} {st.session_state['stock_name']}")
            
            latest_data = st.session_state['stock_history'].iloc[-1]
            change = latest_data['close'] - latest_data['open']
            pct_change = (change / latest_data['open']) * 100
            
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, {THEME_CONFIG['card_bg']}, #253040); border-radius: 12px; padding: 1.5rem; border: 1px solid {THEME_CONFIG['border_color']};'>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                    <div>
                        <p style='color: {THEME_CONFIG['text_muted']}; font-size: 12px; margin-bottom: 0.25rem;'>收盘价</p>
                        <p style='color: {THEME_CONFIG['text_primary']}; font-size: 1.5rem; font-weight: 600;'>{latest_data['close']:.2f}</p>
                    </div>
                    <div>
                        <p style='color: {THEME_CONFIG['text_muted']}; font-size: 12px; margin-bottom: 0.25rem;'>涨跌额</p>
                        <p style='color: {THEME_CONFIG['accent_green'] if change >= 0 else THEME_CONFIG['accent_red']}; font-size: 1.5rem; font-weight: 600;'>{change:+.2f}</p>
                    </div>
                    <div>
                        <p style='color: {THEME_CONFIG['text_muted']}; font-size: 12px; margin-bottom: 0.25rem;'>涨跌幅</p>
                        <p style='color: {THEME_CONFIG['accent_green'] if pct_change >= 0 else THEME_CONFIG['accent_red']}; font-size: 1.5rem; font-weight: 600;'>{pct_change:+.2f}%</p>
                    </div>
                    <div>
                        <p style='color: {THEME_CONFIG['text_muted']}; font-size: 12px; margin-bottom: 0.25rem;'>成交量</p>
                        <p style='color: {THEME_CONFIG['text_primary']}; font-size: 1.5rem; font-weight: 600;'>{latest_data['volume']:,}手</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='color: {THEME_CONFIG['accent_yellow']}; margin-top: 1.5rem;'>🛡️ 持仓风控</h3>", unsafe_allow_html=True)
            
            buy_price = st.number_input("买入价格", value=latest_data['close'], step=0.01)
            position_amount = st.number_input("持仓金额(元)", value=10000.0, step=1000.0)
            
            realtime_price = get_stock_realtime_price(st.session_state['stock_code'])
            risk_data = calculate_risk_management(buy_price, position_amount, realtime_price)
            render_risk_management_panel(buy_price, position_amount, risk_data)
    
    with col2:
        if 'stock_history' in st.session_state:
            latest_data = st.session_state['stock_history'].iloc[-1]
            realtime_price = get_stock_realtime_price(st.session_state['stock_code'])
            if realtime_price is None:
                realtime_price = latest_data['close']
            
            buy_price = st.session_state.get('buy_price', latest_data['close'])
            risk_data = calculate_risk_management(buy_price, 10000, realtime_price)
            
            if risk_data['is_stop_loss']:
                render_stop_loss_alert()
            
            render_kline_chart(
                st.session_state['stock_history'],
                st.session_state['stock_code'],
                st.session_state['stock_name']
            )
            
            st.markdown(f"<h3 style='color: {THEME_CONFIG['text_primary']}; margin-top: 1.5rem;'>📰 个股资讯</h3>", unsafe_allow_html=True)
            news = get_stock_news(st.session_state['stock_code'])
            render_news_section(news)
            
            st.markdown(f"<h3 style='color: {THEME_CONFIG['text_primary']}; margin-top: 1.5rem;'>近期数据</h3>", unsafe_allow_html=True)
            st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
            st.dataframe(
                st.session_state['stock_history'].tail(10)[['date', 'open', 'high', 'low', 'close', 'volume', 'ma5', 'ma10']],
                hide_index=True,
                column_config={
                    'open': st.column_config.NumberColumn(format="%.2f"),
                    'high': st.column_config.NumberColumn(format="%.2f"),
                    'low': st.column_config.NumberColumn(format="%.2f"),
                    'close': st.column_config.NumberColumn(format="%.2f"),
                    'volume': st.column_config.NumberColumn(format="%.0f"),
                    'ma5': st.column_config.NumberColumn(format="%.2f"),
                    'ma10': st.column_config.NumberColumn(format="%.2f")
                },
                height=200
            )
            st.markdown("</div>", unsafe_allow_html=True)

def page_backtest():
    st.markdown("<h1 class='header-gradient'>📊 策略回测</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {THEME_CONFIG['text_secondary']}; margin-bottom: 2rem;'>回测历史表现，评估策略有效性</p>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"<h3 style='color: {THEME_CONFIG['accent_blue']}; margin-bottom: 1rem;'>⏱️ 时间范围</h3>", unsafe_allow_html=True)
        
        time_range = st.selectbox("选择回测周期", ["过去7天", "过去14天", "过去30天", "过去60天"], index=2)
        run_backtest_button = st.button("▶️ 开始回测", type="primary")
    
    if run_backtest_button:
        days_map = {"过去7天": 7, "过去14天": 14, "过去30天": 30, "过去60天": 60}
        days = days_map[time_range]
        
        with st.spinner(f"正在回测过去 {days} 天的数据..."):
            backtest_result = run_backtest(days)
        
        if backtest_result is None:
            st.warning("未找到符合条件的交易信号")
            return
        
        render_backtest_summary(backtest_result)
        
        st.markdown(f"<h3 style='color: {THEME_CONFIG['text_primary']}; margin-top: 2rem;'>📈 累计收益曲线</h3>", unsafe_allow_html=True)
        render_cumulative_return_chart(backtest_result['cumulative_return'], time_range)
        
        st.markdown(f"<h3 style='color: {THEME_CONFIG['text_primary']}; margin-top: 1.5rem;'>📊 回测统计</h3>", unsafe_allow_html=True)
        
        stats_df = pd.DataFrame({
            '指标': ['总交易次数', '盈利次数', '亏损次数', '胜率', '平均盈利', '平均亏损', '盈亏比', '最大回撤', '累计收益'],
            '数值': [
                backtest_result['total_trades'],
                backtest_result['winning_trades'],
                backtest_result['total_trades'] - backtest_result['winning_trades'],
                f"{backtest_result['win_rate']:.1f}%",
                f"{backtest_result['avg_win']:.2f}%",
                f"{backtest_result['avg_loss']:.2f}%",
                f"{backtest_result['profit_ratio']:.2f}",
                f"{backtest_result['max_drawdown']:.2f}%",
                f"{backtest_result['cumulative_return'].iloc[-1]:+.2f}%"
            ]
        })
        
        st.dataframe(
            stats_df,
            hide_index=True,
            column_config={
                '指标': st.column_config.Column(width='medium'),
                '数值': st.column_config.Column(width='small')
            }
        )
