# Nilons IT Ticketing System

A professional ticketing application for IT support with role-based access control and Google Sheets integration.

## Features

- **Role-Based Access Control**: Separate interfaces for regular users and IT staff
- **Two Ticket Types**: SAP and Botree tickets
- **Google Sheets Integration**: Automatic synchronization with Google Sheets
- **Professional UI**: Clean, modern interface suitable for enterprise use
- **Real-time Updates**: Live ticket status management
- **Comprehensive Tracking**: Tracks all ticket details, timestamps, and actions

## User Roles

### Regular Users
- Submit new tickets
- View ticket submission confirmation

### IT Staff
- Submit new tickets
- View all tickets (SAP and Botree)
- Filter tickets by status (Open/Closed)
- Close tickets and add action taken
- All closures are automatically timestamped and assigned

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Sheets Setup

#### A. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API

#### B. Create Service Account
1. Navigate to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Give it a name (e.g., "nilons-ticketing")
4. Click "Create and Continue"
5. Grant the role "Editor" 
6. Click "Done"

#### C. Generate Credentials
1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Choose "JSON" format
5. Download the JSON file
6. Rename it to `credentials.json`
7. Place it in the same directory as `app.py`

#### D. Create and Share Google Sheet
1. Create a new Google Sheet named "Nilons IT Tickets"
2. Share the sheet with the service account email (found in credentials.json as "client_email")
3. Give it "Editor" permissions

### 3. Run the Application

```bash
streamlit run app.py
```

## Demo Credentials

### Regular Users
- Username: `user1`, Password: `user123`
- Username: `user2`, Password: `user123`

### IT Staff
- Username: `it1`, Password: `it123`
- Username: `admin`, Password: `admin123`

## Ticket Fields

### User-Filled Fields:
1. Type of Query
2. SS/DB/DP Name
3. SS/DB/DP Code
4. City
5. State
6. Incident Category (dropdown with predefined options)
7. Subject
8. Call Received From

### Auto-Generated Fields:
9. Received Date
10. Received Time
11. Ticket ID (format: SAP-YYYYMMDDHHMMSS or Botree-YYYYMMDDHHMMSS)
12. Status (Open/Closed)

### IT-Filled Fields (when closing):
13. IT Member Assigned (automatically captures who closed the ticket)
14. Closing Date (auto-generated)
15. Closing Time (auto-generated)
16. Action Taken

## Google Sheets Structure

The application creates separate worksheets for each ticket type:
- "SAP Tickets" worksheet
- "Botree Tickets" worksheet

Each worksheet contains all the fields listed above in columns.

## Fallback Mode

If Google Sheets credentials are not configured, the application automatically falls back to local CSV storage:
- `sap_tickets.csv`
- `botree_tickets.csv`

## Incident Categories

- Billing Issue
- Customer Migration
- Day End Process
- Delivery Process
- Google Form
- GRN Receiving
- Login Issue
- Purchase Return
- Reports
- Scheme
- SFA Order
- Stock
- Tally Integration
- Training

## Production Deployment

For production use:

1. **Replace the dummy user authentication** with a proper authentication system (database, LDAP, OAuth, etc.)
2. **Secure credentials.json** - never commit it to version control
3. **Use environment variables** for sensitive configuration
4. **Add user management** interface for adding/removing users
5. **Implement proper logging** for audit trails
6. **Add data backup** mechanisms
7. **Consider using Streamlit sharing** or deploy to a cloud platform

## Customization

### Adding More Users
Edit the `USERS` dictionary in `app.py`:

```python
USERS = {
    'username': {'password': 'password', 'role': 'user'},  # or 'it'
}
```

### Modifying Incident Categories
Edit the `INCIDENT_CATEGORIES` list in `app.py`.

### Changing Spreadsheet Name
Update the `spreadsheet_name` variable in the `get_or_create_worksheet()` function.

## Troubleshooting

### Google Sheets Connection Issues
- Verify credentials.json is in the correct location
- Ensure the service account email has access to the spreadsheet
- Check that both Google Sheets API and Google Drive API are enabled

### Permission Errors
- Verify the service account has "Editor" permissions on the spreadsheet
- Check file permissions on credentials.json

### Module Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Support

For issues or questions, contact your IT administrator.

## License

Internal use only - Nilons Enterprise