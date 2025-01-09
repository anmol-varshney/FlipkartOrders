import streamlit as st
import requests
import pandas as pd

# Define API details
URL = "https://affiliate-api.flipkart.net/affiliate/report/orders/detail/json"
HEADERS = {
    "Fk-Affiliate-Id": "bh7162",
    "Fk-Affiliate-Token": "1e3be35caea748378cdd98e720ea06b3"
}

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

def main():
    st.set_page_config(page_title="Flipkart Affiliate Report", layout="wide")
    st.title("📊 Flipkart Affiliate Order Report")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("🔍 Filter Options")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        status = st.selectbox("Order Status", ["approved", "tentative", "cancelled"])
        aff_ext_param1 = st.text_input("Affiliate External Param 1", "189")
        fetch_button = st.button("Fetch Data")
    
    if fetch_button:
        st.subheader("Results")
        
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
