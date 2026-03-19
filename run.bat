@echo off
title Pong with AI

SET VENV_NAME=pong_ai_env
SET MODELS_DIR=tables

echo ===== PONG WITH AI =====
echo.

:: Проверяем Python (быстрая проверка)
python --version >nul 2>&1 || (
    echo [ОШИБКА] Python не установлен!
    pause
    exit /b 1
)

:: [1/3] Быстрая проверка окружения
if not exist %VENV_NAME% (
    echo [1/3] Первый запуск: создание окружения...
    python -m venv %VENV_NAME%
    call %VENV_NAME%\Scripts\activate.bat
    pip install -q --upgrade pip
    pip install -q requests tqdm pygame numpy
) else (
    echo [1/3] Запуск в существующем окружении...
    call %VENV_NAME%\Scripts\activate.bat
)

:: [2/3] Быстрая проверка моделей (только если отсутствуют)
if not exist %MODELS_DIR%\gen_1_q_table_and_params_4901.pkl (
    echo [2/3] Первый запуск: загрузка моделей...
    python download_models.py
) else (
    echo [2/3] Модели готовы
)

:: [3/3] Запуск игры
echo [3/3] Запуск игры...
python ping_pong_with_AI.py

:: Деактивация
call %VENV_NAME%\Scripts\deactivate.bat

echo.
echo Спасибо за игру!
pause