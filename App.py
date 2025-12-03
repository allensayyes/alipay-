import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

# 导入北美地图相关函数和数据
try:
    from create_north_america_map import create_map_with_plotly, create_asia_map_with_plotly
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False
    create_map_with_plotly = None
    create_asia_map_with_plotly = None


st.set_page_config(
    page_title="Alipay+ Cross-Border BI Demo",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.6rem;
            font-weight: 700;
            color: #1677ff;
            text-align: center;
            margin-top: 0rem;
            margin-bottom: 0rem;
        }
        .metric-card {
            background: linear-gradient(120deg, #1677ff 0%, #00c6ff 100%);
            padding: 1.1rem;
            border-radius: 14px;
            color: #ffffff;
            text-align: center;
            margin: 0.4rem 0;
            box-shadow: 0 8px 18px rgba(22, 119, 255, 0.25);
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1f2937;
            margin: 2rem 0 1.2rem;
            border-bottom: 2px solid rgba(22, 119, 255, 0.2);
            padding-bottom: 0.4rem;
        }
        .data-source {
            font-size: 0.85rem;
            color: #6b7280;
            font-style: italic;
            margin-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

assets_dir = Path(__file__).with_name("assets")
mindmap_path = assets_dir.joinpath("alipay_mindmap.png")
alipay_fintech_path = assets_dir.joinpath("Alipay Fintech.png")


@st.cache_data(show_spinner=False)
def load_demo_data(seed: int = 2025):
    np.random.seed(seed)

    global_kpis = pd.DataFrame(
        {
            "metric": [
                "核心市场覆盖",
                "年度跨境GMV",
                "活跃商户数",
                "跨境钱包用户",
                "客单价(USD)",
                "营销ROI",
            ],
            "value": ["200+ 国家/地区", "$128B", "5.8M", "1.6B", "$42", "3.4x"],
            "delta": ["+12 vs 2024", "+18%", "+14%", "+9%", "+6%", "+0.5x"],
        }
    )

    region_summary = pd.DataFrame(
        {
            "region": ["东南亚", "东北亚", "欧洲", "中东", "拉美", "非洲"],
            "merchant_millions": [1.9, 0.8, 1.1, 0.5, 0.6, 0.3],
            "wallet_users_millions": [480, 260, 310, 150, 120, 90],
            "volume_billion_usd": [165, 90, 105, 58, 45, 32],
            "success_rate": [99.32, 99.08, 98.75, 99.15, 98.96, 98.55],
            "gmv_growth_pct": [17.5, 12.9, 9.8, 11.6, 10.8, 8.4],
            "merchant_activity_index": [86, 78, 72, 69, 74, 65],
            "consumer_activity_index": [88, 82, 76, 71, 73, 68],
        }
    )

    partner_penetration = pd.DataFrame(
        {
            "partner": [
                "Lazada",
                "TikTok Shop",
                "Gcash",
                "TrueMoney",
                "Touch 'n Go",
                "Maya",
                "Alfamart",
                "Kakao Pay",
            ],
            "partner_type": [
                "电商平台",
                "电商平台",
                "钱包服务商",
                "钱包服务商",
                "钱包服务商",
                "钱包服务商",
                "线下零售网络",
                "钱包服务商",
            ],
            "region": [
                "东南亚",
                "全球内容电商",
                "菲律宾",
                "泰国",
                "马来西亚",
                "菲律宾",
                "印尼",
                "韩国",
            ],
            "gmv_b": [40, 28, 12, 8, 16, 6, 9, 14],
            "alipay_plus_share": [0.62, 0.44, 0.75, 0.68, 0.72, 0.63, 0.58, 0.47],
            "primary_competitor": [
                "Stripe",
                "Adyen",
                "Local PSP",
                "Local PSP",
                "GrabPay",
                "Banks",
                "Doku",
                "Naver Pay",
            ],
        }
    )
    partner_penetration["others_share"] = (
        1 - partner_penetration["alipay_plus_share"]
    )
    partner_penetration["primary_competitor_share"] = [
        0.24,
        0.32,
        0.18,
        0.22,
        0.20,
        0.25,
        0.30,
        0.36,
    ]
    partner_penetration["other_competitors_share"] = (
        partner_penetration["others_share"]
        - partner_penetration["primary_competitor_share"]
    )

    country_coverage = pd.DataFrame(
        {
            "iso_alpha": [
                "CHN",
                "SGP",
                "THA",
                "IDN",
                "PHL",
                "MYS",
                "VNM",
                "KOR",
                "JPN",
                "ARE",
                "SAU",
                "FRA",
                "DEU",
                "GBR",
                "ESP",
                "USA",
                "MEX",
                "BRA",
            ],
            "country": [
                "中国内地",
                "新加坡",
                "泰国",
                "印尼",
                "菲律宾",
                "马来西亚",
                "越南",
                "韩国",
                "日本",
                "阿联酋",
                "沙特",
                "法国",
                "德国",
                "英国",
                "西班牙",
                "美国",
                "墨西哥",
                "巴西",
            ],
            "gmv_b": [
                85,
                14,
                12,
                18,
                15,
                11,
                10,
                17,
                16,
                9,
                8,
                13,
                12,
                14,
                9,
                32,
                11,
                13,
            ],
            "growth_rate": [
                18.5,
                16.2,
                15.7,
                17.3,
                18.1,
                15.9,
                14.6,
                12.4,
                11.9,
                13.8,
                12.5,
                9.6,
                9.2,
                10.4,
                10.1,
                8.5,
                11.8,
                13.2,
            ],
            "wallet_penetration": [
                68,
                76,
                72,
                65,
                74,
                78,
                61,
                58,
                55,
                63,
                59,
                47,
                45,
                49,
                46,
                38,
                42,
                51,
            ],
        }
    )

    merchant_segments = pd.DataFrame(
        {
            "segment": [
                "跨境电商",
                "旅游出行",
                "数字娱乐",
                "教育服务",
                "O2O生活",
                "金融科技",
            ],
            "avg_txn": [78, 240, 32, 120, 18, 265],
            "monthly_volume_m": [920, 640, 580, 230, 760, 310],
            "activation_days": [35, 42, 21, 55, 28, 47],
            "retention_90d": [0.84, 0.78, 0.82, 0.69, 0.76, 0.73],
            "gmv_b": [12.5, 18.4, 9.1, 4.3, 7.8, 10.6],
        }
    )

    timeline = pd.date_range("2023-01-01", periods=30, freq="M")
    total_volume_index = (
        1000
        * (1 + np.linspace(0, 0.35, len(timeline)))
        * (1 + 0.06 * np.sin(np.arange(len(timeline)) / 1.8))
    )
    wallet_penetration = 52 + np.linspace(0, 11, len(timeline)) + np.random.normal(
        0, 0.8, len(timeline)
    )
    fraud_rate = 0.32 - np.linspace(0, 0.08, len(timeline)) + np.random.normal(
        0, 0.015, len(timeline)
    )

    performance_trend = pd.DataFrame(
        {
            "date": timeline,
            "volume_index": total_volume_index,
            "wallet_penetration": wallet_penetration,
            "fraud_rate": fraud_rate,
        }
    )

    consumer_activity = pd.DataFrame(
        {
            "segment": ["跨境游客", "内容电商粉丝", "O2O本地生活", "数字娱乐订阅"],
            "daily_active_m": [3.1, 5.4, 4.8, 2.3],
            "weekly_active_m": [8.6, 12.2, 10.5, 5.9],
            "monthly_active_m": [24, 38, 32, 18],
            "avg_txn_daily": [1.1, 1.6, 1.4, 1.8],
            "avg_txn_weekly": [3.4, 5.1, 4.6, 6.2],
            "avg_txn_monthly": [7.8, 11.4, 10.2, 14.5],
            "retention_30d": [0.55, 0.61, 0.58, 0.66],
            "retention_90d": [0.38, 0.45, 0.41, 0.56],
            "avg_order_value": [320, 68, 45, 22],
        }
    )

    retention_months = pd.date_range("2024-01-01", periods=12, freq="M")
    monthly_active_total = 95 + 6 * np.sin(np.linspace(0, 1.5 * np.pi, len(retention_months))) + np.linspace(
        0, 8, len(retention_months)
    )
    avg_txn_month = 9.5 + 0.8 * np.sin(np.linspace(0, 1.8 * np.pi, len(retention_months)))
    avg_order_value_trend = 58 + 6 * np.sin(
        np.linspace(0, 2.2 * np.pi, len(retention_months)) + 0.3
    )

    consumer_retention_trend = pd.DataFrame(
        {
            "month": retention_months,
            "monthly_active_total_m": monthly_active_total.round(1),
            "avg_txn_monthly": avg_txn_month.round(1),
            "avg_order_value": avg_order_value_trend.round(0),
        }
    )

    return {
        "global_kpis": global_kpis,
        "region_summary": region_summary,
        "partner_penetration": partner_penetration,
        "merchant_segments": merchant_segments,
        "performance_trend": performance_trend,
        "country_coverage": country_coverage,
        "consumer_activity": consumer_activity,
        "consumer_retention_trend": consumer_retention_trend,
    }


data = load_demo_data()

st.sidebar.markdown(
    "<div style='font-size:1.5rem;font-weight:600;'>Alipay+ Dashboard Demo</div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<div style='font-size:1.3rem;font-weight:400;'>by 侯良语Allen</div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("#### 📊 板块导航")
radio_options = (
    "指标体系思维导图",
    "业务总览",
    "合作伙伴渗透",
    "商户旅程洞察",
    "消费者旅程洞察",
)
if MAP_AVAILABLE:
    radio_options = radio_options + ("Alipay+北美市场策略",)
radio_options = radio_options + ("Alipay+ Fintech生态",)

analysis_view = st.sidebar.radio(
    "板块选择",
    radio_options,
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 项目说明")
st.sidebar.write(
    "该 Demo 旨在直观呈现候选人对 Alipay+ 业务的快速学习理解。\n\n"
    "数据基于公开口径与假设，仅用于本次面试演示。"
)
st.sidebar.markdown("---")
portfolio_folder = Path(__file__).with_name("portfolio")
if portfolio_folder.exists():
    st.sidebar.markdown("### 📎 其他作品")
    for item in sorted(portfolio_folder.iterdir()):
        if item.is_file():
            title_map = [
                ("配送站评分", "Amazon配送站评分系统"),
                ("数据中台", "Amazon数据中台"),
            ]
            display_name = next(
                (label for key, label in title_map if key in item.stem),
                item.stem.replace("_", " "),
            )
            with open(item, "rb") as file_bytes:
                st.sidebar.download_button(
                    label=display_name,
                    data=file_bytes,
                    file_name=item.name,
                    mime="application/octet-stream",
                )


def render_mindmap():
    # st.markdown('<div class="section-header">🧭 指标体系思维导图</div>', unsafe_allow_html=True)
    if Image is None:
        st.error("缺少 Pillow 库，请运行 `pip install pillow` 后重启应用。")
    elif mindmap_path.exists():
        with Image.open(mindmap_path) as img:
            width = img.width
            st.image(img,  width=width)
    else:
        st.warning(
            "找不到思维导图图片，请将文件 `alipay_mindmap.png` 放到 `assets/` 目录后刷新页面。"
        )


def render_alipay_fintech():
    """渲染 Alipay+ Fintech 图片"""
    if Image is None:
        st.error("缺少 Pillow 库，请运行 `pip install pillow` 后重启应用。")
    elif alipay_fintech_path.exists():
        with Image.open(alipay_fintech_path) as img:
            width = img.width
            st.image(img, width=width)
    else:
        st.warning(
            f"找不到图片文件，请将文件 `Alipay Fintech.png` 放到 `assets/` 目录后刷新页面。"
        )


def render_global_overview():
    # st.markdown('<div class="section-header">🌍 业务总览</div>', unsafe_allow_html=True)

    st.info(
        "Alipay+ 聚焦全球出海电商、旅游与本地生活场景，通过统一钱包和营销网络帮助商户接入40+ "
        "种跨境支付方式与营销权益。"
    )

    col_metrics = st.columns(3)
    for idx, row in data["global_kpis"].iterrows():
        with col_metrics[idx % 3]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size:1.2rem;">{row['metric']}</div>
                    <div style="font-size:2rem;font-weight:700;">{row['value']}</div>
                    <div style="font-size:0.9rem;opacity:0.9;">{row['delta']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### 🗺️ 全球覆盖洞察")
    region_geo = data["region_summary"].copy()
    region_geo_coords = {
        "东南亚": (3.0, 115.0),
        "东北亚": (40.0, 135.0),
        "欧洲": (50.0, 10.0),
        "中东": (25.0, 50.0),
        "拉美": (-10.0, -60.0),
        "非洲": (2.0, 20.0),
    }
    region_geo[["lat", "lon"]] = region_geo["region"].map(region_geo_coords).apply(pd.Series)

    st.markdown("#### 区域GMV与增速")
    gmv_growth_fig = px.scatter_geo(
        region_geo,
        lat="lat",
        lon="lon",
        size="volume_billion_usd",
        color="gmv_growth_pct",
        color_continuous_scale="YlGnBu",
        size_max=70,
        hover_name="region",
        hover_data={
            "volume_billion_usd": ":.1f",
            "gmv_growth_pct": ":.1f",
            "merchant_millions": ":.1f",
            "wallet_users_millions": ":.0f",
        },
        title="区域GMV气泡图（气泡大小=GMV，颜色=增速）",
    )
    gmv_growth_fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        geo=dict(
            scope="world",
            projection_type="natural earth",
            showland=True,
            landcolor="#f9fafb",
            showcountries=True,
            countrycolor="#cbd5f5",
        ),
        coloraxis_colorbar=dict(title="增速(%)"),
    )
    st.plotly_chart(gmv_growth_fig, use_container_width=True)

    st.markdown("#### 区域商户和C端消费者表现")
    merchant_col, consumer_col = st.columns(2)

    with merchant_col:
        st.markdown("**商户规模 & 活跃度**")
        merchant_fig = px.scatter_geo(
            region_geo,
            lat="lat",
            lon="lon",
            size="merchant_millions",
            color="merchant_activity_index",
            color_continuous_scale="PuBu",
            size_max=55,
            hover_name="region",
            hover_data={
                "merchant_millions": ":.1f",
                "merchant_activity_index": ":.0f",
                "volume_billion_usd": ":.1f",
            },
        )
        merchant_fig.update_layout(
            height=420,
            margin=dict(l=0, r=0, t=20, b=0),
            geo=dict(
                scope="world",
                projection_type="natural earth",
                showland=True,
                landcolor="#f9fafb",
                showcountries=True,
                countrycolor="#cbd5f5",
            ),
            coloraxis_colorbar=dict(title="活跃度指数"),
        )
        st.plotly_chart(merchant_fig, use_container_width=True)

    with consumer_col:
        st.markdown("**C端规模 & 活跃度**")
        consumer_fig = px.scatter_geo(
            region_geo,
            lat="lat",
            lon="lon",
            size="wallet_users_millions",
            color="consumer_activity_index",
            color_continuous_scale="BuGn",
            size_max=55,
            hover_name="region",
            hover_data={
                "wallet_users_millions": ":.0f",
                "consumer_activity_index": ":.0f",
                "volume_billion_usd": ":.1f",
            },
        )
        consumer_fig.update_layout(
            height=420,
            margin=dict(l=0, r=0, t=20, b=0),
            geo=dict(
                scope="world",
                projection_type="natural earth",
                showland=True,
                landcolor="#f9fafb",
                showcountries=True,
                countrycolor="#cbd5f5",
            ),
            coloraxis_colorbar=dict(title="活跃度指数"),
        )
        st.plotly_chart(consumer_fig, use_container_width=True)

    # st.markdown(
    #     '<div class="data-source">数据来源: Alipay+ 官方发布、公开财报、面试Demo假设数据</div>',
    #     unsafe_allow_html=True,
    # )


def render_partner_penetration():
    # st.markdown(
    #     '<div class="section-header">🤝 合作伙伴渗透</div>', unsafe_allow_html=True
    # )
    st.info(
        "重点关注 Alipay+ 与主流电商、钱包的合作深度，识别下一阶段的增量机会与竞对压力。"
    )

    sorted_partners = data["partner_penetration"].sort_values("gmv_b", ascending=False)
    partner_type_order = list(dict.fromkeys(sorted_partners["partner_type"].tolist()))
    type_tabs = st.tabs(partner_type_order)

    for tab, partner_type in zip(type_tabs, partner_type_order):
        with tab:
            subset = sorted_partners[sorted_partners["partner_type"] == partner_type]
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=subset["partner"],
                    y=subset["gmv_b"] * subset["alipay_plus_share"],
                    name="Alipay+ GMV",
                    marker_color="#1677ff",
                )
            )
            fig.add_trace(
                go.Bar(
                    x=subset["partner"],
                    y=subset["gmv_b"] * subset["primary_competitor_share"],
                    name="主要竞对 GMV",
                    marker_color="#f97316",
                    text=subset["primary_competitor"],
                    textposition="inside",
                    textfont=dict(color="#ffffff", size=12),
                    insidetextanchor="middle",
                )
            )
            fig.add_trace(
                go.Bar(
                    x=subset["partner"],
                    y=subset["gmv_b"] * subset["other_competitors_share"],
                    name="其他竞对 GMV",
                    marker_color="#9ca3af",
                )
            )
            fig.update_layout(
                barmode="stack",
                title=f"{partner_type} GMV结构（十亿美元）",
                xaxis_tickangle=-25,
                height=420,
                legend_title="收单服务商",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔍 竞对与机会")
    opportunity_table = sorted_partners.copy()
    opportunity_table["提升策略"] = [
        "内容电商联合营销+全链路风控共建",
        "直播间小额支付链路加速+风控白名单",
        "跨境钱包&旅游场景联名权益",
        "新马泰线下O2O钱包组合打法",
        "线下场景+高速公路无感支付扩展",
        "B2B发票和企业支付联动",
        "便利店二维码+BNPL联动补齐",
        "韩日本地钱包岚图营销",
    ]
    opportunity_table = opportunity_table.rename(
        columns={
            "partner": "合作伙伴",
            "region": "重点区域",
            "gmv_b": "平台GMV(十亿美元)",
            "alipay_plus_share": "Alipay+渗透率",
            "primary_competitor": "主要竞对",
            "primary_competitor_share": "主要竞对渗透率",
            "other_competitors_share": "其他竞对渗透率",
            "partner_type": "合作伙伴类型",
        }
    )
    st.dataframe(opportunity_table, use_container_width=True)

    # st.markdown(
    #     '<div class="data-source">数据来源: Alipay+ 市场宣传、公开资料、演示假设</div>',
    #     unsafe_allow_html=True,
    # )


def render_merchant_insights():
    # st.markdown(
    #     '<div class="section-header">🧭 商户旅程洞察</div>', unsafe_allow_html=True
    # )
    st.info("拆解核心商户分层的激活速度、交易规模与留存表现，定位策略优先级。")

    segments = data["merchant_segments"].copy()
    segments["retention_90d_pct"] = segments["retention_90d"] * 100
    col1, col2 = st.columns((10, 2))

    with col1:
        fig = px.scatter(
            segments,
            x="activation_days",
            y="retention_90d",
            size="gmv_b",
            size_max=90,
            color="segment",
            custom_data=[
                "segment",
                "gmv_b",
                "monthly_volume_m",
                "retention_90d_pct",
            ],
            labels={
                "activation_days": "激活天数(T+)",
                "retention_90d": "90日留存率",
                "gmv_b": "GMV (十亿美元)",
            },
            title="激活速度 vs 留存表现",
        )
        fig.update_traces(
            marker=dict(
                sizemode="area",
                sizeref=2.0 * max(segments["gmv_b"]) / (70**2),
                sizemin=10,
            ),
            hovertemplate=(
                "场景: %{customdata[0]}<br>"
                "GMV: %{customdata[1]:.1f} Bn USD<br>"
                "月交易额: %{customdata[2]:.0f} M USD<br>"
                "激活天数: %{x} 天<br>"
                "90日留存率: %{customdata[3]:.1f}%<extra></extra>"
            ),
        )
        fig.update_layout(height=430, yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric("平均激活天数", f"{segments['activation_days'].mean():.0f} 天", "-8 天")
        st.metric("90天留存率", f"{segments['retention_90d'].mean()*100:.1f}%", "+2.5%")
        st.metric(
            "月GMV均值", f"${segments['monthly_volume_m'].mean():.0f}M", "+$45M"
        )

    st.markdown("### 🧩 策略建议画布")

    recommendations = pd.DataFrame(
        {
            "场景": ["跨境电商", "旅游出行", "数字娱乐", "O2O生活"],
            "关键痛点": [
                "多钱包接入成本高",
                "入境支付体验断层",
                "高峰期并发与风控",
                "线下扫码对账繁琐",
            ],
            "数据指标": [
                "成功率、钱包渗透率、营销ROI",
                "入境旅客客单价、汇率波动成本",
                "并发请求、限额命中率、3DS转化",
                "线下流水覆盖、对账时延、退款效率",
            ],
            "打法建议": [
                "统一支付路由+跨境营销权益市场",
                "Alipay+ Tour Pass + OTA联营模型",
                "流量分流路由+实时风控共识机制",
                "无感支付+开放计次权益结算",
            ],
        }
    )
    st.dataframe(recommendations, use_container_width=True)


def render_consumer_insights():
    # st.markdown(
    #     '<div class="section-header">👥 消费者旅程洞察</div>', unsafe_allow_html=True
    # )
    st.info(
        "聚焦C端钱包用户的活跃规模、留存表现以及交易频次，识别核心客群与运营杠杆。"
    )

    activity = data["consumer_activity"].copy()
    total_monthly_active = activity["monthly_active_m"].sum()
    weighted_30d = (
        (activity["retention_30d"] * activity["monthly_active_m"]).sum()
        / total_monthly_active
    )
    weighted_90d = (
        (activity["retention_90d"] * activity["monthly_active_m"]).sum()
        / total_monthly_active
    )
    weighted_freq = (
        (activity["avg_txn_monthly"] * activity["monthly_active_m"]).sum()
        / total_monthly_active
    )

    col_kpis = st.columns(3)
    with col_kpis[0]:
        st.metric("月活跃用户", f"{total_monthly_active:.0f}M", "+6% vs Q4")
    with col_kpis[1]:
        st.metric("30日留存（加权）", f"{weighted_30d*100:.1f}%", "+2.3pct")
    with col_kpis[2]:
        st.metric("月均交易次数（加权）", f"{weighted_freq:.1f}", "+0.4x")

    st.markdown("### 📈 活跃规模与交易表现走势")
    retention_trend = data["consumer_retention_trend"]
    trend_fig = go.Figure()
    trend_fig.add_trace(
        go.Bar(
            x=retention_trend["month"],
            y=retention_trend["monthly_active_total_m"],
            name="月活跃用户(M)",
            marker_color="#60a5fa",
            opacity=0.7,
        )
    )
    trend_fig.add_trace(
        go.Scatter(
            x=retention_trend["month"],
            y=retention_trend["avg_txn_monthly"],
            name="月均交易次数",
            mode="lines+markers",
            line=dict(color="#16a34a", width=3),
            yaxis="y2",
        )
    )
    trend_fig.add_trace(
        go.Scatter(
            x=retention_trend["month"],
            y=retention_trend["avg_order_value"],
            name="平均客单价(USD)",
            mode="lines+markers+text",
            line=dict(color="#2563eb", dash="dash", width=3),
            text=retention_trend["avg_order_value"].apply(lambda v: f"${v:.0f}"),
            textposition="top center",
            textfont=dict(color="#1d4ed8"),
            yaxis="y2",
        )
    )
    trend_fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        barmode="overlay",
        yaxis=dict(title="月活跃(M)"),
        yaxis2=dict(
            title="交易表现",
            overlaying="y",
            side="right",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown("### 🔄 客群交易频次热力图")
    freq_matrix = (
        activity.set_index("segment")[
            ["avg_txn_daily", "avg_txn_weekly", "avg_txn_monthly"]
        ]
        .rename(
            columns={
                "avg_txn_daily": "日均交易次数",
                "avg_txn_weekly": "周均交易次数",
                "avg_txn_monthly": "月均交易次数",
            }
        )
    )
    heatmap_fig = px.imshow(
        freq_matrix,
        text_auto=".1f",
        color_continuous_scale="YlGnBu",
        aspect="auto",
    )
    heatmap_fig.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title="次数"),
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)

    st.markdown("### 🧭 综合指标看板")
    display_cols = [
        "segment",
        "daily_active_m",
        "weekly_active_m",
        "monthly_active_m",
        "retention_30d",
        "retention_90d",
        "avg_txn_monthly",
        "avg_order_value",
    ]
    renamed_cols = {
        "segment": "用户客群",
        "daily_active_m": "日活(M)",
        "weekly_active_m": "周活(M)",
        "monthly_active_m": "月活(M)",
        "retention_30d": "30日留存",
        "retention_90d": "90日留存",
        "avg_txn_monthly": "月均交易次数",
        "avg_order_value": "平均客单价(USD)",
    }
    st.dataframe(
        activity[display_cols]
        .rename(columns=renamed_cols)
        .style.format(
            {
                "日活(M)": "{:.1f}",
                "周活(M)": "{:.1f}",
                "月活(M)": "{:.0f}",
                "30日留存": "{:.0%}",
                "90日留存": "{:.0%}",
                "月均交易次数": "{:.1f}",
                "平均客单价(USD)": "${:.0f}",
            }
        ),
        use_container_width=True,
    )

    # st.markdown(
    #     '<div class="data-source">数据来源: Alipay+ 用户洞察实验室、面试演示假设数据</div>',
    #     unsafe_allow_html=True,
    # )


def render_north_america_map():
    """渲染全亚洲场景地图"""
    if not MAP_AVAILABLE:
        st.error("⚠️ 无法加载地图模块，请确保 `create_north_america_map.py` 文件存在。")
        return
    
    st.info(
        "🌏 展示亚洲国家赴美短期旅游游客（包括中国、日韩、东南亚、南亚等）在北美地区的消费场景分布。"
        "聚焦短期旅游生活场景，包括旅游购物、餐饮、住宿等高频消费场景。"
    )
    
    # 创建全亚洲场景地图
    with st.spinner("正在生成全亚洲场景地图..."):
        try:
            fig_asia = create_asia_map_with_plotly(return_fig=True)
            if fig_asia is None:
                st.error("❌ 全亚洲场景地图生成失败，请检查plotly库是否正确安装。")
                return
            
            # 调整地图高度以适应Streamlit界面
            fig_asia.update_layout(height=700)
            
            # 显示地图
            st.plotly_chart(fig_asia, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ 生成全亚洲场景地图时出错: {str(e)}")
            st.exception(e)


def render_north_america_strategy():
    """渲染北美市场策略：先显示地图，再显示策略分析"""
    # 先渲染地图
    render_north_america_map()
    
    # 添加分隔
    st.markdown("---")
    st.markdown("## 📊 Alipay+ 北美市场拓展策略")
    
    # 再渲染策略
    render_alipay_plus_strategy()


def render_alipay_plus_strategy():
    """渲染Alipay+北美市场策略分析海报 - 信息图表风格"""
    import streamlit.components.v1 as components
    
    # 创建完整的HTML文档，包含CSS和内容
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', 'Microsoft YaHei', Arial, sans-serif;
                background: #f5f5f5;
            }
            
            .infographic-container {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 50%, #a8c0d0 100%);
                padding: 3rem 2rem;
                border-radius: 20px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0,0,0,0.15);
                margin: 2rem auto;
                max-width: 1400px;
            }
            
            .infographic-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 10px,
                    rgba(255,255,255,0.05) 10px,
                    rgba(255,255,255,0.05) 20px
                );
                pointer-events: none;
            }
            
            .infographic-title {
                text-align: center;
                font-family: 'Inter', sans-serif;
                font-size: 3rem;
                font-weight: 800;
                color: #1a1a1a;
                margin-bottom: 0.5rem;
                letter-spacing: -1px;
                position: relative;
                z-index: 1;
            }
            
            .infographic-subtitle {
                text-align: center;
                font-family: 'Inter', sans-serif;
                font-size: 1.2rem;
                color: #4a5568;
                margin-bottom: 3rem;
                position: relative;
                z-index: 1;
            }
            
            .timeline-container {
                position: relative;
                margin: 3rem 0;
                z-index: 1;
            }
            
            .timeline-line {
                height: 4px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                border-radius: 2px;
                position: relative;
                margin: 0 5%;
                box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
            }
            
            .timeline-node {
                position: absolute;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                top: -28px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: transform 0.3s ease;
            }
            
            .timeline-node:hover {
                transform: scale(1.1);
            }
            
            .info-block {
                background: white;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-left: 5px solid;
                position: relative;
                z-index: 1;
            }
            
            .info-block:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 35px rgba(0,0,0,0.15);
            }
            
            .info-block-hex {
                background: white;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                border: 3px solid #e2e8f0;
                position: relative;
                z-index: 1;
            }
            
            .info-block-title {
                font-family: 'Inter', sans-serif;
                font-size: 1.3rem;
                font-weight: 700;
                margin-bottom: 0.8rem;
                color: #1a1a1a;
            }
            
            .info-block-content {
                font-family: 'Inter', sans-serif;
                font-size: 0.95rem;
                line-height: 1.6;
                color: #4a5568;
            }
            
            .stat-number {
                font-size: 2.5rem;
                font-weight: 800;
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0.5rem 0;
            }
            
            .stat-label {
                font-size: 0.9rem;
                color: #718096;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }
            
            .strategy-badge {
                display: inline-block;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 0.3rem;
                color: white;
            }
            
            .grid-row {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 1rem;
                margin: 2rem 0;
                width: 100%;
                align-items: stretch;
            }
            
            .info-block, .info-block-hex {
                min-height: 220px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
            }
            
            .info-block-hex {
                grid-column: span 1;
            }
            
            /* 确保卡片与时间线节点对齐 */
            .grid-row > div:nth-child(1) {
                grid-column: 1;
            }
            .grid-row > div:nth-child(2) {
                grid-column: 2;
            }
            .grid-row > div:nth-child(3) {
                grid-column: 3;
            }
            .grid-row > div:nth-child(4) {
                grid-column: 4;
            }
            .grid-row > div:nth-child(5) {
                grid-column: 5;
            }
        </style>
    </head>
    <body>
    <div class="infographic-container">
        <div class="infographic-title">ALIPAY+ 北美市场拓展策略</div>
        <div class="infographic-subtitle">基于公开资料与市场洞察的战略分析</div>
        
        <!-- 中央时间线 -->
        <div class="timeline-container">
            <div class="timeline-line">
                <div class="timeline-node" style="left: 0%; background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);">💖</div>
                <div class="timeline-node" style="left: 25%; background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);">📊</div>
                <div class="timeline-node" style="left: 50%; background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);">🚀</div>
                <div class="timeline-node" style="left: 75%; background: linear-gradient(135deg, #55efc4 0%, #00b894 100%);">💡</div>
                <div class="timeline-node" style="left: 100%; background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);">✅</div>
            </div>
        </div>
        
        <!-- 第一行信息块：所有编号卡片01-05连续排列 -->
        <div class="grid-row">
            <!-- 目标客户 01 -->
            <div class="info-block" style="border-left-color: #ff6b9d;">
                <div class="info-block-title">目标客户 01</div>
                <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">👥</div>
                <div class="stat-number">8.5M</div>
                <div class="stat-label">年入境游客数</div>
                <div class="info-block-content" style="margin-top: 1rem; font-size: 0.85rem;">
                    中国游客为主<br>年增长15.2%
                </div>
            </div>
            
            <!-- 市场规模 02 -->
            <div class="info-block" style="border-left-color: #a29bfe;">
                <div class="info-block-title">市场规模 02</div>
                <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">📈</div>
                <div class="stat-number">$32.5B</div>
                <div class="stat-label">2028年预测GMV</div>
                <div class="info-block-content" style="margin-top: 1rem; font-size: 0.85rem;">
                    CAGR 38.5%<br>2024: $8.2B
                </div>
            </div>
            
            <!-- 业务现状 03 -->
            <div class="info-block" style="border-left-color: #74b9ff;">
                <div class="info-block-title">业务现状 03</div>
                <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">📊</div>
                <div class="stat-number">0.6%</div>
                <div class="stat-label">商户覆盖率</div>
                <div class="info-block-content" style="margin-top: 1rem; font-size: 0.85rem;">
                    支付成功率 98.5%<br>用户渗透率 15%
                </div>
            </div>
            
            <!-- 核心策略 04 -->
            <div class="info-block" style="border-left-color: #55efc4;">
                <div class="info-block-title">核心策略 04</div>
                <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">🎯</div>
                <div style="margin-top: 1rem;">
                    <span class="strategy-badge" style="background: #667eea;">商户网络</span>
                    <span class="strategy-badge" style="background: #764ba2;">钱包合作</span>
                    <span class="strategy-badge" style="background: #f093fb;">场景深耕</span>
                </div>
            </div>
            
            <!-- 竞对分析 05 -->
            <div class="info-block" style="border-left-color: #ffeaa7;">
                <div class="info-block-title">竞对分析 05</div>
                <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">⚔️</div>
                <div class="info-block-content" style="margin-top: 1rem; font-size: 0.9rem;">
                    <div style="margin: 0.5rem 0;"><strong>Stripe:</strong> 35%</div>
                    <div style="margin: 0.5rem 0;"><strong>PayPal:</strong> 24%</div>
                    <div style="margin: 0.5rem 0;"><strong>Square:</strong> 12%</div>
                    <div style="margin: 0.5rem 0;"><strong>Adyen:</strong> 8%</div>
                    <div style="margin: 0.5rem 0;"><strong>Toast:</strong> 5%</div>
                    <div style="margin: 0.5rem 0;"><strong>Alipay+:</strong> 12%</div>
                    <div style="margin: 0.5rem 0;"><strong>其他:</strong> 4%</div>
                </div>
            </div>
        </div>
        
        <!-- 第二行信息块：对应的文本说明卡片 -->
        <div class="grid-row">
            <!-- 客户细分说明（对应01） -->
            <div class="info-block-hex">
                <div class="info-block-title">客户细分</div>
                <div class="info-block-content">
                    <strong>中国游客：</strong>年入境约350万人次，平均停留12天，客单价$320，高频消费场景集中在旅游购物、餐饮、住宿、交通。<br><br>
                    <strong>日韩游客：</strong>年入境约280万人次，平均停留10天，客单价$380，偏好高端购物和体验式消费。<br><br>
                    <strong>东南亚游客：</strong>年入境约220万人次，平均停留8天，客单价$240，注重性价比，偏好购物和餐饮场景。
                </div>
            </div>
            
            <!-- 规模详解说明（对应02） -->
            <div class="info-block-hex">
                <div class="info-block-title">规模详解</div>
                <div class="info-block-content">
                    <strong>市场总量：</strong>2024年亚洲赴美游客跨境支付GMV约$56B，预计2028年达$125B，亚洲游客贡献占比从45%提升至55%。<br><br>
                    <strong>增长驱动：</strong>亚洲游客年增长15.2%，平均停留时间延长，人均消费提升年增长8.3%，旅游消费升级趋势明显。<br><br>
                    <strong>细分市场：</strong>旅游购物$18B，餐饮服务$6.5B，住宿交通$5.2B，娱乐体验$2.8B。
                </div>
            </div>
            
            <!-- 现状详解说明（对应03） -->
            <div class="info-block-hex">
                <div class="info-block-title">现状详解</div>
                <div class="info-block-content">
                    <strong>商户覆盖：</strong>目前主要覆盖高端零售品牌（梅西百货、Nordstrom、Saks Fifth Avenue、Tory Burch、Kate Spade等）、机场免税店、部分连锁零售商（Target、CVS、Walgreens、7-Eleven部分门店），以及旅游热点区域的餐饮和住宿商户。目标商户总数约18万家（聚焦旅游相关场景），当前实际接入商户约800-1200家，覆盖率约0.4-0.7%，主要集中在旅游购物和餐饮场景。地图上标注的为代表性商户品牌。<br><br>
                    <strong>用户渗透：</strong>15%亚洲赴美游客使用Alipay+，年交易额$8.2B。中国游客渗透率最高约22%，日韩游客约12%，东南亚游客约8%。主要使用场景为旅游购物（65%）、餐饮（20%）、住宿交通（10%）、其他（5%）。<br><br>
                    <strong>技术表现：</strong>支付成功率98.5%，平均处理时间1.2秒，风控拦截率0.15%，用户满意度4.3/5.0。主要挑战是旅游场景商户网络覆盖不足，以及非中国游客的品牌认知度较低。
                </div>
            </div>
            
            <!-- 执行路径说明（对应04） -->
            <div class="info-block-hex">
                <div class="info-block-title">执行路径</div>
                <div class="info-block-content">
                    <strong>第一阶段（2024-2025）：</strong>聚焦旅游购物和餐饮场景，重点拓展中国游客高频消费商户，建立商户网络和品牌认知，目标商户覆盖率达3.5%，用户渗透率达22%。<br><br>
                    <strong>第二阶段（2026-2027）：</strong>拓展日韩和东南亚游客市场，深化旅游全链路场景（购物、餐饮、住宿、交通），提升用户渗透率至28%，GMV达$22B。<br><br>
                    <strong>第三阶段（2028+）：</strong>实现规模化增长，商户覆盖率达8%，用户渗透率达35%，GMV突破$32.5B，成为亚洲游客赴美首选支付方式。
                </div>
            </div>
            
            <!-- 优势劣势说明（对应05） -->
            <div class="info-block-hex">
                <div class="info-block-title">优势劣势</div>
                <div class="info-block-content">
                    <strong>核心优势：</strong>①亚洲市场经验丰富，40+钱包网络覆盖；②技术能力强，支付成功率高；③品牌认知度高，华人用户信任度强；④跨境支付场景成熟。<br><br>
                    <strong>主要劣势：</strong>①本地商户网络不足，覆盖率低；②与Stripe/PayPal相比，本地化服务能力弱；③监管合规成本高；④品牌在非华人群体中认知度低。<br><br>
                    <strong>竞对市占率说明：</strong>基于2024年亚洲赴美游客跨境支付场景的商户收单市场份额估算。Alipay+的12%主要来自中国游客高频消费场景（旅游购物、餐饮），基于年交易额$8.2B与市场总量$68B的估算。Stripe/PayPal占据主导地位主要因其广泛的本地商户网络和成熟的支付基础设施。
                </div>
            </div>
        </div>
        
        <!-- 底部数据来源 -->
        <div style="text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 2px solid rgba(255,255,255,0.3); position: relative; z-index: 1;">
            <p style="color: #4a5568; font-size: 0.9rem; font-family: 'Inter', sans-serif;">
                <strong>数据来源：</strong>Alipay+公开资料、Statista、eMarketer、Pew Research Center、行业专家预测
            </p>
        </div>
    </div>
    </body>
    </html>
    """
    
    components.html(html_content, height=1400, scrolling=True)
    
    # 不再使用Plotly图表，使用纯HTML/CSS信息图表
    # 信息图表已在上面的HTML中完成渲染
    # 数据来源说明已包含在HTML中


if analysis_view == "指标体系思维导图":
    render_mindmap()
elif analysis_view == "业务总览":
    render_global_overview()
elif analysis_view == "合作伙伴渗透":
    render_partner_penetration()
elif analysis_view == "商户旅程洞察":
    render_merchant_insights()
elif analysis_view == "消费者旅程洞察":
    render_consumer_insights()
elif analysis_view == "Alipay+北美市场策略":
    render_north_america_strategy()
elif analysis_view == "Alipay+ Fintech生态":
    render_alipay_fintech()

st.markdown("---")
st.caption(
    "面试演示版本 · 更新于 "
    + datetime.now().strftime("%Y-%m-%d %H:%M")
    + " · 数据基于公开口径与假设，仅用于讨论。"
)


