@echo off
title AMR Spectator Dashboard Server
echo ========================================================
echo Starting AMR Decentralized Fleet Spectator Dashboard...
echo ========================================================
cd /d "%~dp0\dashboard"
python server.py
pause
