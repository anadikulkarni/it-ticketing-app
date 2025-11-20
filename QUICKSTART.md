# Quick Start Guide - Nilons IT Ticketing System

## For Testing (Without Google Sheets)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```

3. **Login with Demo Credentials**
   - Regular User: `user1` / `user123`
   - IT Staff: `it1` / `it123`

4. **Test the System**
   - As a regular user: Submit a ticket
   - As IT staff: View and close tickets
   
   Note: Without Google Sheets setup, data will be stored in local CSV files.

---

## For Production (With Google Sheets)

### Step 1: Google Cloud Setup

1. Go to https://console.cloud.google.com/
2. Create a new project (e.g., "Nilons Ticketing")
3. Enable APIs:
   - Google Sheets API
   - Google Drive API

### Step 2: Service Account Creation

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name: `nilons-ticketing-service`
4. Role: `Editor`
5. Click "Done"

### Step 3: Generate Credentials

1. Click on your service account
2. Go to "Keys" tab
3. "Add Key" → "Create New Key"
4. Select "JSON"
5. Download the file
6. **Rename to `credentials.json`**
7. **Move to the `nilons_ticketing` folder**

### Step 4: Google Sheet Setup

1. Create a new Google Sheet
2. Name it: **"Nilons IT Tickets"** (exact name)
3. Click "Share"
4. Add the service account email from credentials.json
   (looks like: `name@project-id.iam.gserviceaccount.com`)
5. Give "Editor" permission
6. Click "Done"

### Step 5: Run the Application

```bash
cd nilons_ticketing
pip install -r requirements.txt
streamlit run app.py
```

---

## User Guide

### For Regular Users

1. **Login** with your credentials
2. **Select Ticket Type**: Choose SAP or Botree
3. **Fill in the Form**:
   - Type of Query
   - SS/DB/DP Name and Code
   - City and State
   - Incident Category (dropdown)
   - Subject (detailed description)
   - Call Received From
4. **Submit** the ticket
5. Note your **Ticket ID** for future reference

### For IT Staff

1. **Login** with IT credentials
2. **Navigate** to "View Tickets"
3. **Select** ticket type (SAP or Botree)
4. **Filter** by status (All/Open/Closed)
5. **Expand** a ticket to view details
6. **Close Ticket**:
   - Enter "Action Taken"
   - Click "Close Ticket"
   - System automatically records:
     - Your username
     - Closing date and time

---

## Troubleshooting

### "Credentials not found"
- Ensure `credentials.json` is in the same folder as `app.py`
- Check the filename is exactly `credentials.json`

### "Spreadsheet not found"
- Verify the Google Sheet is named "Nilons IT Tickets"
- Check the service account has access to the sheet

### "Permission denied"
- Make sure the service account has "Editor" permissions
- Verify both APIs are enabled in Google Cloud Console

### App won't start
- Install dependencies: `pip install -r requirements.txt`
- Check Python version (3.8 or higher recommended)

---

## Default Demo Accounts

### Regular Users
| Username | Password | Role |
|----------|----------|------|
| user1    | user123  | User |
| user2    | user123  | User |

### IT Staff
| Username | Password | Role |
|----------|----------|------|
| it1      | it123    | IT   |
| admin    | admin123 | IT   |

**Important**: Change these credentials in production!

---

## Support

For technical issues, contact your system administrator.

For Google Sheets issues, refer to the detailed README.md file.