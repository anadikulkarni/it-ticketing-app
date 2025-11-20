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

3. **Test as a User (No Login Required)**
   - Open the app in your browser (usually http://localhost:8501)
   - Select SAP or Botree ticket type
   - Fill in the required fields
   - Submit ticket and note your Ticket ID

4. **Test as IT Staff**
   - Click "IT Staff Login" in the sidebar
   - Login with: `it1` / `it123`
   - View tickets, filter by status
   - Close open tickets with action details
   
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
7. **Move to the same folder as `app.py`**

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
streamlit run app.py
```

---

## User Guide

### For Regular Users (No Login Required)

1. **Open the Application**
   - Navigate to the app URL
   - No login needed!

2. **Select Ticket Type**
   - Choose SAP or Botree

3. **Fill in Required Fields** (marked with *):
   - Type of Query
   - SS/DB/DP Name
   - Incident Category (dropdown)
   - Subject (detailed description)
   - Call Received From

4. **Optional Fields** (can be left blank):
   - SS/DB/DP Code
   - City
   - State

5. **Optional: Attach an Image**
   - Click "Browse files" to upload a screenshot or photo
   - Supported formats: PNG, JPG, JPEG, GIF
   - Preview will appear before submission
   - Image will be automatically uploaded to Google Drive

6. **Submit the Ticket**
   - Click "Submit Ticket"
   - Note your **Ticket ID** for future reference
   - The ticket is automatically timestamped
   - Image URL is stored in the system

### For IT Staff

1. **Login**
   - Click "IT Staff Login" in the sidebar
   - Enter your IT credentials

2. **View Tickets**
   - Navigate to "View Tickets"
   - Select ticket type (SAP or Botree)
   - Filter by status (All/Open/Closed)
   - 📷 icon indicates tickets with attached images

3. **View Attached Images**
   - Expand the ticket
   - Look for "Attached Image" section
   - Click "View Image in Browser" to open in new tab
   - Click "Show Preview" to display inline

4. **Close a Ticket**
   - Expand an open ticket
   - Scroll to the bottom
   - Enter "Action Taken" description
   - Click "Close Ticket"
   - System automatically records:
     - Your username
     - Closing date and time

5. **Submit Tickets**
   - IT staff can also submit tickets via "Submit New Ticket"

---

## Troubleshooting

### "Credentials not found"
- Ensure `credentials.json` is in the same folder as `app.py`
- Check the filename is exactly `credentials.json`

### "Spreadsheet not found"
- Verify the Google Sheet is named exactly "Nilons IT Tickets"
- Check the service account has access to the sheet

### "Permission denied"
- Make sure the service account has "Editor" permissions
- Verify both APIs are enabled in Google Cloud Console

### App won't start
- Install dependencies: `pip install -r requirements.txt`
- Check Python version (3.8 or higher recommended)

### Can't submit tickets
- Check all required fields (marked with *) are filled
- Verify internet connection if using Google Sheets

### IT Login Issues
- Verify username and password are correct
- Check `IT_STAFF` dictionary in app.py

---

## Default IT Staff Accounts

| Username | Password | Name      |
|----------|----------|-----------|
| it1      | it123    | IT Staff 1|
| it2      | it123    | IT Staff 2|
| admin    | admin123 | Admin     |

**⚠️ IMPORTANT**: Change these credentials before production deployment!

---

## Ticket Field Breakdown

### Always Required:
- Type of Query
- SS/DB/DP Name
- Incident Category
- Subject
- Call Received From

### Optional (Can Be Blank):
- SS/DB/DP Code
- City
- State
- Image Upload (PNG, JPG, JPEG, GIF)

### Auto-Generated:
- Ticket ID
- Received Date & Time
- Status (Open → Closed)
- IT Member Assigned (on close)
- Closing Date & Time (on close)
- Image URL (if image uploaded)

---

## Key Features

✅ **No Login for Users** - Quick and easy ticket submission  
🔐 **Secure IT Portal** - Authentication required for ticket management  
📷 **Image Upload** - Attach screenshots or photos to tickets  
☁️ **Cloud Storage** - Images stored in Google Drive with shareable links  
📊 **Real-time Sync** - Automatic Google Sheets integration  
📋 **Two Systems** - Support for both SAP and Botree  
🎫 **Unique Ticket IDs** - Timestamp-based tracking  
✨ **Professional UI** - Clean, modern interface  
💾 **Fallback Storage** - Works with or without Google Sheets  

---

## Support

For technical issues:
- Check the troubleshooting section above
- Review the detailed README.md file
- Contact your system administrator

For Google Sheets issues:
- Verify service account permissions
- Check API enablement
- Ensure spreadsheet is shared correctly

---

## Next Steps

1. ✅ Test the application locally
2. ✅ Set up Google Sheets integration
3. ✅ Customize IT staff accounts
4. ✅ Update incident categories if needed
5. ✅ Deploy to production server
6. ✅ Share the URL with your team
7. ✅ Train IT staff on ticket management

Enjoy your new ticketing system! 🎉