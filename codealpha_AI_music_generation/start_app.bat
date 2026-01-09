@echo off
echo ==========================================
echo       AI Music Generation Launcher
echo ==========================================
echo.
echo 1. Train LSTM Model
echo 2. Train GAN Model (Experimental)
echo 3. Start Web Interface
echo 4. Generate Music (CLI)
echo 5. Preprocess Data
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting LSTM Training...
    python main.py train-lstm
) else if "%choice%"=="2" (
    echo Starting GAN Training...
    python main.py train-gan
) else if "%choice%"=="3" (
    echo Starting Web App...
    start http://localhost:5000
    python main.py web
) else if "%choice%"=="4" (
    python main.py generate
) else if "%choice%"=="5" (
    python main.py preprocess
) else (
    echo Invalid choice.
)

pause
