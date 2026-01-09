@echo off
set REPO_URL=https://github.com/Varshakaleeswaran/Codealpha_tasks.git
set TARGET_FOLDER=codealpha_AI_music_generation
set SOURCE_DIR=%~dp0

echo ===================================================
echo     AI Music Generator - GitHub Deployer
echo ===================================================
echo.

cd ..
if exist "Codealpha_tasks" (
    echo [!] 'Codealpha_tasks' folder already exists in the parent directory.
    echo     Updating existing repo...
    cd Codealpha_tasks
    git pull
) else (
    echo [*] Cloning Codealpha_tasks repository...
    git clone %REPO_URL%
    cd Codealpha_tasks
)

if not exist "%TARGET_FOLDER%" (
    echo [*] Creating target folder: %TARGET_FOLDER%
    mkdir "%TARGET_FOLDER%"
)

echo [*] Copying project files...
rem Copy everything except git and temp files.
rem Models and Outputs are small enough to include.
robocopy "%SOURCE_DIR%." "%TARGET_FOLDER%" /E /XD ".git" "__pycache__" "venv" "Codealpha_tasks" /XF "*.pyc"

echo.
echo [!] NOTE: Including models and generated output per user request.
echo.

echo [*] Staging changes...
git add .

echo [*] Committing...
git commit -m "Add AI Music Generation Project (codealpha_AI_music_generation)"

echo.
echo [*] Pushing to GitHub...
echo     (You may be asked to sign in)
git push

echo.
echo ===================================================
echo     Done! 🚀
echo ===================================================
pause
