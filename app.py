import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Amazon Sales Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

    /* ======================================================
       MAIN APPLICATION
    ====================================================== */

    .stApp {
        background: #f4f7fb;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       SIDEBAR
    ====================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #172033;
    }

    section[data-testid="stSidebar"] p {
        color: #64748b;
    }

    section[data-testid="stSidebar"] label {
        color: #334155 !important;
        font-weight: 600 !important;
    }


    /* ======================================================
       MAIN TITLE
    ====================================================== */

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #172033;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .main-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 28px;
    }


    /* ======================================================
       KPI CARDS
    ====================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 22px 22px 20px 22px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
        transition: all 0.25s ease;
        min-height: 135px;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
        border-color: #cbd5e1;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #172033 !important;
        font-size: 30px !important;
        font-weight: 800 !important;
    }


    /* ======================================================
       SECTION HEADINGS
    ====================================================== */

    .section-header {
        font-size: 25px;
        font-weight: 800;
        color: #172033;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }


    /* ======================================================
       TABS
    ====================================================== */

    button[data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 700;
        color: #64748b;
        padding: 13px 20px;
    }

    button[data-baseweb="tab"]:hover {
        color: #ea580c;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ea580c !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: #f97316 !important;
        height: 3px !important;
        border-radius: 5px;
    }


    /* ======================================================
       SELECT BOXES
    ====================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 10px;
        border-color: #e2e8f0;
        background-color: #ffffff;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #f97316;
    }


    /* ======================================================
       DATE INPUT
    ====================================================== */

    div[data-testid="stDateInput"] input {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }


    /* ======================================================
       MULTISELECT TAGS
    ====================================================== */

    span[data-baseweb="tag"] {
        background-color: #fff1e8 !important;
        color: #c2410c !important;
        border-radius: 7px !important;
    }


    /* ======================================================
       CHART AREA
    ====================================================== */

    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 18px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    }


    /* ======================================================
       DATA TABLE
    ====================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    }


    /* ======================================================
       INFO BOX
    ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border-left: 4px solid #f97316;
    }


    /* ======================================================
       SIDEBAR FILTER TITLE
    ====================================================== */

    .filter-title {
        font-size: 13px;
        font-weight: 800;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 20px;
        margin-bottom: 8px;
    }


    /* ======================================================
       INSIGHT BOXES
    ====================================================== */

    .insight-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #f97316;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
        margin-top: 10px;
    }

    .insight-label {
        font-size: 12px;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .insight-value {
        font-size: 19px;
        font-weight: 800;
        color: #172033;
        margin-top: 7px;
    }


    /* ======================================================
       FOOTER
    ====================================================== */

    .footer {
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
    }


    /* ======================================================
       REMOVE DEFAULT STREAMLIT FOOTER
    ====================================================== */

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }


    /* ======================================================
       MOBILE
    ====================================================== */

    @media (max-width: 768px) {

        .main-title {
            font-size: 28px;
        }

        .main-subtitle {
            font-size: 14px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
        }
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Amazon Sale Report.csv")

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Convert Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # Convert Amount
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        ).fillna(0)

    # Convert Quantity
    if "Qty" in df.columns:
        df["Qty"] = pd.to_numeric(
            df["Qty"],
            errors="coerce"
        ).fillna(0)

    # Create Customer Type
    if "Customer Type" not in df.columns:

        if "B2B" in df.columns:

            df["Customer Type"] = (
                df["B2B"]
                .astype(str)
                .str.lower()
                .map({
                    "true": "B2B",
                    "1": "B2B",
                    "yes": "B2B",
                    "false": "B2C",
                    "0": "B2C",
                    "no": "B2C"
                })
                .fillna("B2C")
            )

        else:

            df["Customer Type"] = "B2C"

    # Validate columns
    if "Date" not in df.columns:
        st.error("Date column not found.")
        st.stop()

    if "Amount" not in df.columns:
        st.error("Amount column not found.")
        st.stop()

    # Remove invalid dates
    df = df.dropna(subset=["Date"])

    return df


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛒 Sales Intelligence")

st.sidebar.caption(
    "Interactive Amazon sales analytics"
)

