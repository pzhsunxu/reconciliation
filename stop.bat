@echo off
chcp 65001 >nul
echo ============================================
echo   对账系统 - 停止服务
echo ============================================
echo.

echo [1/2] 停止后端服务 (端口 8001)...
for /f "tokens=2" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do (
    echo   终止进程 %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/2] 停止前端服务 (端口 5173)...
for /f "tokens=2" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    echo   终止进程 %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo 服务已停止。
pause
