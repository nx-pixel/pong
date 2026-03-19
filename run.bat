@echo off
chcp 65001 >nul
title Pong with AI

SET VENV_NAME=pong_ai_env
SET MODELS_DIR=tables

echo ===== PONG WITH AI =====
echo.

:: Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: [1/4] Проверка окружения
if not exist %VENV_NAME% (
    echo [1/4] First run: creating environment...
    python -m venv %VENV_NAME%
) else (
    echo [1/4] Using existing environment...
)

:: [2/4] Активация окружения
call %VENV_NAME%\Scripts\activate.bat

:: Обновляем pip (исправленная команда)
echo Updating pip...
python -m pip install --upgrade pip

:: Устанавливаем зависимости (одной командой)
echo Installing dependencies...
pip install requests tqdm pygame numpy


:: [3/4] Скачивание моделей
echo [3/4] Скачивание моделей
python download_models.py

:: [4/4] Запуск игры
echo [4/4] Starting game...
python ping_pong_with_AI.py

:: Деактивация
call %VENV_NAME%\Scripts\deactivate.bat >nul 2>&1

echo.
echo Thanks for playing!
pause
