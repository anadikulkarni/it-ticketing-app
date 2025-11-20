# Nilons IT Ticketing System

A professional ticketing application for IT support with role-based access control and Google Sheets integration.

## Features

- **Public Ticket Submission**: Users can submit tickets without logging in
- **IT Staff Portal**: Secure login for IT staff to manage tickets
- **Two Ticket Types**: SAP and Botree tickets
- **Google Sheets Integration**: Automatic synchronization with Google Sheets
- **Professional UI**: Clean, modern interface suitable for enterprise use
- **Real-time Updates**: Live ticket status management
- **Comprehensive Tracking**: Tracks all ticket details, timestamps, and actions
- **Optional Fields**: City, State, and SS/DB/DP Code are optional

## User Roles

### Public Users (No Login Required)
- Submit new tickets for SAP or Botree systems
- View ticket submission confirmation with Ticket ID
- All submissions are automatically recorded

### IT Staff (Login Required)
- View all tickets (SAP and Botree)
- Filter tickets by status (Open/Closed)
- Close tickets and add action taken
- All closures are automatically timestamped and assigned to the IT member

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

## IT Staff Credentials

### Default IT Accounts
- Username: `it1`, Password: `it123`
- Username: `it2`, Password: `it123`
- Username: `admin`, Password: `admin123`

**Important**: Change these credentials before deploying to production!

## Ticket Fields

### Required Fields (User-Filled):
1. Type of Query
2. SS/DB/DP Name
3. Incident Category (dropdown with predefined options)
4. Subject
5. Call Received From

### Optional Fields (User-Filled):
6. SS/DB/DP Code
7. City
8. State

### Auto-Generated Fields:
9. Ticket ID (format: SAP-YYYYMMDDHHMMSS or Botree-YYYYMMDDHHMMSS)
10. Received Date
11. Received Time
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

1. **Secure IT staff credentials** - Replace default passwords and consider using a database
2. **Secure credentials.json** - Never commit it to version control
3. **Use environment variables** for sensitive configuration
4. **Add IT staff management** interface for adding/removing IT users
5. **Implement proper logging** for audit trails
6. **Add data backup** mechanisms
7. **Consider HTTPS** for secure communication
8. **Deploy to a secure server** or cloud platform (AWS, Azure, Google Cloud)

## Customization

### Adding More IT Staff
Edit the `IT_STAFF` dictionary in `app.py`:

```python
IT_STAFF = {
    'username': {'password': 'secure_password', 'name': 'Display Name'},
}
```

### Modifying Incident Categories
Edit the `INCIDENT_CATEGORIES` list in `app.py`.

### Changing Spreadsheet Name
Update the `spreadsheet_name` variable in the `get_or_create_worksheet()` function.

## Workflow

### For Users:
1. Open the application
2. Select ticket type (SAP or Botree)
3. Fill in required fields (Type of Query, SS/DB/DP Name, Incident Category, Subject, Call Received From)
4. Optionally fill in City, State, SS/DB/DP Code
5. Submit ticket
6. Note the Ticket ID for future reference

### For IT Staff:
1. Click "IT Staff Login" in the sidebar
2. Login with IT credentials
3. Navigate to "View Tickets"
4. Select ticket type and filter by status
5. Expand ticket to view details
6. Enter action taken and close the ticket
7. System automatically records IT member, closing date, and time

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

### Login Issues
- Verify IT staff credentials in the `IT_STAFF` dictionary
- Check for typos in username/password

## Security Considerations

- The application allows public ticket submission without authentication
- Only IT staff require authentication to view and manage tickets
- All ticket closures are tracked with IT member name and timestamp
- Consider implementing rate limiting for ticket submission in production
- Use HTTPS in production to protect credentials during IT login

## Support

For issues or questions, contact your IT administrator.

## License

Internal use only - Nilons Enterprise