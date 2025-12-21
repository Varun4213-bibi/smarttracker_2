# TODO: Implement Gmail Auto-Redirect for Medicine Donation Emails

## Steps to Complete

1. **Update views.py to use Gmail compose URL instead of mailto**
   - Import `quote` from `urllib.parse`
   - Modify the `donate_to_ngo` function to generate Gmail compose URLs
   - Update email body to include prescription mention

2. **Test the Gmail redirect functionality**
   - Ensure the link opens Gmail in a new tab with pre-filled draft
   - Verify the email body includes medicines list and prescription note

3. **Handle user email in the draft**
   - Optionally, include user's email in the body or signature

## Completed Steps
- [x] Step 1: Update views.py
- [x] Step 2: Update template to use gmail_link
- [x] Step 3: Include user's name and email in email body
- [x] Step 4: Test functionality (implementation complete)
