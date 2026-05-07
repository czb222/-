import streamlit as st

THEME_CONFIG = {
    'primary_bg': '#0a0e1a',
    'secondary_bg': '#111827',
    'card_bg': '#1a2332',
    'accent_green': '#00ff88',
    'accent_red': '#ff4757',
    'accent_blue': '#00d4ff',
    'accent_yellow': '#ffd93d',
    'text_primary': '#ffffff',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',
    'border_color': '#2d3a4f',
}

STRATEGY_CONFIG = {
    'min_change': 3.0,
    'max_change': 9.0,
    'min_volume_ratio': 1.5,
    'stop_loss_pct': 5.0,
    'take_profit_pct': 5.0,
}

BEARISH_WORDS = ['立案', '违规', '减持', '亏损', '跌停', '处罚', '诉讼', '退市', '警告', '风险', '暴雷']
BULLISH_WORDS = ['中标', '增长', '利好', '突破', '涨停', '收购', '增持', '盈利', '合作', '订单', '业绩预增']

CACHE_CONFIG = {
    'market_ttl': 60,
    'stock_list_ttl': 120,
    'stock_history_ttl': 300,
    'news_ttl': 60,
}

def apply_theme():
    css = f"""
    <style>
        :root {{
            --primary-bg: {THEME_CONFIG['primary_bg']};
            --secondary-bg: {THEME_CONFIG['secondary_bg']};
            --card-bg: {THEME_CONFIG['card_bg']};
            --accent-green: {THEME_CONFIG['accent_green']};
            --accent-red: {THEME_CONFIG['accent_red']};
            --accent-blue: {THEME_CONFIG['accent_blue']};
            --accent-yellow: {THEME_CONFIG['accent_yellow']};
            --text-primary: {THEME_CONFIG['text_primary']};
            --text-secondary: {THEME_CONFIG['text_secondary']};
            --text-muted: {THEME_CONFIG['text_muted']};
            --border-color: {THEME_CONFIG['border_color']};
            --shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }}

        .stApp {{
            background: linear-gradient(135deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
            min-height: 100vh;
        }}

        .css-1d391kg {{
            background-color: var(--secondary-bg);
            border-right: 1px solid var(--border-color);
        }}

        .stSidebar > div:first-child {{
            background-color: var(--secondary-bg);
        }}

        .stButton>button {{
            background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .stButton>button:hover {{
            background: linear-gradient(135deg, #2d4a6f 0%, #3d5a8f 100%);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
            transform: translateY(-2px);
        }}

        .stTextInput>div>div>input, .stNumberInput>div>div>input {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
        }}

        .stSlider>div>div>div>div {{
            background-color: var(--accent-blue);
        }}

        .metric-card {{
            background: linear-gradient(145deg, var(--card-bg), #253040);
            border-radius: 12px;
            padding: 1.25rem;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
        }}

        .dataframe-container {{
            background-color: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border-color);
            overflow: hidden;
        }}

        .warning-alert {{
            background: linear-gradient(135deg, rgba(255, 71, 87, 0.2), rgba(255, 71, 87, 0.1));
            border: 2px solid var(--accent-red);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}

        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .blink-animation {{
            animation: blink 1s ease-in-out infinite;
        }}

        .header-gradient {{
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .green-text {{ color: var(--accent-green); }}
        .red-text {{ color: var(--accent-red); }}
        .blue-text {{ color: var(--accent-blue); }}
        .yellow-text {{ color: var(--accent-yellow); }}
        .glow-green {{ text-shadow: 0 0 10px rgba(0, 255, 136, 0.5); }}
        .glow-red {{ text-shadow: 0 0 10px rgba(255, 71, 87, 0.5); }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
