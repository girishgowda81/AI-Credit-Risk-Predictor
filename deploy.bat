@echo off
echo Deploying AI Credit Risk Prediction System via Docker...

:: Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b
)

echo [1/3] Building system containers...
docker-compose build

echo [2/3] Starting services in detached mode...
docker-compose up -d

echo [3/3] Finalizing deployment...
timeout /t 10 /nobreak > nul

echo.
echo ======================================================
echo  SYSTEM DEPLOYED SUCCESSFULLY!
echo ======================================================
echo  Access Dashboard: http://localhost
echo  Access Backend API: http://localhost:8001
echo  Database Port: 5432
echo ======================================================
echo.
echo To see logs, run: docker-compose logs -f
echo To stop the system, run: docker-compose down
echo.
pause
