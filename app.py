# ============================================================
# AMAZON SALES INTELLIGENCE DASHBOARD
# Streamlit + Pandas + Plotly
# ============================================================

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
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F7F8FA;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #172033;
}


/* Main title */

.main-title {
    font-size: 42px;
    font-weight: 750;
    color: #172033;
    margin-bottom: 4px;
    letter-spacing: -1px;
}

.subtitle {
    color: #6B7280;
    font-size: 16px;
    margin-bottom: 25px;
}


/* KPI Cards */

.kpi-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 20px 22px;
    min-height: 130px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.kpi-label {
    color: #6B7280;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-value {
    color: #172033;
    font-size: 29px;
    font-weight: 750;
    margin-top: 8px;
}

.kpi-description {
    color: #9CA3AF;
    font-size: 12px;
    margin-top: 5px;
}


/* Section headings */

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #172033;
    margin-top: 25px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #6B7280;
    font-size: 14px;
    margin-bottom: 15px;
}


/* Insight Cards */

.insight-card {
    background: white;
    border-left: 4px solid #FF9900;
    border-radius: 10px;
    padding: 15px 18px;
    margin-bottom: 10px;
    border-top: 1px solid #E5E7EB;
    border-right: 1px solid #E5E7EB;
    border-bottom: 1px solid #E5E7EB;
}

.insight-title {
    font-weight: 700;
    color: #172033;
    font-size: 14px;
}

.insight-text {
    color: #4B5563;
    font-size: 13px;
    margin-top: 4px;
}


/* Info Box */

.info-box {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 18px;
    margin-top: 10px;
}


/* Footer */

.footer {
    text-align: center;
    color: #9CA3AF;
    font-size: 12px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #E5E7EB;
}


/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_name = "Amazon Sale Report.csv"

    df = pd.read_csv(file_name)

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # --------------------------------------------------------
    # AMOUNT
    # --------------------------------------------------------

    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        ).fillna(0)

    # --------------------------------------------------------
    # QUANTITY
    # --------------------------------------------------------

    if "Qty" in df.columns:
        df["Qty"] = pd.to_numeric(
            df["Qty"],
            errors="coerce"
        ).fillna(0)

    # --------------------------------------------------------
    # ORDER ID
    # --------------------------------------------------------

    if "Order ID" not in df.columns:

        possible_order_columns = [
            "OrderID",
            "order_id",
            "Order Id"
        ]

        for col in possible_order_columns:
            if col in df.columns:
                df["Order ID"] = df[col]
                break

    # --------------------------------------------------------
    # SKU
    # --------------------------------------------------------

    if "SKU" not in df.columns:

        possible_sku_columns = [
            "Sku",
            "sku",
            "Product ID",
            "Product_ID"
        ]

        for col in possible_sku_columns:
            if col in df.columns:
                df["SKU"] = df[col]
                break

    # --------------------------------------------------------
    # CUSTOMER TYPE
    # --------------------------------------------------------

    # If Customer Type doesn't exist, create a reasonable
    # fallback using B2B information if available.

    if "Customer Type" not in df.columns:

        if "B2B" in df.columns:

            df["Customer Type"] = np.where(
                df["B2B"].astype(str).str.lower().isin(
                    ["true", "1", "yes"]
                ),
                "Business",
                "Individual"
            )

        else:
            df["Customer Type"] = "All Customers"

    return df


try:
    df = load_data()

except FileNotFoundError:

    st.error(
        "Amazon Sale Report.csv was not found. "
        "Make sure the CSV file is in the same folder as app.py."
    )

    st.stop()


# ============================================================
# DATA VALIDATION
# ============================================================

if "Date" not in df.columns:
    st.error("The dataset must contain a 'Date' column.")
    st.stop()

if "Amount" not in df.columns:
    st.error("The dataset must contain an 'Amount' column.")
    st.stop()


