import requests
import json
from urllib.parse import quote
from datetime import datetime
import streamlit as st

#will change later.
#Required: the dataset found.
CITY_LIVING_COSTS = {
    "London": 2100,
    "New York": 2500,
    "Berlin": 1800,
    "Tokyo": 1900,
    "Toronto": 2000,
    "Default": 2000  # fallback
}


#defi protocols from defillama.
def get_all_protocols():
    url = "https://api.llama.fi/protocols"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching protocols: {e}")
        return None


#gets prices for multiple coins at different timestamps
def get_batch_historical_prices(coins_dict, search_width):
    base_url = "https://coins.llama.fi/batchHistorical"
    coins_json = json.dumps(coins_dict)
    encoded_coins = quote(coins_json)
    url = f"{base_url}?coins={encoded_coins}&searchWidth={search_width}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Batch price error: {e}")
        return None


#current TVL for specific protocol
def get_current_tvl(protocol_name):
    url = f"https://api.llama.fi/tvl/{protocol_name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()


        if isinstance(data, dict) and 'tvl' in data:
            return data['tvl']
        else:

            return 0

    except requests.exceptions.RequestException as e:
        print(f"TVL fetch error: {e}")
        return 0

def get_historical_tvl(protocol_name):
    """
    Fetch historical TVL data for a specific protocol.
    """
    url = f"https://api.llama.fi/v2/historicalChainTvl"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Print the data for debugging (temporary)
        print("Historical TVL Data:", data)

        # Ensure that data is a list and contains relevant information
        if isinstance(data, list):
            # Iterate through the list and check if the protocol name is found in any 'name' field
            for chain_data in data:
                # Adjust according to the actual field in the response data
                print("Chain Data:", chain_data)  # Debugging output
                if 'name' in chain_data and protocol_name.lower() in chain_data['name'].lower():
                    return chain_data.get('tvl', 0)  # Return the TVL for the matched protocol
        return 0  # Return 0 if protocol name is not found or no data exists

    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical TVL: {e}")
        return 0



#roi calculation based on historical and current tvl.
def calculate_roi(initial_investment, current_tvl, historical_tvl):
    # Here we assume that the difference between the current TVL and the historical TVL is the ROI.
    if historical_tvl == 0:
        return 0
    roi = ((current_tvl - historical_tvl) / historical_tvl) * 100
    return roi


#top defi protocols.
def get_top_defi_protocols():
    protocols = get_all_protocols()
    if not protocols:
        return []
    return [protocol for protocol in protocols if (protocol.get("tvl") or 0) > 10_000_000]


#recommend defi investments based on monthly investment.
def recommend_defi_investments(monthly_investment):
    protocols = get_top_defi_protocols()
    if not protocols:
        return ["Ethereum (ETH)", "Bitcoin (BTC)", "Uniswap (UNI)"]  # Default if no protocols found
    # Sort protocols by TVL (Total Value Locked) descending
    protocols_sorted = sorted(protocols, key=lambda x: x.get("tvl", 0), reverse=True)
    recommendations = []
    for protocol in protocols_sorted[:3]:  # Top 3 protocols
        name = protocol.get("name", "Unknown Protocol")
        tvl = protocol.get("tvl", 0)
        recommendations.append({
            'name': name,
            'tvl': tvl
        })
    return recommendations


def main():
    st.title("Investment Recommendation Assistant")

    # User inputs
    city = st.text_input("Enter your city")
    salary = st.number_input("Enter your monthly salary (GBP)", min_value=0)
    months = st.number_input("Investment duration (months)", min_value=1)

    if st.button("Calculate and Recommend"):
        # How much the user can invest
        living_cost = CITY_LIVING_COSTS.get(city.title(), CITY_LIVING_COSTS["Default"])
        investable = max(0, salary - living_cost)
        total_invest = investable * months

        # Avoid unbound variable error.
        roi = 0

        # Display investment details
        st.success(f"You can invest approximately £{investable} per month.")
        st.info(f"Over {months} months, you can invest a total of £{total_invest}.")

        # Suggested investments (same as before)
        st.subheader("Suggested DeFi Investments:")
        for rec in recommend_defi_investments(investable):
            st.write(f"- {rec['name']} (TVL: £{rec['tvl']:,.2f})")

            # Fetch historical TVL and current TVL for each recommended protocol
            protocol_name = rec['name'].lower()
            current_tvl = get_current_tvl(protocol_name)

            # Fetch historical TVL for the protocol
            historical_tvl = get_historical_tvl(protocol_name)

            # Calculate ROI for this protocol
            protocol_roi = calculate_roi(total_invest, current_tvl, historical_tvl)
            st.write(f"Estimated ROI for {rec['name']}: {protocol_roi:.2f}%")

        # Display ROI
        st.subheader("Estimated Return on Investment (ROI):")
        st.write(f"Your estimated ROI is {roi}% based on your monthly investment.")



if __name__ == "__main__":
    if 'history' not in st.session_state:
        st.session_state.history = []
    main()
