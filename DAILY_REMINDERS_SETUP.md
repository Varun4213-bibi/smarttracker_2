# Daily Automatic Expiry Reminders - Setup Guide

## Overview
The system now sends **daily automatic email reminders every morning at 8:00 AM IST** to users with items expiring within their chosen reminder window (3 days, 1 week, or 2 weeks).

## How It Works

### User Experience
1. **User selects reminder frequency** in Profile page:
   - 3 days before expiry (urgent items only)
   - 1 week before expiry (default)
   - 2 weeks before expiry (maximum advance notice)

2. **Every morning at 8 AM IST**, the system:
   - Checks all items for each user
   - Filters items expiring within their chosen window
   - Sends personalized email with item list
   - Continues daily until items expire or are removed

3. **Email content includes**:
   - Number of items expiring soon
   - Countdown days for each item
   - Urgent warnings for items expiring in ≤3 days
   - Clear indication it's a daily reminder

### Example Scenarios

**Scenario 1: User selects "2 weeks before expiry"**
- Day 14: Gets first reminder "Item expires in 14 days"
- Day 13: Gets reminder "Item expires in 13 days"
- Day 12: Gets reminder "Item expires in 12 days"
- ...continues daily...
- Day 1: Gets urgent reminder "⚠️ Item expires in 1 day!"
- Day 0: Item expires, no more reminders

**Scenario 2: User selects "3 days before expiry"**
- Day 14-4: No reminders
- Day 3: Gets first reminder "Item expires in 3 days"
- Day 2: Gets reminder "Item expires in 2 days"
- Day 1: Gets urgent reminder "⚠️ Item expires in 1 day!"

## Running the System

### Development Setup

**Terminal 1: Start Django Server**
```powershell
cd c:\Users\varsh\OneDrive\Desktop\project\expirytracker
python manage.py runserver
```

**Terminal 2: Start Redis (Required for Celery)**
```powershell
cd c:\Users\varsh\OneDrive\Desktop\project
redis-server redis\redis.windows.conf
```

**Terminal 3: Start Celery Worker**
```powershell
cd c:\Users\varsh\OneDrive\Desktop\project\expirytracker
celery -A expirytracker worker --loglevel=info --pool=solo
```

**Terminal 4: Start Celery Beat (Daily Scheduler)**
```powershell
cd c:\Users\varsh\OneDrive\Desktop\project\expirytracker
celery -A expirytracker beat --loglevel=info
```

### Testing Reminders

**Option 1: Manual Test Command**
```powershell
python manage.py send_test_reminder
```

**Option 2: Django Shell**
```powershell
python manage.py shell
>>> from tracker.tasks import send_expiry_reminders
>>> send_expiry_reminders()
```

**Option 3: Celery Shell (Test Scheduled Task)**
```powershell
celery -A expirytracker shell
>>> from tracker.tasks import send_expiry_reminders
>>> send_expiry_reminders.delay()  # Async execution
```

### Verifying Schedule

Check that the daily task is registered:
```powershell
python manage.py shell
>>> from django_celery_beat.models import PeriodicTask
>>> PeriodicTask.objects.all()
```

Or inspect Celery Beat schedule:
```powershell
celery -A expirytracker inspect scheduled
```

## Production Deployment (Render)

### Environment Variables
Add to Render dashboard:
```
TIME_ZONE=Asia/Kolkata
CELERY_BROKER_URL=<your-redis-url>
```

### Services Required
1. **Web Service**: Django app (already configured)
2. **Worker Service**: Celery worker (already configured)
3. **Beat Service**: Celery beat scheduler (ADD THIS)
4. **Redis**: Message broker (already configured)

### Add Celery Beat Service in render.yaml
```yaml
- type: worker
  name: celery-beat
  runtime: python
  buildCommand: "pip install -r requirements.txt"
  startCommand: "celery -A expirytracker beat --loglevel=info"
  envVars:
    - key: DJANGO_SETTINGS_MODULE
      value: expirytracker.settings
```

## Configuration Details

### Schedule (settings.py)
```python
CELERY_BEAT_SCHEDULE = {
    'send-daily-expiry-reminders': {
        'task': 'tracker.tasks.send_expiry_reminders',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM IST daily
    },
}
```

### Customizing Schedule Time
Change the `hour` value in settings.py:
- `hour=6` → 6:00 AM
- `hour=9` → 9:00 AM
- `hour=20` → 8:00 PM

### Timezone
Set to `Asia/Kolkata` for Indian Standard Time (IST)

## User Controls

Users can manage reminders via Profile page:
- ✅ **Enable/Disable Email Reminders**: Toggle checkbox
- ✅ **Choose Frequency**: 3 days / 1 week / 2 weeks
- ✅ **Enable/Disable Push Notifications**: Separate toggle

## Monitoring

### Check Task Execution Logs
```powershell
# In Celery worker terminal
# Look for: "Starting daily expiry reminders task"
# Success: "Sent reminders to X users"
# Failures: Check error messages
```

### Email Delivery
- Emails sent via Gmail SMTP
- Check Gmail "Sent" folder for varshavarun4213@gmail.com
- Monitor bounce rates and delivery failures

### Database Verification
```sql
-- Check users with reminders enabled
SELECT u.username, up.reminder_days, up.email_reminders_enabled 
FROM auth_user u 
JOIN tracker_userprofile up ON u.id = up.user_id 
WHERE up.email_reminders_enabled = TRUE;

-- Check items in reminder window
SELECT name, expiry_date, 
       expiry_date - CURRENT_DATE as days_until_expiry 
FROM tracker_item 
WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '14 days';
```

## Troubleshooting

### Issue: Reminders not sending
**Check:**
1. Celery Beat is running (`ps aux | grep celery`)
2. Redis is running (`redis-cli ping` should return PONG)
3. Email credentials are valid (test with `python manage.py shell`)
4. Users have `email_reminders_enabled=True`

### Issue: Wrong time execution
**Fix:** Verify `TIME_ZONE = 'Asia/Kolkata'` in settings.py

### Issue: Duplicate emails
**Check:** Only one Celery Beat instance should run (kill duplicates)

### Issue: No emails despite items expiring
**Verify:**
1. User has valid email address
2. Item expiry_date is within reminder window
3. Email SMTP settings are correct

## Best Practices

1. **Test before production**: Use management command to verify emails
2. **Monitor logs**: Check Celery worker output daily
3. **User education**: Inform users about daily reminders
4. **Graceful degradation**: Task retries 3 times on email failure
5. **Rate limiting**: Consider Gmail daily sending limits (500/day)

## Benefits

✅ **Consistent reminders**: Never miss expiry dates  
✅ **User control**: Choose reminder frequency  
✅ **Automated**: No manual intervention needed  
✅ **Scalable**: Handles thousands of users  
✅ **Reliable**: Retry logic ensures delivery  
✅ **Timezone-aware**: Sends at local morning time  

## Next Steps

- [ ] Add SMS reminders (Twilio integration)
- [ ] Implement "snooze" functionality
- [ ] Add weekly summary emails
- [ ] Create reminder analytics dashboard
- [ ] Support multiple reminder times per day
