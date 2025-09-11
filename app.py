import streamlit as st
import requests
import pandas as pd
import json
from datetime import date, datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# ===================== CONFIG =====================
URL = "https://affiliate-api.flipkart.net/affiliate/report/orders/detail/json"
HEADERS = {
    "Fk-Affiliate-Id": st.secrets["FLIPKART_AFFILIATE_ID"],
    "Fk-Affiliate-Token": st.secrets["FLIPKART_AFFILIATE_TOKEN"]
}

# Affiliate Link Generator Settings
AFFILIATE_ID = "bh7162"
KEEP_PARAMS = [
    "marketplace", "iid", "ppt", "lid", "srno", "pid",
    "store", "ssid", "otracker1", "ppn", "spotlightTagId"
]
ORDER = [
    "marketplace", "iid", "ppt", "lid", "srno",
    "pid", "affid", "store", "ssid", "otracker1",
    "ppn", "spotlightTagId"
]

# ===================== HELPERS =====================
def load_credentials():
    with open("credentials.json", "r") as file:
        return json.load(file)

def fetch_data(start_date, end_date, status, aff_ext_param1, page_number):
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "status": status,
        "offset": 0,
        "pageNumber": page_number,
        "affExtParam1": aff_ext_param1
    }
    response = requests.get(URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

def generate_affiliate_link(original_url: str) -> str:
    parsed = urlparse(original_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    query_params = parse_qs(parsed.query)

    filtered = {k: v for k, v in query_params.items() if k in KEEP_PARAMS}
    filtered["affid"] = [AFFILIATE_ID]

    ordered_query = []
    for key in ORDER:
        if key in filtered:
            ordered_query.append((key, filtered[key][0]))

    new_query = urlencode(ordered_query, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", new_query, ""))

# ===================== AUTH =====================
def login():
    col1, col2, col3 = st.columns([1, 2, 1])  
    with col2:  
        st.image("https://github.com/anmol-varshney/FlipkartOrders/blob/main/company_logo.png?raw=true")

    st.write(" ")
    st.title("🔑 Login Page")
    
    credentials = load_credentials()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked and username in credentials and credentials[username][0] == password:
        st.session_state["logged_in"] = True
        st.session_state["aff_ext_param1"] = credentials[username][1]
        st.session_state["username"] = username
        st.rerun()
    elif login_clicked:
        st.error("Invalid username or password")
        
def logout():
    st.session_state.clear()
    st.rerun()

# ===================== MAIN =====================
def main():
    st.set_page_config(
        page_title="AdgamaDigital", 
        layout="centered", 
        page_icon="https://github.com/anmol-varshney/FlipkartOrders/blob/main/company_logo.png?raw=true"
    )
    
    # CSS
    st.markdown(
    """
        <style>
        .main { background-color: #e3f2fd; color: #0d47a1; font-family: 'Roboto', sans-serif; }
        .title-container { background-color: #0d47a1; color: white; padding: 2em; text-align: center; border-radius: 8px; margin-bottom: 2em; }
        .title-container h1 { color: white; }
        header { background-color: white; color: #0d47a1; padding: 10px; font-size: 1.2em; font-weight: bold; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); }
        .nav-logo { display: flex; justify-content: center; }
        .logged-in-info { background-color: #ffffff; color: #0d47a1; border: 2px solid #0288d1; border-radius: 8px; padding: 0.8em; margin-bottom: 1em; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); font-size: 1em; font-weight: bold; display: flex; align-items: center; justify-content: center; }
        .stSidebar { background-color: #bbdefb; color: #0d47a1; border-right: 3px solid #039be5; display: flex; flex-direction: column; justify-content: space-between; height: 100vh; }
        </style>
    """,
    unsafe_allow_html=True
    )

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if not st.session_state["logged_in"]:
        login()
        return
    
    # Title
    st.markdown(
        """
        <div class="title-container">
            <h1>📊 Flipkart Affiliate Order Report</h1>
            <p><b>Welcome to the Flipkart Affiliate Order Dashboard!<br>
            Track your affiliate orders and their status with ease. Use the filters below to customize the data you wish to view.</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.markdown(
            """
            <div class="nav-logo">
                <img src="https://github.com/anmol-varshney/FlipkartOrders/blob/main/company_logo.png?raw=true" width="100"/>
            </div>
            """,
            unsafe_allow_html=True
        )
        if "username" in st.session_state:
            st.markdown(
                f"""
                <div class="logged-in-info">
                    Logged in as:<span> {st.session_state['username']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.header("🔍 Filter Options")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        status = st.selectbox("Order Status", ["approved", "tentative", "cancelled"])
        
        fetch_button = st.button("Fetch Data", key="fetch_data_button", use_container_width=True)
        
        if st.button("Logout", key="logout_button", use_container_width=True):
            logout()
    
    if fetch_button:
        aff_ext_param1 = st.session_state["aff_ext_param1"]
        data = fetch_data(start_date, end_date, status, aff_ext_param1, 1)
        if data and 'paginationContext' in data:
            full_data = []
            total_pages = data['paginationContext']['totalPages']
            for i in range(total_pages):
                page_data = fetch_data(start_date, end_date, status, aff_ext_param1, i+1)
                if page_data and 'orderList' in page_data:
                    full_data.extend(page_data['orderList'])
            req_data = []
            for sample in full_data:
                if str(sample['affExtParam1']).startswith(str(aff_ext_param1)):
                    sample['sales'] = sample['sales']['amount']
                    sample['tentativeCommission'] = sample['tentativeCommission']['amount']
                    sample.pop("commissionRate", None)
                    sample.pop("customerType", None)
                    sample.pop("price", None)
                    sample.pop("quantity", None)
                    req_data.append(sample)

            st.markdown("<div style='text-align: center;'><h2>📌 Order Report 📌</h2></div>", unsafe_allow_html=True)
            if req_data:
                df = pd.DataFrame(req_data).reset_index(drop=True)
                df.index = df.index + 1  
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No data found for the given criteria.")

    # ===================== AFFILIATE LINK GENERATOR =====================
    st.markdown(
       f"""
        <div style="text-align: center; margin-top: 30px;">
            <h2>🔗 Flipkart Affiliate Link Generator</h2>
            <p><b>Paste a product link below and generate your affiliate link instantly.</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    original_url = st.text_input("Enter Flipkart Product URL:")
    if st.button("Generate Affiliate Link"):
        if original_url.strip():
            affiliate_link = generate_affiliate_link(original_url)
            st.success("✅ Affiliate Link Generated")
            st.code(affiliate_link, language="text")
            st.markdown(
                f"""
                <button class="stButton" onclick="navigator.clipboard.writeText('{affiliate_link}')">
                    📋 Copy Link
                </button>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Please enter a valid Flipkart URL.")

# ===================== RUN =====================
if __name__ == "__main__":
    main()
