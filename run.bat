@echo off
echo Starting AI Credit Risk Prediction System...

:: Start the Backend Server on Port 8001
start "NexaLend Backend" cmd /k "python -m app.main"

:: Wait for backend to initialize
timeout /t 5 /nobreak > nul

:: Start the React Frontend on Port 3000
echo Starting React Dashboard...
cd frontend
start "NexaLend Frontend" cmd /k "npm run dev"

:: Open the browser to the frontend
timeout /t 5 /nobreak > nul
start http://localhost:3000

echo.
echo Development environment is being launched!
echo Backend: http://127.0.0.1:8001
echo Frontend: http://localhost:3000
echo.
pause
