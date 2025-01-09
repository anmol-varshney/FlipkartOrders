import streamlit as st
import requests
import pandas as pd
import json

# Define API details
URL = "https://affiliate-api.flipkart.net/affiliate/report/orders/detail/json"
HEADERS = {
    "Fk-Affiliate-Id": "bh7162",
    "Fk-Affiliate-Token": "1e3be35caea748378cdd98e720ea06b3"
}

# Load credentials from JSON file
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

def login():
    st.title("🔑 Login Page")
    credentials = load_credentials()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")
    if login_clicked and username in credentials and credentials[username][0] == password:
        st.session_state["logged_in"] = True
        st.session_state["aff_ext_param1"] = credentials[username][1]
        st.rerun()
    elif login_clicked:
        st.error("Invalid username or password")

def logout():
    st.session_state.clear()
    st.rerun()

def main():
    st.set_page_config(page_title="Flipkart Affiliate Report", layout="wide")
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if not st.session_state["logged_in"]:
        login()
        return
    
    st.title("📊 Flipkart Affiliate Order Report")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("🔍 Filter Options")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        status = st.selectbox("Order Status", ["approved", "tentative", "cancelled"])
        fetch_button = st.button("Fetch Data")
        
        st.markdown("---")
        if st.button("Logout"):
            logout()
    
    if fetch_button:
        st.subheader("Results")
        
        aff_ext_param1 = st.session_state["aff_ext_param1"]
        
        # Initial fetch
        data = fetch_data(start_date, end_date, status, aff_ext_param1, 1)
        if data and 'paginationContext' in data:
            full_data = []
            total_pages = data['paginationContext']['totalPages']
            
            # Fetch all pages
            for i in range(total_pages):
                page_data = fetch_data(start_date, end_date, status, aff_ext_param1, i+1)
                if page_data and 'orderList' in page_data:
                    full_data.extend(page_data['orderList'])
            
            # Filter results
            req_data = [sample for sample in full_data if sample['affExtParam1'] == str(aff_ext_param1)]
            
            # Center align metric
            st.markdown("""
                <div style="display: flex; justify-content: center;">
                    <div style="text-align: center;">
                        <h2>📌 Total Samples</h2>
                        <h1>{}</h1>
                    </div>
                </div>
            """.format(len(req_data)), unsafe_allow_html=True)
            
            if req_data:
                df = pd.DataFrame(req_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No data found for the given criteria.")

if __name__ == "__main__":
    main()
