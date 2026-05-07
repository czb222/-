# 📈 QuantStock Pro - A股量化选股系统

基于 Python + Streamlit 构建的专业 A 股量化选股 Web 应用。

## ✨ 功能特性

- **大盘概览** - 实时跟踪上证指数、深证成指、创业板指走势
- **智能选股** - 基于量化策略筛选优质标的（涨幅、量比、非ST等条件）
- **个股详情** - 交互式 K 线图、持仓风控面板、新闻情绪分析
- **策略回测** - 回测历史表现，评估策略有效性（收益率、最大回撤、胜率、盈亏比）

## 🛠️ 技术栈

- **框架**: Streamlit 1.57+
- **数据**: akshare (A股数据接口)
- **图表**: Plotly
- **数据处理**: Pandas

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

### 部署到 Streamlit Cloud

1. Fork 本仓库到你的 GitHub 账号
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 点击 "New app"
4. 选择你的 GitHub 仓库、分支和主文件 `app.py`
5. 点击 "Deploy"

## 📁 项目结构

```
quantstock_pro/
├── app.py                    # 主入口文件
├── settings.py               # 配置管理
├── requirements.txt          # 依赖清单
├── ARCHITECTURE.md           # 架构文档
├── data/                     # 数据层
│   └── market_data.py        # 市场数据获取与缓存
├── strategies/               # 策略层
│   └── stock_picker.py       # 选股策略、回测引擎
└── ui/                       # UI层
    ├── components.py         # 可复用UI组件
    └── pages.py              # 页面视图
```

## 📊 选股策略

- 涨幅范围: 3% ~ 9%
- 量比 > 1.5
- 排除 ST 股票
- 排除科创板（688开头）和北交所股票

## 📝 风控参数

- 止损比例: 5%
- 止盈比例: 5%

## 📄 License

MIT License