# Remove rows without dates
df = df.dropna(subset=["Date"]).copy()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="color:#172033;">
        🔎 Filters
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    if "Category" in df.columns:

        categories = sorted(
            df["Category"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Category",
            ["All"] + categories,
            key="category_filter"
        )

    else:
        selected_category = "All"


    # --------------------------------------------------------
    # SIZE
    # --------------------------------------------------------

    if "Size" in df.columns:

        sizes = sorted(
            df["Size"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_size = st.selectbox(
            "Size",
            ["All"] + sizes,
            key="size_filter"
        )

    else:
        selected_size = "All"


    # --------------------------------------------------------
    # COURIER STATUS
    # --------------------------------------------------------

    if "Courier Status" in df.columns:

        courier_statuses = sorted(
            df["Courier Status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_courier = st.selectbox(
            "Courier Status",
            ["All"] + courier_statuses,
            key="courier_filter"
        )

    else:
        selected_courier = "All"


    # --------------------------------------------------------
    # CUSTOMER TYPE
    # --------------------------------------------------------

    customer_types = sorted(
        df["Customer Type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_customer = st.selectbox(
        "Customer Type",
        ["All"] + customer_types,
        key="customer_filter"
    )


    # ========================================================
    # FIXED DATE RANGE FILTER
    # ========================================================

    # IMPORTANT:
    # The date picker is restricted to dates actually present
    # in the dataset.
    #
    # This prevents the problem where Streamlit allows
    # 2026 dates even though the dataset is from 2022.

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    selected_dates = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range_filter"
    )


    # --------------------------------------------------------
    # SAFELY PROCESS DATE SELECTION
    # --------------------------------------------------------

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

        start_date = pd.Timestamp(selected_dates[0])
        end_date = pd.Timestamp(selected_dates[1])

    else:

        start_date = pd.Timestamp(min_date)
        end_date = pd.Timestamp(max_date)


    st.markdown("---")

    st.caption(
        "Filters update the complete dashboard dynamically."
    )

    st.caption(
        f"Available data: {min_date} → {max_date}"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


# Category
if selected_category != "All" and "Category" in filtered_df.columns:

    filtered_df = filtered_df[
        filtered_df["Category"].astype(str) == selected_category
    ]


# Size
if selected_size != "All" and "Size" in filtered_df.columns:

    filtered_df = filtered_df[
        filtered_df["Size"].astype(str) == selected_size
    ]


# Courier Status
if selected_courier != "All" and "Courier Status" in filtered_df.columns:

    filtered_df = filtered_df[
        filtered_df["Courier Status"].astype(str)
        == selected_courier
    ]


# Customer Type
if selected_customer != "All":

    filtered_df = filtered_df[
        filtered_df["Customer Type"].astype(str)
        == selected_customer
    ]


# Date
filtered_df = filtered_df[
    (filtered_df["Date"] >= start_date)
    &
    (filtered_df["Date"] <= end_date)
]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🛒 Amazon Sales Intelligence
    </div>

    <div class="subtitle">
        Executive analytics dashboard for sales, products and operations
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["Amount"].sum()

total_units = (
    filtered_df["Qty"].sum()
    if "Qty" in filtered_df.columns
    else 0
)

if "Order ID" in filtered_df.columns:

    total_orders = filtered_df["Order ID"].nunique()

else:

    total_orders = len(filtered_df)


if "SKU" in filtered_df.columns:

    total_products = filtered_df["SKU"].nunique()

else:

    total_products = len(filtered_df)


# ============================================================
# FORMAT FUNCTIONS
# ============================================================

def format_currency(value):

    if value >= 10000000:
        return f"₹{value / 10000000:.2f}Cr"

    elif value >= 100000:
        return f"₹{value / 100000:.1f}L"

    elif value >= 1000:
        return f"₹{value / 1000:.1f}K"

    else:
        return f"₹{value:,.0f}"


def format_number(value):

    if value >= 1000000:
        return f"{value / 1000000:.1f}M"

    elif value >= 1000:
        return f"{value / 1000:.1f}K"

    else:
        return f"{value:,.0f}"


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">

        <div class="kpi-label">
        Total Revenue
        </div>

        <div class="kpi-value">
        {format_currency(total_revenue)}
        </div>

        <div class="kpi-description">
        Sales generated
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
        Units Sold
        </div>

        <div class="kpi-value">
        {format_number(total_units)}
        </div>

        <div class="kpi-description">
        Total quantity
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
        Orders
        </div>

        <div class="kpi-value">
        {format_number(total_orders)}
        </div>

        <div class="kpi-description">
        Unique orders
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
        Products
        </div>

        <div class="kpi-value">
        {format_number(total_products)}
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
        Sales Performance
        </div>

        <div class="section-subtitle">
        Revenue movement across the selected period
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SALES TREND
    # --------------------------------------------------------

    if not filtered_df.empty:

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
            markers=True,
            title="Sales Performance"
        )

        fig_sales.update_layout(
            template="plotly_white",
            height=450,
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis_title="Date",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig_sales,
            use_container_width=True,
            key="executive_sales_trend"
        )

    else:

        st.warning(
            "No data available for the selected filters."
        )


    # --------------------------------------------------------
    # TWO CHARTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        if (
            "Category" in filtered_df.columns
            and not filtered_df.empty
        ):

            category_sales = (
                filtered_df
                .groupby("Category", as_index=False)["Amount"]
                .sum()
                .sort_values("Amount", ascending=False)
                .head(10)
            )

            fig_category = px.bar(
                category_sales,
                x="Amount",
                y="Category",
                orientation="h",
                title="Revenue by Category"
            )

            fig_category.update_layout(
                template="plotly_white",
                height=420,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True,
                key="executive_category_revenue"
            )


    with col2:

        if (
            "Size" in filtered_df.columns
            and not filtered_df.empty
        ):

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
                title="Revenue by Size"
            )

            fig_size.update_layout(
                template="plotly_white",
                height=420,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_size,
                use_container_width=True,
                key="executive_size_revenue"
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
        Identify high-performing products and categories
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    with col1:

        if (
            "SKU" in filtered_df.columns
            and not filtered_df.empty
        ):

            top_products = (
                filtered_df
                .groupby("SKU", as_index=False)["Amount"]
                .sum()
                .sort_values(
                    "Amount",
                    ascending=False
                )
                .head(10)
            )

            fig_top_products = px.bar(
                top_products,
                x="Amount",
                y="SKU",
                orientation="h",
                title="Top 10 Products by Revenue"
            )

            fig_top_products.update_layout(
                template="plotly_white",
                height=450,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_top_products,
                use_container_width=True,
                key="product_top_revenue"
            )


    # --------------------------------------------------------
    # CATEGORY DISTRIBUTION
    # --------------------------------------------------------

    with col2:

        if (
            "Category" in filtered_df.columns
            and not filtered_df.empty
        ):

            category_quantity = (
                filtered_df
                .groupby("Category", as_index=False)["Qty"]
                .sum()
                .sort_values(
                    "Qty",
                    ascending=False
                )
                .head(10)
            )

            fig_category_qty = px.bar(
                category_quantity,
                x="Category",
                y="Qty",
                title="Units Sold by Category"
            )

            fig_category_qty.update_layout(
                template="plotly_white",
                height=450,
                margin=dict(l=20, r=20, t=60, b=20)
            )

            st.plotly_chart(
                fig_category_qty,
                use_container_width=True,
                key="product_category_quantity"
            )


    # --------------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------------

    if (
        "SKU" in filtered_df.columns
        and not filtered_df.empty
    ):

        product_summary = (
            filtered_df
            .groupby("SKU")
            .agg(
                Revenue=("Amount", "sum"),
                Units=("Qty", "sum")
            )
            .reset_index()
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(20)
        )

        st.markdown(
            """
            <div class="section-title">
            Product Performance
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            product_summary,
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
        Operations
        </div>

        <div class="section-subtitle">
        Monitor fulfilment and courier performance
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # COURIER STATUS
    # --------------------------------------------------------

    with col1:

        if (
            "Courier Status" in filtered_df.columns
            and not filtered_df.empty
        ):

            courier_data = (
                filtered_df[
                    "Courier Status"
                ]
                .value_counts()
                .reset_index()
            )

            courier_data.columns = [
                "Courier Status",
                "Orders"
            ]

            fig_courier = px.pie(
                courier_data,
                names="Courier Status",
                values="Orders",
                hole=0.55,
                title="Courier Status Distribution"
            )

            fig_courier.update_layout(
                template="plotly_white",
                height=430
            )

            st.plotly_chart(
                fig_courier,
                use_container_width=True,
                key="operations_courier_status"
            )


    # --------------------------------------------------------
    # CUSTOMER TYPE
    # --------------------------------------------------------

    with col2:

        if not filtered_df.empty:

            customer_data = (
                filtered_df[
                    "Customer Type"
                ]
                .value_counts()
                .reset_index()
            )

            customer_data.columns = [
                "Customer Type",
                "Orders"
            ]

            fig_customer = px.pie(
                customer_data,
                names="Customer Type",
                values="Orders",
                hole=0.55,
                title="Customer Type Distribution"
            )

            fig_customer.update_layout(
                template="plotly_white",
                height=430
            )

            st.plotly_chart(
                fig_customer,
                use_container_width=True,
                key="operations_customer_type"
            )


    # --------------------------------------------------------
    # STATE ANALYSIS
    # --------------------------------------------------------

    if (
        "ship-state" in filtered_df.columns
        and not filtered_df.empty
    ):

        state_sales = (
            filtered_df
            .groupby(
                "ship-state",
                as_index=False
            )["Amount"]
            .sum()
            .sort_values(
                "Amount",
                ascending=False
            )
            .head(15)
        )

        fig_state = px.bar(
            state_sales,
            x="Amount",
            y="ship-state",
            orientation="h",
            title="Top States by Revenue"
        )

        fig_state.update_layout(
            template="plotly_white",
            height=500
        )

        st.plotly_chart(
            fig_state,
            use_container_width=True,
            key="operations_state_revenue"
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
        Additional analytical insights from the selected data
        </div>
        """,
        unsafe_allow_html=True
    )


    if filtered_df.empty:

        st.warning(
            "No records available for the selected filters."
        )

    else:

        # ----------------------------------------------------
        # MONTHLY SALES
        # ----------------------------------------------------

        monthly_data = (
            filtered_df
            .assign(
                Month=filtered_df["Date"].dt.to_period("M").astype(str)
            )
            .groupby("Month", as_index=False)["Amount"]
            .sum()
        )

        fig_monthly = px.bar(
            monthly_data,
            x="Month",
            y="Amount",
            title="Monthly Revenue"
        )

        fig_monthly.update_layout(
            template="plotly_white",
            height=430
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True,
            key="deep_monthly_revenue"
        )


        # ----------------------------------------------------
        # REVENUE VS QUANTITY
        # ----------------------------------------------------

        if "Qty" in filtered_df.columns:

            analysis_df = (
                filtered_df
                .groupby("Date", as_index=False)
                .agg(
                    Revenue=("Amount", "sum"),
                    Quantity=("Qty", "sum")
                )
            )

            fig_scatter = px.scatter(
                analysis_df,
                x="Quantity",
                y="Revenue",
                title="Revenue vs Quantity",
                trendline=None
            )

            fig_scatter.update_layout(
                template="plotly_white",
                height=430
            )

            st.plotly_chart(
                fig_scatter,
                use_container_width=True,
                key="deep_revenue_quantity"
            )


        # ----------------------------------------------------
        # SUMMARY STATISTICS
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-title">
            Selected Dataset Summary
            </div>
            """,
            unsafe_allow_html=True
        )

        summary1, summary2, summary3 = st.columns(3)


        average_order_value = (
            total_revenue / total_orders
            if total_orders > 0
            else 0
        )

        revenue_per_unit = (
            total_revenue / total_units
            if total_units > 0
            else 0
        )

        with summary1:

            st.metric(
                "Average Order Value",
                format_currency(
                    average_order_value
                )
            )


        with summary2:

            st.metric(
                "Revenue per Unit",
                format_currency(
                    revenue_per_unit
                )
            )


        with summary3:

            st.metric(
                "Records Analyzed",
                f"{len(filtered_df):,}"
            )


# ============================================================
# DYNAMIC INSIGHTS
# ============================================================

st.markdown(
    """
    <div class="section-title">
    💡 Key Insights
    </div>

    <div class="section-subtitle">
    Automatically generated from the currently selected filters
    </div>
    """,
    unsafe_allow_html=True
)


if not filtered_df.empty:

    # --------------------------------------------------------
    # TOP CATEGORY
    # --------------------------------------------------------

    if "Category" in filtered_df.columns:

        category_summary = (
            filtered_df
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not category_summary.empty:

            top_category = category_summary.index[0]

            top_category_value = (
                category_summary.iloc[0]
            )

            st.markdown(
                f"""
                <div class="insight-card">

                <div class="insight-title">
                🏆 Top Revenue Category
                </div>

                <div class="insight-text">
                <b>{top_category}</b>
                generated
                <b>{format_currency(top_category_value)}</b>
                in revenue for the selected filters.
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # TOP PRODUCT
    # --------------------------------------------------------

    if "SKU" in filtered_df.columns:

        sku_summary = (
            filtered_df
            .groupby("SKU")["Amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not sku_summary.empty:

            top_sku = sku_summary.index[0]

            top_sku_value = sku_summary.iloc[0]

            st.markdown(
                f"""
                <div class="insight-card">

                <div class="insight-title">
                ⭐ Highest Revenue Product
                </div>

                <div class="insight-text">
                SKU <b>{top_sku}</b> generated
                <b>{format_currency(top_sku_value)}</b>
                in revenue within the selected data.
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # CUSTOMER INSIGHT
    # --------------------------------------------------------

    customer_summary = (
        filtered_df[
            "Customer Type"
        ]
        .value_counts()
    )

    if not customer_summary.empty:

        dominant_customer = (
            customer_summary.index[0]
        )

        dominant_customer_count = (
            customer_summary.iloc[0]
        )

        st.markdown(
            f"""
            <div class="insight-card">

            <div class="insight-title">
            👥 Dominant Customer Segment
            </div>

            <div class="insight-text">
            <b>{dominant_customer}</b>
            represents the largest customer segment
            with <b>{dominant_customer_count:,}</b>
            records in the selected data.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


else:

    st.info(
        "No insights available because no records match the selected filters."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    Amazon Sales Intelligence Dashboard
    &nbsp;•&nbsp;
    Built with Python, Pandas, Plotly and Streamlit

    </div>
    """,
    unsafe_allow_html=True
)