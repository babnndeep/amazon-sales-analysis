import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


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
# ENHANCED PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

/* -----------------------------------------------------------
   GLOBAL PAGE
----------------------------------------------------------- */

.stApp {
    background: linear-gradient(135deg, #f5f7fb 0%, #eef2f7 100%);
    color: #172033;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}


/* -----------------------------------------------------------
   MAIN HEADER
----------------------------------------------------------- */

.dashboard-header {
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1e293b 55%,
        #334155 100%
    );

    padding: 32px 36px;
    border-radius: 22px;
    margin-bottom: 28px;

    box-shadow:
        0 15px 35px rgba(15, 23, 42, 0.18);

    position: relative;
    overflow: hidden;
}

.dashboard-header::before {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(249, 115, 22, 0.12);
    top: -120px;
    right: -60px;
}

.dashboard-header::after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: rgba(59, 130, 246, 0.08);
    bottom: -100px;
    left: 35%;
}

.dashboard-title {
    color: white;
    font-size: 38px;
    font-weight: 800;
    margin: 0;
    position: relative;
    z-index: 2;
    letter-spacing: -1px;
}

.dashboard-subtitle {
    color: #cbd5e1;
    font-size: 16px;
    margin-top: 8px;
    position: relative;
    z-index: 2;
}

.header-badge {
    display: inline-block;
    margin-top: 18px;
    padding: 7px 15px;
    border-radius: 30px;
    background: rgba(249, 115, 22, 0.16);
    border: 1px solid rgba(249, 115, 22, 0.35);
    color: #fed7aa;
    font-size: 13px;
    font-weight: 600;
    position: relative;
    z-index: 2;
}


/* -----------------------------------------------------------
   SIDEBAR
----------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f8fafc 100%
    );

    border-right: 1px solid #e2e8f0;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

.sidebar-title {
    font-size: 23px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 5px;
}

.sidebar-subtitle {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 25px;
}

.filter-heading {
    color: #334155;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-top: 20px;
    margin-bottom: 8px;
}


/* -----------------------------------------------------------
   KPI CARDS
----------------------------------------------------------- */

.kpi-card {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #e2e8f0;
    border-radius: 18px;

    padding: 22px 22px 20px 22px;

    min-height: 145px;

    box-shadow:
        0 7px 20px rgba(15, 23, 42, 0.06);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;

    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-5px);

    box-shadow:
        0 15px 30px rgba(15, 23, 42, 0.12);

    border-color: #cbd5e1;
}

.kpi-card::after {
    content: "";
    position: absolute;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    right: -35px;
    top: -35px;
    background: rgba(249, 115, 22, 0.07);
}

.kpi-label {
    font-size: 13px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
    margin-top: 10px;
    line-height: 1.1;
}

.kpi-description {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 10px;
}


/* -----------------------------------------------------------
   SECTION HEADINGS
----------------------------------------------------------- */

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #172033;
    margin-top: 25px;
    margin-bottom: 5px;
}

.section-subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 18px;
}


/* -----------------------------------------------------------
   CHART CONTAINER
----------------------------------------------------------- */

.chart-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;

    padding: 18px;

    box-shadow:
        0 6px 18px rgba(15, 23, 42, 0.05);

    margin-bottom: 20px;
}


/* -----------------------------------------------------------
   INSIGHT CARDS
----------------------------------------------------------- */

.insight-card {
    background: linear-gradient(
        135deg,
        #fff7ed 0%,
        #ffffff 100%
    );

    border: 1px solid #fed7aa;
    border-left: 5px solid #f97316;

    border-radius: 14px;

    padding: 18px 20px;

    margin-top: 10px;

    box-shadow:
        0 6px 16px rgba(249, 115, 22, 0.06);
}

.insight-title {
    font-size: 13px;
    color: #9a3412;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.insight-value {
    font-size: 20px;
    color: #172033;
    font-weight: 800;
    margin-top: 5px;
}


/* -----------------------------------------------------------
   TABS
----------------------------------------------------------- */

button[data-baseweb="tab"] {
    font-size: 14px;
    font-weight: 700;
    color: #64748b;
    padding: 12px 20px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ea580c;
}

