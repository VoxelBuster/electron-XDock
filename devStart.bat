@echo off
start javaStart.bat
PING localhost -n 2
python electronUI.py
