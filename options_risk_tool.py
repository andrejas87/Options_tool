import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import uuid

# Streamlit app configuration
st.set_page_config(page_title="Options Trading Risk Management Tool", layout="wide")

# Helper function to calculate Greeks (simplified for demonstration)
def calculate_greeks(option_type, stock_price, strike_price, time_to_expiry, volatility, interest_rate):
    # Placeholder: Simplified Greeks calculations (in practice, use Black-Scholes or binomial models)
    delta = 0.5 if option_type == "Call" else -0.5
    gamma = 0.1
    theta = -0.01 * time_to_expiry
    vega = 0.2 * volatility
    rho = 0.05 * interest_rate
    return {"Delta": delta, "Gamma": gamma, "Theta": theta, "Vega": vega, "Rho": rho}

# Helper function to calculate risk-to-reward ratio
def calculate_risk_reward(entry_price, target_price, stop_loss_price):
    if entry_price == 0 or (target_price - entry_price) == 0:
        return 0
    risk = entry_price - stop_loss_price
    reward = target_price - entry_price
    return reward / risk if risk > 0 else float('inf')

# Main app
st.title("Options Trading Risk Management Tool")

# Sidebar for trade input
st.sidebar.header("Enter Trade Details")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
underlying_asset = st.sidebar.text_input("Underlying Asset", "SPY")
stock_price = st.sidebar.number_input("Current Stock Price ($)", min_value=0.0, value=100.0)
strike_price = st.sidebar.number_input("Strike Price ($)", min_value=0.0, value=100.0)
expiration_date = st.sidebar.date_input("Expiration Date", min_value=datetime.today())
time_to_expiry = (expiration_date - datetime.today().date()).days / 365.0
volatility = st.sidebar.number_input("Implied Volatility (%)", min_value=0.0, value=20.0) / 100
interest_rate = st.sidebar.number_input("Risk-Free Interest Rate (%)", min_value=0.0, value=5.0) / 100
entry_price = st.sidebar.number_input("Entry Price ($)", min_value=0.0, value=5.0)
contracts = st.sidebar.number_input("Number of Contracts", min_value=1, value=1)
stop_loss_price = st.sidebar.number_input("Stop-Loss Price ($)", min_value=0.0, value=3.0)
take_profit_price = st.sidebar.number_input("Take-Profit Price ($)", min_value=0.0, value=8.0)

# Risk tolerance and position sizing
st.sidebar.header("Risk Management Settings")
total_capital = st.sidebar.number_input("Total Trading Capital ($)", min_value=0.0, value=10000.0)
risk_tolerance = st.sidebar.slider("Risk Tolerance per Trade (%)", 0.0, 10.0, 1.0) / 100
asset_class = st.sidebar.selectbox("Asset Class", ["Stocks", "ETFs", "Commodities"])
geographic_region = st.sidebar.selectbox("Geographic Region", ["US", "Europe", "Asia", "Global"])

# Calculate position size
max_risk = total_capital * risk_tolerance
position_size = min(max_risk / (entry_price - stop_loss_price), contracts * 100 * entry_price)

# Calculate Greeks and risk metrics
greeks = calculate_greeks(option_type, stock_price, strike_price, time_to_expiry, volatility, interest_rate)
risk_reward_ratio = calculate_risk_reward(entry_price, take_profit_price, stop_loss_price)

# Main content
st.header("Risk Analysis")

# Display Greeks
st.subheader("Option Greeks")
greeks_df = pd.DataFrame([greeks])
st.table(greeks_df)

# Display Risk Metrics
st.subheader("Risk Metrics")
st.write(f"**Risk-to-Reward Ratio**: {risk_reward_ratio:.2f}")
st.write(f"**Position Size (Contracts)**: {position_size / (100 * entry_price):.2f}")
st.write(f"**Max Loss per Trade**: ${max_risk:.2f}")
st.write(f"**Time to Expiry**: {time_to_expiry:.2f} years")
st.write(f"**Market Risk**: Monitor economic data and news for {underlying_asset}.")
st.write(f"**Liquidity Risk**: Ensure {underlying_asset} options are liquid.")
st.write(f"**Volatility Risk**: Volatility at {volatility*100:.2f}% may impact premiums.")
st.write(f"**Time Decay Risk**: Theta indicates daily loss of ${abs(greeks['Theta']*100):.2f} per contract.")

# Portfolio Diversification Visualization
st.subheader("Portfolio Diversification")
portfolio_data = {
    "Asset": [underlying_asset, "Other Asset 1", "Other Asset 2"],
    "Allocation": [position_size, total_capital * 0.3, total_capital * 0.2],
    "Asset Class": [asset_class, "Stocks", "Commodities"],
    "Region": [geographic_region, "US", "Global"]
}
portfolio_df = pd.DataFrame(portfolio_data)
fig = px.pie(portfolio_df, values="Allocation", names="Asset", title="Portfolio Allocation")
st.plotly_chart(fig)

# Risk Management Tips
st.subheader("Risk Management Tips")
st.markdown("""
- **Diversify**: Spread risk across different strikes, expirations, and asset classes.
- **Position Sizing**: Limit risk to {risk_tolerance*100:.1f}% of capital per trade.
- **Stop-Loss/Take-Profit**: Set at ${stop_loss_price:.2f} and ${take_profit_price:.2f} to manage exits.
- **Monitor Greeks**: Use Delta, Gamma, Theta, Vega, and Rho to adjust strategies.
- **Stay Informed**: Regularly review market news and backtest strategies.
""")

# Save trade to session state for history
if "trade_history" not in st.session_state:
    st.session_state.trade_history = []
if st.button("Save Trade"):
    trade = {
        "Trade ID": str(uuid.uuid4()),
        "Asset": underlying_asset,
        "Option Type": option_type,
        "Strike Price": strike_price,
        "Entry Price": entry_price,
        "Position Size": position_size,
        "Risk-to-Reward": risk_reward_ratio,
        "Date": datetime.now()
    }
    st.session_state.trade_history.append(trade)
    st.success("Trade saved!")

# Display trade history
st.subheader("Trade History")
if st.session_state.trade_history:
    history_df = pd.DataFrame(st.session_state.trade_history)
    st.table(history_df)

# Continuous Learning Section
st.subheader("Learning Resources")
st.markdown("""
- **Books**: "Options, Futures, and Other Derivatives" by John C. Hull
- **Courses**: Check Coursera or Udemy for options trading courses
- **Communities**: Join trading forums on Reddit or X for insights
- **Backtesting**: Use historical data to test strategies before trading
""")