div[data-baseweb="tab-highlight"] {
    background-color: #f97316;
    height: 3px;
    border-radius: 3px;
}


/* -----------------------------------------------------------
   DATAFRAME / TABLE
----------------------------------------------------------- */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}


/* -----------------------------------------------------------
   BUTTONS
----------------------------------------------------------- */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #f97316;
    color: #ea580c;
}


/* -----------------------------------------------------------
   SELECTBOX
----------------------------------------------------------- */

div[data-baseweb="select"] > div {
    border-radius: 10px;
    border-color: #e2e8f0;
    background-color: white;
}


/* -----------------------------------------------------------
   DATE INPUT
----------------------------------------------------------- */

div[data-testid="stDateInput"] input {
    border-radius: 10px;
    border: 1px solid #e2e8f0;
}


/* -----------------------------------------------------------
   INFO MESSAGE
----------------------------------------------------------- */

div[data-testid="stAlert"] {
    border-radius: 12px;
}


/* -----------------------------------------------------------
   FOOTER
----------------------------------------------------------- */

.dashboard-footer {
    margin-top: 40px;
    padding: 22px;

    text-align: center;

    border-top: 1px solid #e2e8f0;

    color: #94a3b8;

    font-size: 12px;
}

.footer-brand {
    color: #475569;
    font-weight: 700;
}


/* -----------------------------------------------------------
   HIDE STREAMLIT DEFAULT ELEMENTS
----------------------------------------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* -----------------------------------------------------------
   MOBILE RESPONSIVENESS
----------------------------------------------------------- */

@media (max-width: 768px) {

    .dashboard-title {
        font-size: 28px;
    }

    .dashboard-header {
        padding: 25px;
    }

    .kpi-value {
        font-size: 24px;
    }

    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
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

    # Convert date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # Convert numeric columns
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        ).fillna(0)

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

    # Validate required columns
    if "Date" not in df.columns:
        st.error("Date column not found in dataset.")
        st.stop()

    if "Amount" not in df.columns:
        st.error("Amount column not found in dataset.")
        st.stop()

    # Remove invalid dates
    df = df.dropna(subset=["Date"])

    return df


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">🛒 Sales Intelligence</div>
    <div class="sidebar-subtitle">
        Interactive Amazon sales analytics
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="filter-heading">Filters</div>',
    unsafe_allow_html=True
)


# Category filter
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


# Size filter
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


# Courier status filter
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


# Customer type filter
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


# Date filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