st.sidebar.markdown(
    '<div class="filter-title">Filters</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# Category
# ------------------------------------------------------------

if "Category" in df.columns:

    categories = sorted(
        df["Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_category = st.sidebar.multiselect(
        "Category",
        categories,
        default=categories
    )

else:

    selected_category = []


# ------------------------------------------------------------
# Size
# ------------------------------------------------------------

if "Size" in df.columns:

    sizes = sorted(
        df["Size"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_size = st.sidebar.multiselect(
        "Size",
        sizes,
        default=sizes
    )

else:

    selected_size = []


# ------------------------------------------------------------
# Courier Status
# ------------------------------------------------------------

if "Courier Status" in df.columns:

    courier_statuses = sorted(
        df["Courier Status"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_courier = st.sidebar.multiselect(
        "Courier Status",
        courier_statuses,
        default=courier_statuses
    )

else:

    selected_courier = []


# ------------------------------------------------------------
# Customer Type
# ------------------------------------------------------------

customer_types = sorted(
    df["Customer Type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_customer_type = st.sidebar.multiselect(
    "Customer Type",
    customer_types,
    default=customer_types
)


# ------------------------------------------------------------
# Date
# ------------------------------------------------------------

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

st.sidebar.markdown(
    '<div class="filter-title">Date Range</div>',
    unsafe_allow_html=True
)

selected_dates = st.sidebar.date_input(
    "Select dates",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if "Category" in filtered_df.columns and selected_category:

    filtered_df = filtered_df[
        filtered_df["Category"]
        .astype(str)
        .isin(selected_category)
    ]


if "Size" in filtered_df.columns and selected_size:

    filtered_df = filtered_df[
        filtered_df["Size"]
        .astype(str)
        .isin(selected_size)
    ]


if "Courier Status" in filtered_df.columns and selected_courier:

    filtered_df = filtered_df[
        filtered_df["Courier Status"]
        .astype(str)
        .isin(selected_courier)
    ]


if selected_customer_type:

    filtered_df = filtered_df[
        filtered_df["Customer Type"]
        .astype(str)
        .isin(selected_customer_type)
    ]


# Date filter
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        &
        (filtered_df["Date"] <= end_date)
    ]


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Amazon Sales Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Interactive analytics dashboard for understanding '
    'revenue, products, customers, and operations.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["Amount"].sum()

total_units = filtered_df["Qty"].sum()


if "Order ID" in filtered_df.columns:

    total_orders = filtered_df["Order ID"].nunique()

else:

    total_orders = len(filtered_df)


if "SKU" in filtered_df.columns:

    total_products = filtered_df["SKU"].nunique()

else:

    total_products = 0


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        label="💰 Total Revenue",
        value=f"₹{total_revenue / 10000000:.2f} Cr"
    )


with kpi2:

    st.metric(
        label="📦 Units Sold",
        value=f"{total_units / 1000:.1f}K"
    )


with kpi3:

    st.metric(
        label="🧾 Orders",
        value=f"{total_orders / 1000:.1f}K"
    )


with kpi4:

    st.metric(
        label="🏷️ Products",
        value=f"{total_products / 1000:.1f}K"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Executive Overview",
        "🏆 Product Intelligence",
        "🚚 Operations",
        "🔬 Deep Analysis"
    ]
)


# ============================================================
# TAB 1 — EXECUTIVE OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-header">Executive Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Understand overall sales performance and category trends.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SALES PERFORMANCE
    # --------------------------------------------------------

    daily_sales = (
        filtered_df
        .groupby("Date", as_index=False)["Amount"]
        .sum()
        .sort_values("Date")
    )

    fig_sales = px.line(
        daily_sales,
        x="Date",
        y="Amount",
        title="Sales Performance Over Time",
        markers=True
    )

    fig_sales.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Revenue (₹)",
        hovermode="x unified",
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True,
        key="sales_trend_chart"
    )


    # --------------------------------------------------------
    # CATEGORY AND SIZE
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        if "Category" in filtered_df.columns:

            category_sales = (
                filtered_df
                .groupby("Category", as_index=False)["Amount"]
                .sum()
                .sort_values("Amount", ascending=False)
            )

            fig_category = px.bar(
                category_sales,
                x="Category",
                y="Amount",
                title="Revenue by Category",
                text_auto=".2s"
            )

            fig_category.update_layout(
                template="plotly_white",
                height=400,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True,
                key="category_revenue_chart"
            )


    with col2:

        if "Size" in filtered_df.columns:

            size_sales = (
                filtered_df
                .groupby("Size", as_index=False)["Amount"]
                .sum()
                .sort_values("Amount", ascending=False)
            )

            fig_size = px.bar(
                size_sales,
                x="Size",
                y="Amount",
                title="Revenue by Size",
                text_auto=".2s"
            )

            fig_size.update_layout(
                template="plotly_white",
                height=400,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_size,
                use_container_width=True,
                key="size_revenue_chart"
            )


# ============================================================
# TAB 2 — PRODUCT INTELLIGENCE
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-header">Product Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Identify the products and categories contributing most to sales.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    if "SKU" in filtered_df.columns:

        top_products = (
            filtered_df
            .groupby("SKU", as_index=False)["Amount"]
            .sum()
            .sort_values("Amount", ascending=False)
            .head(10)
        )

        fig_top_products = px.bar(
            top_products.sort_values("Amount"),
            x="Amount",
            y="SKU",
            orientation="h",
            title="Top 10 Products by Revenue",
            text_auto=".2s"
        )

        fig_top_products.update_layout(
            template="plotly_white",
            height=500,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_top_products,
            use_container_width=True,
            key="top_products_revenue_chart"
        )


    # --------------------------------------------------------
    # UNITS BY CATEGORY
    # --------------------------------------------------------

    if "Category" in filtered_df.columns:

        units_category = (
            filtered_df
            .groupby("Category", as_index=False)["Qty"]
            .sum()
            .sort_values("Qty", ascending=False)
        )

        fig_units_category = px.bar(
            units_category,
            x="Category",
            y="Qty",
            title="Units Sold by Category",
            text_auto=".2s"
        )

        fig_units_category.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_units_category,
            use_container_width=True,
            key="category_units_chart"
        )


    # --------------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------------

    if "SKU" in filtered_df.columns:

        product_table = (
            filtered_df
            .groupby("SKU")
            .agg(
                Revenue=("Amount", "sum"),
                Units=("Qty", "sum")
            )
            .sort_values("Revenue", ascending=False)
            .head(20)
            .reset_index()
        )

        product_table["Revenue"] = product_table["Revenue"].round(2)

        st.markdown(
            '<div class="section-header">Product Performance</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Top 20 products ranked by revenue.'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            product_table,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 3 — OPERATIONS
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-header">'
        'Operations & Customer Insights'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Analyze delivery status, customer segments, and geographic performance.'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # COURIER STATUS
    # --------------------------------------------------------

    with col1:

        if "Courier Status" in filtered_df.columns:

            courier_data = (
                filtered_df["Courier Status"]
                .value_counts()
                .reset_index()
            )

            courier_data.columns = [
                "Courier Status",
                "Count"
            ]

            fig_courier = px.pie(
                courier_data,
                names="Courier Status",
                values="Count",
                hole=0.55,
                title="Courier Status Distribution"
            )

            fig_courier.update_layout(
                template="plotly_white",
                height=400,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_courier,
                use_container_width=True,
                key="courier_status_chart"
            )


    # --------------------------------------------------------
    # CUSTOMER TYPE
    # --------------------------------------------------------

    with col2:

        customer_data = (
            filtered_df["Customer Type"]
            .value_counts()
            .reset_index()
        )

        customer_data.columns = [
            "Customer Type",
            "Count"
        ]

        fig_customer = px.pie(
            customer_data,
            names="Customer Type",
            values="Count",
            hole=0.55,
            title="Customer Type Distribution"
        )

        fig_customer.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_customer,
            use_container_width=True,
            key="customer_type_chart"
        )


    # --------------------------------------------------------
    # TOP STATES
    # --------------------------------------------------------

    if "ship-state" in filtered_df.columns:

        state_sales = (
            filtered_df
            .groupby("ship-state", as_index=False)["Amount"]
            .sum()
            .sort_values("Amount", ascending=False)
            .head(10)
        )

        fig_states = px.bar(
            state_sales.sort_values("Amount"),
            x="Amount",
            y="ship-state",
            orientation="h",
            title="Top 10 States by Revenue",
            text_auto=".2s"
        )

        fig_states.update_layout(
            template="plotly_white",
            height=500,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_states,
            use_container_width=True,
            key="top_states_chart"
        )


# ============================================================
# TAB 4 — DEEP ANALYSIS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-header">Deep Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Explore trends, relationships, and statistical patterns in the data.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------------------------

    monthly_df = filtered_df.copy()

    monthly_df["Month"] = (
        monthly_df["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_sales = (
        monthly_df
        .groupby("Month", as_index=False)["Amount"]
        .sum()
    )

    fig_monthly = px.bar(
        monthly_sales,
        x="Month",
        y="Amount",
        title="Monthly Revenue"
    )

    fig_monthly.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
        key="monthly_revenue_chart"
    )


    # --------------------------------------------------------
    # QUANTITY VS REVENUE
    # --------------------------------------------------------

    scatter_df = filtered_df[
        ["Qty", "Amount"]
    ].copy()

    scatter_df = scatter_df[
        (scatter_df["Qty"] >= 0) &
        (scatter_df["Amount"] >= 0)
    ]

    fig_scatter = px.scatter(
        scatter_df,
        x="Qty",
        y="Amount",
        title="Quantity vs Revenue",
        opacity=0.55,
        trendline=None
    )

    fig_scatter.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True,
        key="quantity_amount_scatter"
    )


    # ========================================================
    # CORRELATION ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-header">Correlation Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Explore relationships between quantity, revenue, and B2B transactions.'
        '</div>',
        unsafe_allow_html=True
    )


    correlation_columns = []

    if "Qty" in filtered_df.columns:
        correlation_columns.append("Qty")

    if "Amount" in filtered_df.columns:
        correlation_columns.append("Amount")

    if "B2B" in filtered_df.columns:
        correlation_columns.append("B2B")


    if len(correlation_columns) >= 2:

        correlation_df = filtered_df[
            correlation_columns
        ].copy()


        # Convert B2B values
        if "B2B" in correlation_df.columns:

            correlation_df["B2B"] = (
                correlation_df["B2B"]
                .astype(str)
                .str.lower()
                .map({
                    "true": 1,
                    "false": 0,
                    "1": 1,
                    "0": 0,
                    "yes": 1,
                    "no": 0
                })
            )


        # Convert columns to numeric
        for column in correlation_df.columns:

            correlation_df[column] = pd.to_numeric(
                correlation_df[column],
                errors="coerce"
            )


        correlation_df = correlation_df.dropna()


        if not correlation_df.empty:

            correlation_matrix = correlation_df.corr()


            fig_corr = px.imshow(
                correlation_matrix,
                text_auto=".2f",
                aspect="auto",
                title="Correlation Heatmap"
            )

            fig_corr.update_layout(
                template="plotly_white",
                height=450,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_corr,
                use_container_width=True,
                key="deep_correlation_heatmap"
            )


            st.info(
                """
                **How to read correlation:**

                • **+1.00** → Strong positive relationship

                • **0.00** → Little or no linear relationship

                • **-1.00** → Strong negative relationship

                Correlation shows association, not causation.
                """
            )


            st.markdown(
                '<div class="section-header">Correlation Values</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                correlation_matrix.round(2),
                use_container_width=True
            )


    # ========================================================
    # SUMMARY STATISTICS
    # ========================================================

    st.markdown(
        '<div class="section-header">Summary Statistics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Key calculated metrics for the currently selected data.'
        '</div>',
        unsafe_allow_html=True
    )


    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    revenue_per_unit = (
        total_revenue / total_units
        if total_units > 0
        else 0
    )


    stat1, stat2, stat3 = st.columns(3)


    with stat1:

        st.markdown(
            '<div class="insight-box">'
            '<div class="insight-label">Average Order Value</div>'
            f'<div class="insight-value">₹{avg_order_value:,.2f}</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with stat2:

        st.markdown(
            '<div class="insight-box">'
            '<div class="insight-label">Revenue per Unit</div>'
            f'<div class="insight-value">₹{revenue_per_unit:,.2f}</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with stat3:

        st.markdown(
            '<div class="insight-box">'
            '<div class="insight-label">Records Analyzed</div>'
            f'<div class="insight-value">{len(filtered_df):,}</div>'
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-header">💡 Key Business Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Automatically generated insights based on the selected filters.'
    '</div>',
    unsafe_allow_html=True
)


insight1, insight2, insight3 = st.columns(3)


# ------------------------------------------------------------
# TOP CATEGORY
# ------------------------------------------------------------

with insight1:

    if "Category" in filtered_df.columns and not filtered_df.empty:

        top_category = (
            filtered_df
            .groupby("Category")["Amount"]
            .sum()
            .idxmax()
        )

        st.markdown(
            '<div class="insight-box">'
            '<div class="insight-label">🏆 Top Revenue Category</div>'
            f'<div class="insight-value">{top_category}</div>'
            '</div>',
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# TOP PRODUCT
# ------------------------------------------------------------

with insight2:

    if "SKU" in filtered_df.columns and not filtered_df.empty:

        top_product = (
            filtered_df
            .groupby("SKU")["Amount"]
            .sum()
            .idxmax()
        )

        st.markdown(
            '<div class="insight-box">'
            '<div class="insight-label">⭐ Highest Revenue Product</div>'
            f'<div class="insight-value">{top_product}</div>'
            '</div>',
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# CUSTOMER SEGMENT
# ------------------------------------------------------------

with insight3:

    if not filtered_df.empty:

        dominant_customer = (
            filtered_df["Customer Type"]
            .value_counts()
            .idxmax()
        )

        st.markdown(
            '<div class="insight-box">'
            '<div class="insight-label">👥 Dominant Customer Segment</div>'
            f'<div class="insight-value">{dominant_customer}</div>'
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>Amazon Sales Intelligence</strong>
        &nbsp; • &nbsp;
        Interactive Sales Analytics Dashboard
        <br><br>
        Built with Python, Pandas, Plotly & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)