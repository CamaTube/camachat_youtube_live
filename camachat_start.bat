@echo off
CD /D %~dp0
start "" "http://localhost:5000"
powershell.exe -Command python312\python.exe camachat.py
