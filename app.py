# app.py
import streamlit as st
import pandas as pd
import json

# Page config
st.set_page_config(page_title="Stock Analyzer", layout="wide")

# Load stock notes
try:
    with open("stock_notes.json", "r") as f:
        stock_notes = json.load(f)
except Exception as e:
    stock_notes = {}
    st.error("Could not load stock_notes.json. Notes will not be displayed.")

# Load tickers
try:
    ticker_df = pd.read_csv("tickers.csv")
    ticker_options = ticker_df["ticker"] + " - " + ticker_df["name"]
    ticker_map = dict(zip(ticker_options, ticker_df["ticker"]))
except Exception as e:
    st.error("Error loading tickers.csv. Make sure it's in the root directory and formatted correctly.")
    ticker_options = []
    ticker_map = {}

# Sidebar
st.sidebar.title("📊 Stock Analysis Tool")

selected_option = st.sidebar.selectbox("Select Ticker", ticker_options)
ticker = ticker_map.get(selected_option, "AAPL")  # Fallback to AAPL

st.sidebar.markdown("---")
st.sidebar.markdown("Select a module:")

selected_module = st.sidebar.radio(
    "",
    ["📌 Overview", "📈 Fundamentals", "💰 Valuation", "⚖️ Rule of 40", "📉 Technicals", "🧠 Options Flow"]
)

# Main Page
st.title(f"Stock Dashboard for {ticker}")

if selected_module == "📌 Overview":
    st.subheader("Summary & Key Stats")

    notes = stock_notes.get(ticker.upper(), {})

    st.markdown("### 🏢 About the Company")
    st.write(notes.get("about", "No company description available."))

    st.markdown("### ⚙️ Factors Influencing the Stock")
    factors = notes.get("factors", [])
    if factors:
        for factor in factors:
            st.markdown(f"- {factor}")
    else:
        st.write("No factors available.")

    st.markdown("### 📅 Upcoming Events")
    events = notes.get("events", [])
    if events:
        for event in events:
            st.markdown(f"- {event}")
    else:
        st.write("No upcoming events listed.")

elif selected_module == "📈 Fundamentals":
    st.subheader("Fundamental Analysis")
    st.info("This will show revenue, earnings, margins, etc.")

elif selected_module == "💰 Valuation":
    st.subheader("Valuation Metrics")
    st.info("This will show PE, EV/EBITDA, Price/Sales, etc.")

elif selected_module == "⚖️ Rule of 40":
    st.subheader("Rule of 40 Score")
    st.info("Will calculate revenue growth + profit margin.")

elif selected_module == "📉 Technicals":
    st.subheader("Technical Analysis")
    st.info("Will show price chart, RSI, MACD, moving averages, etc.")

elif selected_module == "🧠 Options Flow":
    st.subheader("Options Flow & Unusual Activity")
    st.info("Will display options flow, unusual volume, and sentiment.")
