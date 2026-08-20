@echo off
title IntelliAudit Launcher
cd /d "%~dp0backend"
start "" http://127.0.0.1:8000/
uvicorn app.main:app
pause
