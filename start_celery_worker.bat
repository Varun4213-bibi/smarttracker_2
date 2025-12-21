@echo off
cd /d "C:\Users\varsh\OneDrive\Desktop\project\expirytracker"
call venv\Scripts\activate.bat
celery -A expirytracker worker --loglevel=info --pool=solo
pause
