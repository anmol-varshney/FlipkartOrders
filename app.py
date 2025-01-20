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

    # Centering the logo using Streamlit's columns
    col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns, middle column is wider
    
    with col2:  # Place image in the center column
        st.image("https://github.com/anmol-varshney/FlipkartOrders/blob/main/company_logo.png?raw=true")

    st.write(" ")
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

def main():
    st.set_page_config(page_title="AdgamaDigital", layout="centered", page_icon="https://github.com/anmol-varshney/FlipkartOrders/blob/main/company_logo.png?raw=true")
    
    # Inject custom CSS for a professional look and fixed buttons
    st.markdown(
    """
        <style>
    /* General Styles */
    .main {
        background-color: #e3f2fd; /* Light blue background */
        color: #0d47a1; /* Dark blue text */
        font-family: 'Roboto', sans-serif;
    }

    /* Title Container */
    .title-container {
        background-color: #0d47a1; /* Dark blue background */
        color: white; /* White text */
        padding: 2em; /* Padding around the title */
        text-align: center;
        border-radius: 8px; /* Rounded corners */
        margin-bottom: 2em;
    }

    /* Change title color to yellow */
    .title-container h1 {
        color: white; /* Yellow color for the title */
    }

    /* Navigation Bar */
    header {
        background-color: white; /* White background */
        color: #0d47a1; /* Dark blue text */
        padding: 10px;
        font-size: 1.2em;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Subtle shadow */
    }
    .nav-logo {
        display: flex;
        justify-content: center; /* Center the image */
    }

    /* Input Fields */
    .stTextInput, .stDateInput, .stSelectbox {
        background-color: #e3f2fd; /* Match main background */
        color: #0d47a1; /* Dark blue text */
        border: 1px solid #0288d1; /* Light blue border */
        border-radius: 5px;
        padding: 0.5em;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0d47a1; /* Green background for a professional feel */
        color: white; /* White text */
        border: none;
        padding: 0.6em 1.5em; /* Larger padding for a modern look */
        border-radius: 25px; /* Rounded corners for a polished design */
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
        transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transitions */
    }
    .stButton>button:hover {
        background-color: #bbdefb; /* Light blue background on hover */
        color: white; /* Text stays white */
        transform: scale(1.05); /* Slight zoom effect */
    }

    /* "Logged in as" Section */
    .logged-in-info {
        background-color: #ffffff; /* White background */
        color: #0d47a1; /* Dark blue text */
        border: 2px solid #0288d1; /* Light blue border */
        border-radius: 8px;
        padding: 0.8em;
        margin-bottom: 1em;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        font-size: 1em;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center; /* Center-align the text */
    }

    /* Sidebar Styles */
    .stSidebar {
        background-color: #bbdefb; /* Lighter blue sidebar */
        color: #0d47a1; /* Dark blue text */
        border-right: 3px solid #039be5; /* Blue border */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100vh;
    }

    .stSidebar .block-container {
        flex: 1;
    }

    /* Buttons at the bottom */
    .bottom-button {
        position: absolute;
        bottom: 10px;
        width: 100%;
        padding: 0.6em 1.5em;
        background-color: #4caf50; /* Green background for Fetch Data */
        color: white;
        border: none;
        border-radius: 25px;
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
        transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transitions */
    }
    .bottom-button:hover {
        background-color: #bbdefb; /* Light blue background on hover */
        color: white; /* Text stays white */
        transform: scale(1.05); /* Slight zoom effect */
    }

    /* Logout Button at the bottom */
    .logout-btn {
        position: absolute;
        bottom: 10px;
        width: 100%;
        padding: 0.6em 1.5em;
        background-color: #f44336; /* Red background */
        color: white;
        border: none;
        border-radius: 25px;
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Subtle shadow */
        transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transitions */
    }
    .logout-btn:hover {
        background-color: #d32f2f; /* Darker red on hover */
        transform: scale(1.05); /* Slight zoom effect */
    }
    </style>

    """,
    unsafe_allow_html=True
    )

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if not st.session_state["logged_in"]:
        login()
        return
    
    # Title Container
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

    # Sidebar for user inputs
    with st.sidebar:
        st.markdown(
            """
            <div class="nav-logo">
                <img src="https://github.com/anmol-varshney/FlipkartOrders/blob/main/company_logo.png?raw=true" width="100"/>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write(" ")
        st.write(" ")
        st.write(" ")
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
        
        # Fetch Data Button
        st.write(" ")
        st.write(" ")
        fetch_button = st.button("Fetch Data", key="fetch_data_button", use_container_width=True)
        
        # Logout Button
        if st.button("Logout", key="logout_button", use_container_width=True):
            logout()
    
    # Position the buttons at the bottom of the sidebar using custom CSS
    st.markdown("""
    <script>
        document.querySelector('.stSidebar').style.position = 'relative';
        document.querySelector('.stSidebar').style.display = 'flex';
        document.querySelector('.stSidebar').style.flexDirection = 'column';
        document.querySelector('.stSidebar').style.justifyContent = 'space-between';
    </script>
    """, unsafe_allow_html=True)

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
                if sample['affExtParam1'] == str(aff_ext_param1):
                    sample['sales'] = sample['sales']['amount']
                    sample['tentativeCommission'] = sample['tentativeCommission']['amount']
                    sample.pop("commissionRate", None)
                    sample.pop("affExtParam2", None)
                    sample.pop("customerType", None)
                    sample.pop("price", None)
                    sample.pop("quantity", None)
                    #sample.pop("tentativeCommission", None)
                    req_data.append(sample)
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <h2>📌 Order Report 📌</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            if req_data:
                if req_data:
                    df = pd.DataFrame(req_data)
                    df.index = df.index + 1  # Change index to start from 1
                    st.dataframe(df, use_container_width=True)

            else:
                st.warning("No data found for the given criteria.")
        

if __name__ == "__main__":
    main()

