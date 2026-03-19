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

:: [1/3] Проверка окружения
if not exist %VENV_NAME% (
    echo [1/3] First run: creating environment...
    python -m venv %VENV_NAME%
) else (
    echo [1/3] Using existing environment...
)

:: Активируем окружение
call %VENV_NAME%\Scripts\activate.bat

:: [2/3] Обновляем pip правильным способом
echo [2/3] Checking pip...
python -m pip install --upgrade pip >nul 2>&1

:: Устанавливаем зависимости
echo Installing dependencies...
python -m pip install -q requests tqdm pygame numpy

:: [3/3] Запуск игры
echo [3/3] Starting game...
python ping_pong_with_AI.py

:: Деактивация
call %VENV_NAME%\Scripts\deactivate.bat >nul 2>&1

echo.
echo Thanks for playing!
pause
