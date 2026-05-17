@echo off
chcp 65001 >nul
echo ============================================
echo   对账系统 - 一键启动
echo ============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 16+
    pause
    exit /b 1
)

echo [1/4] 检查后端依赖...
cd /d "%~dp0backend"
if not exist "venv" (
    echo   创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo [2/4] 启动后端服务 (端口 8001)...
start "对账系统-后端" cmd /c "python main.py"
cd /d "%~dp0"

echo [3/4] 检查前端依赖...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo   安装前端依赖...
    call npm install
)

echo [4/4] 启动前端服务 (端口 5173)...
start "对账系统-前端" cmd /c "npm run dev"
cd /d "%~dp0"

echo.
echo ============================================
echo   启动完成！
echo   前端: http://localhost:5173
echo   后端: http://localhost:8001
echo   API文档: http://localhost:8001/docs
echo ============================================
echo.
echo 按任意键关闭此窗口（服务将在独立窗口中继续运行）
pause >nul
