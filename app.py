import streamlit as st
from settings import apply_theme, THEME_CONFIG
from ui.pages import page_market_overview, page_stock_picker, page_stock_detail, page_backtest

st.set_page_config(
    page_title="QuantStock Pro - A股量化选股",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📈"
)

apply_theme()

def main():
    with st.sidebar:
        st.markdown("<h1 style='background: linear-gradient(90deg, var(--accent-blue), var(--accent-green)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.5rem; margin-bottom: 2rem;'>📈 QuantStock Pro</h1>", unsafe_allow_html=True)
        
        page = st.radio(
            "",
            ["大盘概览", "智能选股", "个股详情", "策略回测"],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown(f"<p style='color: {THEME_CONFIG['text_muted']}; font-size: 12px;'>A股量化选股系统 v2.0</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {THEME_CONFIG['text_muted']}; font-size: 10px;'>数据来源: akshare</p>", unsafe_allow_html=True)
    
    if page == "大盘概览":
        page_market_overview()
    elif page == "智能选股":
        page_stock_picker()
    elif page == "个股详情":
        page_stock_detail()
    elif page == "策略回测":
        page_backtest()

if __name__ == "__main__":
    main()