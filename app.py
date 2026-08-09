import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Laptop Data Analysis Dashboard",
    page_icon="💻",
    layout="wide"
)

# -----------------------------
# Load dataset
# -----------------------------
from pathlib import Path

@st.cache_data
def load_data():
    return pd.read_csv("dataset/laptop_data.csv")
df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("💻 Laptop Data Analysis Dashboard")
st.write(
    "An interactive dashboard for exploring laptop prices, companies, "
    "laptop types, and hardware features."
)

# -----------------------------
# Dataset overview
# -----------------------------
st.header("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Laptops", len(df))
col2.metric("Total Columns", len(df.columns))

if "Company" in df.columns:
    col3.metric("Companies", df["Company"].nunique())

if "Price" in df.columns:
    col4.metric("Average Price", f"{df['Price'].mean():,.2f}")

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

filtered_df = df.copy()

if "Company" in df.columns:
    companies = sorted(df["Company"].dropna().unique())

    selected_company = st.sidebar.multiselect(
        "Select Company",
        companies
    )

    if selected_company:
        filtered_df = filtered_df[
            filtered_df["Company"].isin(selected_company)
        ]

if "TypeName" in df.columns:
    types = sorted(df["TypeName"].dropna().unique())

    selected_type = st.sidebar.multiselect(
        "Select Laptop Type",
        types
    )

    if selected_type:
        filtered_df = filtered_df[
            filtered_df["TypeName"].isin(selected_type)
        ]

# -----------------------------
# Filtered dataset information
# -----------------------------
st.subheader("Filtered Dataset")

st.write(f"Showing **{len(filtered_df)}** laptops.")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------
# Price distribution
# -----------------------------
if "Price" in filtered_df.columns:

    st.header("Price Analysis")

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.histplot(
        filtered_df["Price"].dropna(),
        kde=True,
        ax=ax
    )

    ax.set_title("Laptop Price Distribution")
    ax.set_xlabel("Price")
    ax.set_ylabel("Number of Laptops")

    st.pyplot(fig)

# -----------------------------
# Company distribution
# -----------------------------
if "Company" in filtered_df.columns:

    st.header("Company Distribution")

    company_counts = filtered_df["Company"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 5))

    company_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Number of Laptops by Company")
    ax.set_xlabel("Company")
    ax.set_ylabel("Number of Laptops")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# -----------------------------
# Average price by company
# -----------------------------
if "Company" in filtered_df.columns and "Price" in filtered_df.columns:

    st.header("Average Price by Company")

    avg_company_price = (
        filtered_df
        .groupby("Company")["Price"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    avg_company_price.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Average Laptop Price by Company")
    ax.set_xlabel("Company")
    ax.set_ylabel("Average Price")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# -----------------------------
# Laptop type distribution
# -----------------------------
if "TypeName" in filtered_df.columns:

    st.header("Laptop Type Distribution")

    type_counts = filtered_df["TypeName"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))

    type_counts.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

# -----------------------------
# Correlation heatmap
# -----------------------------
st.header("Correlation Analysis")

numeric_df = filtered_df.select_dtypes(include="number")

if numeric_df.shape[1] >= 2:

    correlation = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax
    )

    ax.set_title("Correlation Heatmap")

    st.pyplot(fig)

else:
    st.info("Not enough numerical columns for correlation analysis.")

# -----------------------------
# Summary statistics
# -----------------------------
st.header("Summary Statistics")

st.dataframe(
    filtered_df.describe(),
    use_container_width=True
)

# -----------------------------
# Key insights
# -----------------------------
st.header("Key Insights")

if "Price" in filtered_df.columns:

    st.write(
        f"• Average laptop price: **{filtered_df['Price'].mean():,.2f}**"
    )

    st.write(
        f"• Minimum laptop price: **{filtered_df['Price'].min():,.2f}**"
    )

    st.write(
        f"• Maximum laptop price: **{filtered_df['Price'].max():,.2f}**"
    )

if "Company" in filtered_df.columns:

    most_common_company = filtered_df["Company"].mode()[0]

    st.write(
        f"• Most represented company: **{most_common_company}**"
    )

if "TypeName" in filtered_df.columns:

    most_common_type = filtered_df["TypeName"].mode()[0]

    st.write(
        f"• Most common laptop type: **{most_common_type}**"
    )

st.success("Dashboard loaded successfully.")