@echo off
setlocal
title 热词系统 - 自动化测试

echo ========================================================
echo        正在准备测试环境...
echo ========================================================

:: 1. 检查并创建/激活虚拟环境 (逻辑同 run.bat)
if not exist venv (
    echo [系统] 未检测到虚拟环境，正在创建...
    python -m venv venv
)
call venv\Scripts\activate.bat

:: 2. 确保安装了 pytest
pip install pytest >nul 2>&1

:: 3. 运行测试
echo ========================================================
echo        开始运行 pytest 单元测试...
echo ========================================================

:: -v 显示详细信息
:: --disable-warnings 隐藏烦人的警告信息
python -m pytest -v --disable-warnings

if %errorlevel% equ 0 (
    echo.
    echo [成功] 所有测试用例通过！恭喜！
    color 0A
) else (
    echo.
    echo [失败] 测试未通过，请检查代码。
    color 0C
)

echo.
pause
deactivate