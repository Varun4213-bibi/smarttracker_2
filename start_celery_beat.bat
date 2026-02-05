@echo off
echo ========================================
echo Starting Celery Beat Scheduler
echo Daily Reminders at 8:00 AM IST
echo ========================================
echo.

cd /d "%~dp0expirytracker"

echo Current Directory: %CD%
echo.
echo Starting Celery Beat...
echo Press Ctrl+C to stop
echo.

celery -A expirytracker beat --loglevel=info

pause
