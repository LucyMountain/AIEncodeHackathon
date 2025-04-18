import requests
import json
import pandas as pd
from urllib.parse import quote
from datetime import datetime, timedelta

#default values.
DEFAULT_LIVING_COST = 1000  # fallback
CITY_LIVING_COSTS = {
    "London": 2100,
    "New York": 2500,
    "Berlin": 1800,
    "Tokyo": 1900,
    "Toronto": 2000,
}


def load_cost_of_living_data():
    try:
        df = pd.read_csv("Cost_Living_in_GBP.csv")
        return df
    except Exception as e:
        return pd.DataFrame()

#updates cost- dictionary.
def update_cost_of_living_dict():
    try:
        df = load_cost_of_living_data()
        new_record = {}
        for _, row in df.iterrows():
            city_name = row['city']
            cost_in_gbp = row['Living_cost_in_GBP']
            new_record[city_name] = cost_in_gbp
        return new_record.copy()
    except Exception as e:
        print(f"Failed to update city living costs: {e}")
        return CITY_LIVING_COSTS

#gets DeFi protocols.
def get_all_protocols():
    url = "https://api.llama.fi/protocols"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching protocols: {e}")
        return []

#current TVL
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
        print(f"Error fetching current TVL: {e}")
        return 0

#historical TVL
def get_historical_tvl(protocol_slug, days_ago=30):
    url = f"https://api.llama.fi/protocol/{protocol_slug}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        tvl_data = data.get('tvl', [])
        if not tvl_data:
            return 0
        target_date = datetime.utcnow() - timedelta(days=days_ago)
        closest_entry = min(
            tvl_data,
            key=lambda x: abs(datetime.utcfromtimestamp(x['date']) - target_date)
        )
        return closest_entry.get('totalLiquidityUSD', 0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical TVL: {e}")
        return 0


def calculate_roi(current_tvl, historical_tvl):
    if historical_tvl == 0:
        return 0
    roi = ((current_tvl - historical_tvl) / historical_tvl) * 100
    return roi

#specifically filters out the Solana-DeFi protocols from all of the other protocols.
def get_top_solana_protocols():
    all_protocols = get_all_protocols()
    return [
        p for p in all_protocols
        if p.get("chain", "").lower() == "solana"
        and isinstance(p.get("tvl"), (int, float)) and p["tvl"] > 10_000_000
    ]

#mapping for investment type, available options.
protocol_categories = {
    "Solend": "Lending Platforms",
    "Tulip Protocol": "Yield Farming",
    "Saber": "Stablecoins",
    "Raydium": "DEXs",
    "Mango Markets": "Lending Platforms",
    "Orca": "DEXs",
    "Jupiter Aggregator": "Auto Yield Aggregator",
    "Marinade Finance": "Staking",
    "Drift Protocol": "DEXs",
    "Port Finance": "Lending Platforms",
    "Francium": "Vault Strategy",
}


def generate_investment_summary(city, salary, months, risk_tolerance, preferred_types):

    living_cost = DEFAULT_LIVING_COST
    city_lower = city.lower()
    for key in CITY_LIVING_COSTS:
        if key.lower().startswith(city_lower + ",") or key.lower() == city_lower:
            living_cost = CITY_LIVING_COSTS[key]
            break

    monthly_invest = max(0, salary - living_cost)
    total_invest = monthly_invest * months

    protocols = get_top_solana_protocols()
    results = []

    def matches_risk(tvl):
        if risk_tolerance == "Low":
            return tvl > 100_000_000
        elif risk_tolerance == "Medium":
            return 20_000_000 < tvl <= 100_000_000
        elif risk_tolerance == "High":
            return tvl <= 20_000_000
        return True

    for protocol in protocols:
        name = protocol.get("name", "Unknown")
        slug = protocol.get("slug", name.lower().replace(" ", ""))
        tvl = protocol.get("tvl", 0)
        category = protocol_categories.get(name, "Other")

        if matches_risk(tvl) and (not preferred_types or category in preferred_types):
            current_tvl = get_current_tvl(slug)
            historical_tvl = get_historical_tvl(slug)
            roi = calculate_roi(current_tvl, historical_tvl)
            results.append([name, category, tvl, roi])

    return [[city, salary, months, risk_tolerance, preferred_types], monthly_invest, total_invest, results[:5]]


def start_init():
    CITY_LIVING_COSTS.update(update_cost_of_living_dict())