st.sidebar.markdown(
    '<div class="filter-heading">Date Range</div>',
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


# Date filtering
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        &
        (filtered_df["Date"] <= end_date)
    ]


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">

        <div class="dashboard-title">
            Amazon Sales Intelligence
        </div>

        <div class="dashboard-subtitle">
            Interactive analytics dashboard for understanding
            revenue, products, customers, and operations.
        </div>

        <div class="header-badge">
            📈 Data-Driven Sales Analytics
        </div>

    </div>
    """,
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

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                💰 Total Revenue
            </div>

            <div class="kpi-value">
                ₹{total_revenue / 10000000:.2f} Cr
            </div>

            <div class="kpi-description">
                Total sales generated
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                📦 Units Sold
            </div>

            <div class="kpi-value">
                {total_units / 1000:.1f}K
            </div>

            <div class="kpi-description">
                Products sold
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                🧾 Orders
            </div>

            <div class="kpi-value">
                {total_orders / 1000:.1f}K
            </div>

            <div class="kpi-description">
                Unique customer orders
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                🏷️ Products
            </div>

            <div class="kpi-value">
                {total_products / 1000:.1f}K
            </div>

            <div class="kpi-description">
                Unique SKUs
            </div>

        </div>
        """,
        unsafe_allow_html=True
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
        """
        <div class="section-title">
            Executive Overview
        </div>

        <div class="section-subtitle">
            Understand overall sales performance and category trends.
        </div>
        """,
        unsafe_allow_html=True
    )


    # Sales Trend
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
        height=420
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True,
        key="sales_trend_chart"
    )


    # Category + Size
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
                height=400
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
                height=400
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
        """
        <div class="section-title">
            Product Intelligence
        </div>

        <div class="section-subtitle">
            Identify the products and categories contributing most to sales.
        </div>
        """,
        unsafe_allow_html=True
    )


    # Top products by revenue
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
            height=500
        )

        st.plotly_chart(
            fig_top_products,
            use_container_width=True,
            key="top_products_revenue_chart"
        )


    # Units by category
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
            height=400
        )

        st.plotly_chart(
            fig_units_category,
            use_container_width=True,
            key="category_units_chart"
        )


    # Product performance table
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
            """
            <div class="section-title">
                Product Performance
            </div>

            <div class="section-subtitle">
                Top 20 products ranked by revenue.
            </div>
            """,
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
        """
        <div class="section-title">
            Operations & Customer Insights
        </div>

        <div class="section-subtitle">
            Analyze delivery status, customer segments, and geographic performance.
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # Courier Status
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
                height=400
            )

            st.plotly_chart(
                fig_courier,
                use_container_width=True,
                key="courier_status_chart"
            )


    # Customer Type
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
            height=400
        )

        st.plotly_chart(
            fig_customer,
            use_container_width=True,
            key="customer_type_chart"
        )


    # Top states
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
            height=500
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
        """
        <div class="section-title">
            Deep Analysis
        </div>

        <div class="section-subtitle">
            Explore trends, relationships, and statistical patterns in the data.
        </div>
        """,
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
        height=400
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
        key="monthly_revenue_chart"
    )


    # --------------------------------------------------------
    # QUANTITY VS AMOUNT
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
        height=450
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
        """
        <div class="section-title">
            Correlation Analysis
        </div>

        <div class="section-subtitle">
            Explore relationships between quantity, revenue, and B2B transactions.
        </div>
        """,
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


        # Convert B2B into numeric values
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


        # Convert numeric columns
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
                height=450
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

                Remember: correlation shows association, not causation.
                """
            )


            # Show correlation values
            st.markdown(
                """
                <div class="section-title">
                    Correlation Values
                </div>
                """,
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
        """
        <div class="section-title">
            Summary Statistics
        </div>

        <div class="section-subtitle">
            Key calculated metrics for the currently selected data.
        </div>
        """,
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
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    Average Order Value
                </div>

                <div class="insight-value">
                    ₹{avg_order_value:,.2f}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with stat2:

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    Revenue per Unit
                </div>

                <div class="insight-value">
                    ₹{revenue_per_unit:,.2f}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with stat3:

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    Records Analyzed
                </div>

                <div class="insight-value">
                    {len(filtered_df):,}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DYNAMIC BUSINESS INSIGHTS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        💡 Key Business Insights
    </div>

    <div class="section-subtitle">
        Automatically generated insights based on the selected filters.
    </div>
    """,
    unsafe_allow_html=True
)


insight1, insight2, insight3 = st.columns(3)


# Top category
with insight1:

    if "Category" in filtered_df.columns and not filtered_df.empty:

        top_category = (
            filtered_df
            .groupby("Category")["Amount"]
            .sum()
            .idxmax()
        )

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    🏆 Top Revenue Category
                </div>

                <div class="insight-value">
                    {top_category}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# Highest revenue product
with insight2:

    if "SKU" in filtered_df.columns and not filtered_df.empty:

        top_product = (
            filtered_df
            .groupby("SKU")["Amount"]
            .sum()
            .idxmax()
        )

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    ⭐ Highest Revenue Product
                </div>

                <div class="insight-value">
                    {top_product}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# Dominant customer segment
with insight3:

    if not filtered_df.empty:

        dominant_customer = (
            filtered_df["Customer Type"]
            .value_counts()
            .idxmax()
        )

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    👥 Dominant Customer Segment
                </div>

                <div class="insight-value">
                    {dominant_customer}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="dashboard-footer">

        <span class="footer-brand">
            Amazon Sales Intelligence
        </span>

        &nbsp;•&nbsp;

        Interactive Sales Analytics Dashboard

        <br><br>

        Built with Python, Pandas, Plotly & Streamlit

    </div>
    """,
    unsafe_allow_html=True
)