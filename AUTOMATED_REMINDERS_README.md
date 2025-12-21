# Automated Expiry Reminders Setup

## Problem
The expiry reminders only work when VS Code terminals are running. When VS Code is closed, the Celery worker and beat scheduler processes stop, so automated reminders don't work.

## Solution
Set up Celery services to run as background processes using Windows Task Scheduler.

## Step 1: Create Batch Files
Two batch files have been created:
- `start_celery_worker.bat` - Runs the Celery worker
- `start_celery_beat.bat` - Runs the Celery beat scheduler

## Step 2: Set Up Windows Task Scheduler

### For Celery Worker:
1. Open Windows Task Scheduler
2. Click "Create Task"
3. General Tab:
   - Name: "ExpiryTracker Celery Worker"
   - Check "Run with highest privileges"
   - Configure for: Windows 10
4. Triggers Tab:
   - New Trigger: "At log on" (or "At startup" for automatic start)
5. Actions Tab:
   - New Action: "Start a program"
   - Program/script: `C:\Users\varsh\OneDrive\Desktop\project\start_celery_worker.bat`
   - Start in: `C:\Users\varsh\OneDrive\Desktop\project`
6. Conditions Tab:
   - Uncheck "Start the task only if the computer is on AC power"
7. Settings Tab:
   - Check "Run task as soon as possible after a scheduled start is missed"
   - Check "If the task fails, restart every: 1 minute"

### For Celery Beat:
1. Create another task with same settings but:
   - Name: "ExpiryTracker Celery Beat"
   - Program/script: `C:\Users\varsh\OneDrive\Desktop\project\start_celery_beat.bat`

## Step 3: Test the Setup
1. Run both batch files manually first to ensure they work
2. Check Windows Task Scheduler to verify tasks are created
3. Restart computer to test automatic startup

## Alternative: Manual Testing
While developing, you can run these commands in separate terminals:
```bash
# Terminal 1 - Celery Worker
celery -A expirytracker worker --loglevel=info

# Terminal 2 - Celery Beat Scheduler
celery -A expirytracker beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Troubleshooting
- Check Windows Event Viewer for task errors
- Verify virtual environment path in batch files
- Ensure Redis is running (if using Redis as broker)
- Check Celery logs for detailed error messages

## Current Status
- ✅ Manual reminders work: `python manage.py send_expiry_reminders`
- ✅ Automated scheduling set up: Daily reminders configured
- ✅ Batch files created for background execution
- ⏳ Windows Task Scheduler configuration needed for 24/7 operation
