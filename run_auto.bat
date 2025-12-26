@echo off
setlocal
title 热词分析系统 - 一键启动脚本

echo ========================================================
echo        正在初始化运行环境，请稍候...
echo ========================================================

:: 1. 检查是否安装了 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 并添加到环境变量。
    pause
    exit /b
)

:: 2. 检查是否存在虚拟环境 venv
if not exist venv (
    echo [系统] 检测到首次运行，正在创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 创建虚拟环境失败。
        pause
        exit /b
    )
    echo [系统] 虚拟环境创建成功。
) else (
    echo [系统] 检测到已有虚拟环境，跳过创建。
)

:: 3. 激活虚拟环境
call venv\Scripts\activate.bat

:: 4. 安装/更新依赖 (使用清华源加速)
echo [系统] 正在检查依赖库...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

:: 5. 启动主程序
echo ========================================================
echo        环境准备完毕，系统即将启动！
echo        模式: 交互模式 (Interactive)
echo        提示: 程序运行结束后将自动弹出 Web 图表
echo ========================================================

:: 启动 main.py，参数设为 interactive
python main.py --mode interactive

:: 如果程序异常退出，暂停一下让助教看到错误信息
if %errorlevel% neq 0 (
    echo.
    echo [警告] 程序发生错误或异常退出。
    pause
)

:: 正常结束，取消虚拟环境激活
deactivate