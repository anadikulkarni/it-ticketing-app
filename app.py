import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Page configuration
st.set_page_config(
    page_title="Nilons IT Ticketing System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .ticket-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .status-open {
        background-color: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .status-closed {
        background-color: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    div[data-testid="stSidebar"] {
        background-color: #f9fafb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# Dummy user database (in production, use a proper database)
USERS = {
    'user1': {'password': 'user123', 'role': 'user'},
    'user2': {'password': 'user123', 'role': 'user'},
    'it1': {'password': 'it123', 'role': 'it'},
    'it2': {'password': 'it123', 'role': 'it'},
    'admin': {'password': 'admin123', 'role': 'it'}
}

# Incident categories
INCIDENT_CATEGORIES = [
    "Billing Issue",
    "Customer Migration",
    "Day End Process",
    "Delivery Process",
    "Google Form",
    "GRN Receiving",
    "Login Issue",
    "Purchase Return",
    "Reports",
    "Scheme",
    "SFA Order",
    "Stock",
    "Tally Integration",
    "Training"
]

# Google Sheets setup
def get_google_sheets_client():
    """Initialize Google Sheets client"""
    try:
        # Check if credentials file exists
        creds_file = 'credentials.json'
        if not os.path.exists(creds_file):
            st.warning("⚠️ Google Sheets credentials not found. Using local storage mode.")
            return None
        
        # Define the scope
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        
        # Load credentials
        creds = Credentials.from_service_account_file(creds_file, scopes=scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

def get_or_create_worksheet(client, ticket_type):
    """Get or create worksheet for ticket type"""
    if client is None:
        return None
    
    try:
        # Replace with your Google Sheets URL or ID
        spreadsheet_name = "Nilons IT Tickets"
        
        try:
            spreadsheet = client.open(spreadsheet_name)
        except:
            st.error(f"Spreadsheet '{spreadsheet_name}' not found. Please create it first.")
            return None
        
        worksheet_name = f"{ticket_type} Tickets"
        
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except:
            # Create worksheet if it doesn't exist
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
            
            # Add headers
            headers = [
                "Ticket ID",
                "Type of Query",
                "SS/DB/DP Name",
                "SS/DB/DP Code",
                "City",
                "State",
                "Incident Category",
                "Subject",
                "Call Received From",
                "Received Date",
                "Received Time",
                "Status",
                "IT Member Assigned",
                "Closing Date",
                "Closing Time",
                "Action Taken"
            ]
            worksheet.append_row(headers)
        
        return worksheet
    except Exception as e:
        st.error(f"Error accessing worksheet: {e}")
        return None

def save_ticket_to_sheets(ticket_data, ticket_type):
    """Save ticket to Google Sheets"""
    client = get_google_sheets_client()
    worksheet = get_or_create_worksheet(client, ticket_type)
    
    if worksheet:
        try:
            row = [
                ticket_data['ticket_id'],
                ticket_data['type_of_query'],
                ticket_data['ss_db_dp_name'],
                ticket_data['ss_db_dp_code'],
                ticket_data['city'],
                ticket_data['state'],
                ticket_data['incident_category'],
                ticket_data['subject'],
                ticket_data['call_received_from'],
                ticket_data['received_date'],
                ticket_data['received_time'],
                ticket_data['status'],
                ticket_data.get('it_member_assigned', ''),
                ticket_data.get('closing_date', ''),
                ticket_data.get('closing_time', ''),
                ticket_data.get('action_taken', '')
            ]
            worksheet.append_row(row)
            return True
        except Exception as e:
            st.error(f"Error saving to Google Sheets: {e}")
            return False
    else:
        # Fallback to local CSV storage
        save_ticket_to_csv(ticket_data, ticket_type)
        return True

def save_ticket_to_csv(ticket_data, ticket_type):
    """Fallback: Save ticket to local CSV file"""
    filename = f"{ticket_type.lower()}_tickets.csv"
    
    df_new = pd.DataFrame([ticket_data])
    
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(filename, index=False)
    else:
        df_new.to_csv(filename, index=False)

def get_tickets_from_sheets(ticket_type):
    """Get tickets from Google Sheets"""
    client = get_google_sheets_client()
    worksheet = get_or_create_worksheet(client, ticket_type)
    
    if worksheet:
        try:
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error reading from Google Sheets: {e}")
            return get_tickets_from_csv(ticket_type)
    else:
        return get_tickets_from_csv(ticket_type)

def get_tickets_from_csv(ticket_type):
    """Fallback: Get tickets from local CSV"""
    filename = f"{ticket_type.lower()}_tickets.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame()

def update_ticket_in_sheets(ticket_id, ticket_type, it_member, action_taken):
    """Update ticket status in Google Sheets"""
    client = get_google_sheets_client()
    worksheet = get_or_create_worksheet(client, ticket_type)
    
    closing_date = datetime.now().strftime("%Y-%m-%d")
    closing_time = datetime.now().strftime("%H:%M:%S")
    
    if worksheet:
        try:
            # Find the row with the ticket ID
            cell = worksheet.find(ticket_id)
            row_num = cell.row
            
            # Update the row
            worksheet.update_cell(row_num, 12, "Closed")  # Status
            worksheet.update_cell(row_num, 13, it_member)  # IT Member Assigned
            worksheet.update_cell(row_num, 14, closing_date)  # Closing Date
            worksheet.update_cell(row_num, 15, closing_time)  # Closing Time
            worksheet.update_cell(row_num, 16, action_taken)  # Action Taken
            return True
        except Exception as e:
            st.error(f"Error updating Google Sheets: {e}")
            return False
    else:
        # Fallback to CSV
        return update_ticket_in_csv(ticket_id, ticket_type, it_member, action_taken, closing_date, closing_time)

def update_ticket_in_csv(ticket_id, ticket_type, it_member, action_taken, closing_date, closing_time):
    """Fallback: Update ticket in local CSV"""
    filename = f"{ticket_type.lower()}_tickets.csv"
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        mask = df['ticket_id'] == ticket_id
        df.loc[mask, 'status'] = 'Closed'
        df.loc[mask, 'it_member_assigned'] = it_member
        df.loc[mask, 'closing_date'] = closing_date
        df.loc[mask, 'closing_time'] = closing_time
        df.loc[mask, 'action_taken'] = action_taken
        df.to_csv(filename, index=False)
        return True
    return False

def login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>🎫 Nilons IT Ticketing System</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Secure Access Portal</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='ticket-card'>", unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔐 Login", use_container_width=True):
                    if username in USERS and USERS[username]['password'] == password:
                        st.session_state.logged_in = True
                        st.session_state.user_role = USERS[username]['role']
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("""
            **Demo Credentials:**
            
            **Regular Users:**
            - username: `user1`, password: `user123`
            - username: `user2`, password: `user123`
            
            **IT Staff:**
            - username: `it1`, password: `it123`
            - username: `admin`, password: `admin123`
            """)

def submit_ticket_page():
    """Page for submitting tickets"""
    st.markdown("<h1 class='main-header'>📝 Submit New Ticket</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Fill in the details below to create a support ticket</p>", unsafe_allow_html=True)
    
    # Ticket type selection
    ticket_type = st.radio(
        "Select Ticket Type",
        ["SAP", "Botree"],
        horizontal=True,
        help="Choose the system your issue is related to"
    )
    
    st.markdown("---")
    
    with st.form("ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            type_of_query = st.text_input("Type of Query *", help="Brief description of query type")
            ss_db_dp_name = st.text_input("SS/DB/DP Name *", help="Enter the name")
            ss_db_dp_code = st.text_input("SS/DB/DP Code *", help="Enter the code")
            city = st.text_input("City *", help="Enter city")
        
        with col2:
            state = st.text_input("State *", help="Enter state")
            incident_category = st.selectbox("Incident Category *", INCIDENT_CATEGORIES)
            call_received_from = st.text_input("Call Received From *", help="Name of the person")
        
        subject = st.text_area("Subject *", help="Detailed description of the issue", height=100)
        
        submit_button = st.form_submit_button("🚀 Submit Ticket", use_container_width=True)
        
        if submit_button:
            # Validate required fields
            if not all([type_of_query, ss_db_dp_name, ss_db_dp_code, city, state, subject, call_received_from]):
                st.error("Please fill in all required fields marked with *")
            else:
                # Generate ticket ID
                now = datetime.now()
                ticket_id = f"{ticket_type}-{now.strftime('%Y%m%d%H%M%S')}"
                
                # Create ticket data
                ticket_data = {
                    'ticket_id': ticket_id,
                    'type_of_query': type_of_query,
                    'ss_db_dp_name': ss_db_dp_name,
                    'ss_db_dp_code': ss_db_dp_code,
                    'city': city,
                    'state': state,
                    'incident_category': incident_category,
                    'subject': subject,
                    'call_received_from': call_received_from,
                    'received_date': now.strftime("%Y-%m-%d"),
                    'received_time': now.strftime("%H:%M:%S"),
                    'status': 'Open',
                    'it_member_assigned': '',
                    'closing_date': '',
                    'closing_time': '',
                    'action_taken': ''
                }
                
                # Save ticket
                if save_ticket_to_sheets(ticket_data, ticket_type):
                    st.success(f"✅ Ticket submitted successfully! Ticket ID: **{ticket_id}**")
                    st.balloons()
                else:
                    st.error("Failed to submit ticket. Please try again.")

def view_tickets_page():
    """Page for IT staff to view and manage tickets"""
    st.markdown("<h1 class='main-header'>🎯 Ticket Management</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>View and manage support tickets</p>", unsafe_allow_html=True)
    
    # Ticket type filter
    ticket_type = st.radio(
        "Select Ticket Type to View",
        ["SAP", "Botree"],
        horizontal=True
    )
    
    # Status filter
    status_filter = st.radio(
        "Filter by Status",
        ["All", "Open", "Closed"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Get tickets
    df = get_tickets_from_sheets(ticket_type)
    
    if df.empty:
        st.info(f"No {ticket_type} tickets found.")
        return
    
    # Apply status filter
    if status_filter != "All":
        df = df[df['Status'] == status_filter]
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tickets", len(df))
    with col2:
        open_tickets = len(df[df['Status'] == 'Open']) if 'Status' in df.columns else 0
        st.metric("Open Tickets", open_tickets)
    with col3:
        closed_tickets = len(df[df['Status'] == 'Closed']) if 'Status' in df.columns else 0
        st.metric("Closed Tickets", closed_tickets)
    
    st.markdown("---")
    
    # Display tickets
    for idx, row in df.iterrows():
        with st.expander(f"🎫 {row['Ticket ID']} - {row['Incident Category']} ({row['Status']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Type of Query:** {row['Type of Query']}")
                st.markdown(f"**SS/DB/DP Name:** {row['SS/DB/DP Name']}")
                st.markdown(f"**SS/DB/DP Code:** {row['SS/DB/DP Code']}")
                st.markdown(f"**City:** {row['City']}")
                st.markdown(f"**State:** {row['State']}")
                st.markdown(f"**Call Received From:** {row['Call Received From']}")
            
            with col2:
                st.markdown(f"**Incident Category:** {row['Incident Category']}")
                st.markdown(f"**Received Date:** {row['Received Date']}")
                st.markdown(f"**Received Time:** {row['Received Time']}")
                if row['Status'] == 'Closed':
                    st.markdown(f"**IT Member:** {row['IT Member Assigned']}")
                    st.markdown(f"**Closing Date:** {row['Closing Date']}")
                    st.markdown(f"**Closing Time:** {row['Closing Time']}")
            
            st.markdown(f"**Subject:** {row['Subject']}")
            
            if row['Status'] == 'Closed':
                st.markdown(f"**Action Taken:** {row['Action Taken']}")
            
            # Close ticket option for open tickets
            if row['Status'] == 'Open':
                st.markdown("---")
                with st.form(f"close_form_{row['Ticket ID']}"):
                    action_taken = st.text_area("Action Taken", key=f"action_{row['Ticket ID']}")
                    
                    if st.form_submit_button("✅ Close Ticket"):
                        if action_taken:
                            if update_ticket_in_sheets(
                                row['Ticket ID'],
                                ticket_type,
                                st.session_state.username,
                                action_taken
                            ):
                                st.success("Ticket closed successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to close ticket.")
                        else:
                            st.error("Please provide action taken details.")

def main():
    """Main application"""
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.markdown(f"### 👤 Welcome, {st.session_state.username}!")
            st.markdown(f"**Role:** {st.session_state.user_role.upper()}")
            st.markdown("---")
            
            if st.session_state.user_role == 'user':
                page = st.radio("Navigation", ["Submit Ticket"])
            else:
                page = st.radio("Navigation", ["Submit Ticket", "View Tickets"])
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.rerun()
        
        # Main content
        if page == "Submit Ticket":
            submit_ticket_page()
        elif page == "View Tickets":
            view_tickets_page()

if __name__ == "__main__":
    main()