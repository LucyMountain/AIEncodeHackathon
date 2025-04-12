import requests
import json
from urllib.parse import quote
from datetime import datetime, timedelta
import streamlit as st
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

CITY_LIVING_COSTS = {
    "London": 2100,
    "New York": 2500,
    "Berlin": 1800,
    "Tokyo": 1900,
    "Toronto": 2000,
    "Default": 2000
}

def get_all_protocols():
    url = "https://api.llama.fi/protocols"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching protocols: {e}") # was outputting error message to terminal and not streamlit
        logger.error(f"Protocol fetch failed: {e}", exc_info = True) #loging the error - easier to handle errors/debug
        return []

def get_current_tvl(protocol_slug):
    url = f"https://api.llama.fi/tvl/{protocol_slug}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            return data.get('tvl', 0)
        elif isinstance(data, (int, float)):
            return data
        else:
            return 0
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching current TVL: {e}")# was outputting error message to terminal and not streamlit
        logger.error(f"Current TVL fetch error: {e}", exc_info = True) #loging the error - easier to handle errors/debug
        return 0


#I am looking at actual historical TVL data from the previous 30 days.
#Also handles more than one type of value formats.

def get_historical_tvl(protocol_slug, days_ago=30):
    url = f"https://api.llama.fi/protocol/{protocol_slug}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        tvl_data = data.get('tvl', [])
        if not tvl_data:
            return 0
        target_date = datetime.utcnow() - timedelta(days=days_ago) #(?)
        closest_entry = min(
            tvl_data,
            key=lambda x: abs(datetime.utcfromtimestamp(x['date']) - target_date)
        )
        return closest_entry.get('totalLiquidityUSD', 0)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching historical TVL: {e}")# was outputting error message to terminal and not streamlit
        logger.error(f"Historical TVL fetch error: {e}", exc_info = True)#loging the error - easier to handle errors/debug
        return 0

def calculate_roi(current_tvl, historical_tvl):
    if historical_tvl == 0:
        return 0
    roi = ((current_tvl - historical_tvl) / historical_tvl) * 100 #checks how much the TVL data has changed over the past 30 days (percentage)
    return roi

def get_top_defi_protocols():
    protocols = get_all_protocols()
    return [p for p in protocols if isinstance(p.get("tvl"), (int, float)) and p["tvl"] > 10_000_000]


def recommend_defi_investments(monthly_investment):
    protocols = get_top_defi_protocols()
    protocols_sorted = sorted(protocols, key=lambda x: x.get("tvl", 0), reverse=True)
    recommendations = []
    for protocol in protocols_sorted[:5]:
        name = protocol.get("name", "Unknown")
        slug = protocol.get("slug", name.lower().replace(" ", ""))
        tvl = protocol.get("tvl", 0)
        recommendations.append({
            'name': name,
            'slug': slug,
            'tvl': tvl
        })
    return recommendations

def main():
    st.title("DeFi Investment Recommendation Assistant")

    city = st.text_input("Enter your city")
    salary = st.number_input("Enter your monthly salary (GBP)", min_value=0)
    months = st.number_input("Investment duration (months)", min_value=1)

    if st.button("Calculate and Recommend"):
        living_cost = CITY_LIVING_COSTS.get(city.title(), CITY_LIVING_COSTS["Default"])
        investable = max(0, salary - living_cost)
        total_invest = investable * months

        st.success(f"You can invest approximately £{investable} per month.")
        st.info(f"Over {months} months, you can invest a total of £{total_invest}.")

        st.subheader("Suggested DeFi Investments:")
        for rec in recommend_defi_investments(investable):
            st.write(f"- {rec['name']} (TVL: £{rec['tvl']:,.2f})")
            current_tvl = get_current_tvl(rec['slug'])
            historical_tvl = get_historical_tvl(rec['slug'])
            roi = calculate_roi(current_tvl, historical_tvl)
            st.write(f"Estimated ROI for {rec['name']}: {roi:.2f}%")

        st.subheader("Investment Types Explained")
        st.markdown("""
        **Lending Platforms** (e.g., Aave, Compound)
        - Earn interest by supplying assets.
        - Lower risk, lower return.

        **Decentralized Exchanges (DEXs)** (e.g., Uniswap)
        - Earn fees by providing liquidity.
        - Watch for impermanent loss.

        **Yield Farming / Liquidity Mining**
        - Potentially high returns.
        - Requires active management and risk.

        **Stablecoin Investments** (e.g., DAI, USDC)
        - Lower volatility.
        - Less upside, but good for risk-averse strategies.
        """)

if __name__ == "__main__":
    if 'history' not in st.session_state:
        st.session_state.history = []
    main()
