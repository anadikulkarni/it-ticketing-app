# Image Upload Feature - Setup Guide

## Overview

The Nilons IT Ticketing System now supports optional image attachments with each ticket. Images are automatically uploaded to Google Drive and stored as shareable URLs in Google Sheets.

## Features

- **Optional Image Upload**: Users can attach screenshots or photos when submitting tickets
- **Supported Formats**: PNG, JPG, JPEG, GIF
- **Automatic Upload**: Images are automatically uploaded to Google Drive
- **Shareable Links**: Public viewing links are stored in Google Sheets
- **Image Preview**: Users see a preview before submitting
- **IT Staff Viewing**: IT staff can view images directly or open in browser
- **Fallback Storage**: Local storage available if Google Drive is not configured

## How It Works

### For Users (Ticket Submission)

1. Fill in the ticket details as usual
2. Scroll to the "Attach Image" section
3. Click "Browse files" to select an image
4. Preview appears automatically
5. Submit the ticket
6. Image is uploaded to Google Drive
7. Image URL is stored in Google Sheet

### For IT Staff (Viewing)

1. Open the ticket management portal
2. Tickets with images show a 📷 icon in the title
3. Expand the ticket to view details
4. In the "Attached Image" section:
   - Click "View Image in Browser" to open in new tab
   - Click "Show Preview" to display inline (iframe)

## Google Drive Setup

The application automatically:
- Creates a folder named "Nilons Ticket Images" in Google Drive
- Uploads images to this folder
- Names images with format: `{TicketID}_{original_filename}`
- Sets public viewing permissions (anyone with link can view)
- Stores the shareable URL in Google Sheets

## Google Sheets Integration

A new column "Image URL" has been added to the worksheets:
- Column 17 in both SAP and Botree ticket worksheets
- Contains the Google Drive shareable link
- Empty if no image was uploaded

## Permissions Required

The service account needs the following permissions:
- Google Sheets API (already configured)
- Google Drive API (already configured)
- Scope: `https://www.googleapis.com/auth/drive` (already included)

**No additional setup required** if you've already configured Google Sheets!

## Image URL Formats

### Google Drive (Production)
```
https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing
```

### Local Storage (Fallback)
```
local://ticket_images/{TicketID}_{filename}
```

## Troubleshooting

### Image Upload Fails
**Problem**: Image upload shows an error
**Solutions**:
1. Check Google Drive API is enabled in Google Cloud Console
2. Verify service account has proper permissions
3. Check internet connectivity
4. Verify image file size (recommended < 10MB)

### Image Not Displaying for IT Staff
**Problem**: Preview button doesn't work
**Solutions**:
1. Click "View Image in Browser" instead
2. Check if the URL is accessible
3. Verify the service account made the file public
4. Check browser allows iframes (for inline preview)

### Folder Not Created
**Problem**: "Nilons Ticket Images" folder not appearing
**Solution**: 
- The folder is created automatically on first image upload
- Check the service account's Drive (may need to share with your account to see)

### Local Storage Mode
**Problem**: Images saving locally instead of Google Drive
**Solution**: 
- This is the fallback when `credentials.json` is not configured
- Images are saved to `ticket_images/` directory
- Configure Google credentials to use Drive storage

## File Size Recommendations

- **Optimal**: 1-5 MB per image
- **Maximum**: 10 MB (to ensure smooth upload)
- **Format**: PNG or JPG recommended

## Security Considerations

### Current Implementation:
- Images are set to public viewing (anyone with link)
- Links are only known to IT staff and ticket submitters
- No authentication required to view images

### For Enhanced Security (Future):
Consider implementing:
- Restricted sharing (only specific users)
- Expiring links
- Image encryption
- Access logging

## Data Storage

### With Google Drive:
- Images: Google Drive "Nilons Ticket Images" folder
- URLs: Google Sheets "Image URL" column
- Backup: Consider regular Drive backups

### Without Google Drive (Fallback):
- Images: Local `ticket_images/` directory
- Paths: CSV files with local paths
- Backup: Include `ticket_images/` in backup routine

## Testing the Feature

1. **Submit a test ticket with an image**:
   ```
   - Go to ticket submission page
   - Fill in required fields
   - Upload a test image (screenshot)
   - Submit and note the Ticket ID
   ```

2. **Verify in Google Drive**:
   ```
   - Log into Google Drive with service account
   - Look for "Nilons Ticket Images" folder
   - Verify image was uploaded
   ```

3. **Verify in Google Sheets**:
   ```
   - Open the Google Sheet
   - Find the ticket row
   - Check column 17 (Image URL) has a link
   - Click the link to verify it works
   ```

4. **Test IT Staff View**:
   ```
   - Login as IT staff
   - View the ticket
   - Verify 📷 icon appears
   - Click "View Image in Browser"
   - Click "Show Preview"
   ```

## Code Changes Summary

### New Dependencies:
- `google-api-python-client` (added to requirements.txt)

### New Functions:
- `upload_image_to_drive()`: Uploads image to Google Drive
- `save_image_locally()`: Fallback for local storage

### Modified Functions:
- `get_google_sheets_client()`: Now also returns Drive service
- `get_or_create_worksheet()`: Added "Image URL" column
- `save_ticket_to_sheets()`: Includes image URL in row
- `submit_ticket_page()`: Added file uploader widget
- `view_tickets_page()`: Added image display section

### New Files Generated:
- `ticket_images/`: Directory for local image storage (fallback mode)

## Maintenance

### Regular Tasks:
1. Monitor Google Drive storage space
2. Check "Nilons Ticket Images" folder periodically
3. Archive old images if needed
4. Verify links in closed tickets still work

### Cleanup:
To remove old images:
```python
# Manual cleanup script (run with caution)
# Archive images from closed tickets older than X days
# Delete local images if using Google Drive
```

## FAQ

**Q: Can users upload multiple images?**
A: Currently, one image per ticket. Future versions could support multiple images.

**Q: What happens if image upload fails?**
A: The ticket is still created, just without the image. A warning is shown to the user.

**Q: Can IT staff upload images when closing tickets?**
A: Not currently, but this could be added in a future version.

**Q: Are images compressed?**
A: No, images are uploaded as-is. Users should compress before uploading if needed.

**Q: Can images be edited after upload?**
A: No, images are read-only once uploaded. A new ticket would be needed.

## Support

For issues with image uploads:
1. Check this guide first
2. Verify Google Drive API is enabled
3. Test with a small image file
4. Check browser console for errors
5. Contact your system administrator

---

**Version**: 2.0 with Image Upload Support
**Last Updated**: November 2025