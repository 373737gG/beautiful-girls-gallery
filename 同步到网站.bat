@echo off
rem ==== One-click sync: git add / commit / push ====
rem ==== Double-click to run. Keep this .bat INSIDE the project folder. ====
rem ==== Phase 1 (below) is ASCII-only by design: chcp 65001 must run
rem ==== before cmd ever reads the CJK bytes in this file, otherwise
rem ==== GBK decoding can swallow newlines and corrupt the script. ====
if /i "%~1"=="run" goto :run
chcp 65001 >nul
cmd /d /c ""%~f0" run"
exit /b %errorlevel%

:run
rem ============================================================
rem  美少女图鉴 - 一键同步到网站（git add / commit / push）
rem  用法：双击运行即可，无需手动输命令。
rem  本脚本必须放在项目目录内（同步到网站.bat）。
rem  技术说明：上半段为纯 ASCII 引导区，先 chcp 65001 再带 run
rem  参数重新调用自身，全文件在 65001 码页下解析，中文零乱码。
rem ============================================================
title 美少女图鉴 - 一键同步到网站

echo.
echo ==============================================
echo    美少女图鉴 - 一键同步到网站
echo ==============================================
echo.

rem ---------- [1/5] 检查 git 是否已安装 ----------
echo [1/5] 检查 git 环境...
where git >nul 2>nul
if errorlevel 1 goto :noGit

rem ---------- [2/5] 进入项目目录（即本脚本所在目录）----------
echo [2/5] 进入项目目录...
cd /d "%~dp0"
if errorlevel 1 goto :noDir
git rev-parse --is-inside-work-tree >nul 2>nul
if errorlevel 1 goto :noRepo
echo        当前目录：%cd%

rem ---------- [3/5] git add . ----------
echo [3/5] 收集所有改动（git add .）...
git add .
if errorlevel 1 goto :addFail

rem ---------- [4/5] git commit ----------
git diff --cached --quiet
if errorlevel 1 goto :doCommit
echo [4/5] 没有新的改动需要提交，跳过 commit。
goto :doPush

:doCommit
echo [4/5] 提交改动（git commit）...
git commit -m "更新图鉴"
if errorlevel 1 goto :commitFail

rem ---------- [5/5] git push ----------
:doPush
echo [5/5] 推送到远程仓库（git push）...
git push
if errorlevel 1 goto :pushFail

echo.
echo ==============================================
echo    [完成] 同步成功！本地改动已推送到网站仓库。
echo ==============================================
echo.
pause
exit /b 0

:noGit
echo.
echo [错误] 未检测到 git！请先安装 Git（https://git-scm.com/）再运行本脚本。
goto :fail

:noDir
echo.
echo [错误] 无法进入项目目录：%~dp0
goto :fail

:noRepo
echo.
echo [错误] 当前目录不是 git 仓库！请先执行 git init 并关联远程仓库。
goto :fail

:addFail
echo.
echo [错误] git add 失败，请查看上方报错信息。
goto :fail

:commitFail
echo.
echo [错误] git commit 失败！
echo        常见原因：没配置 git 用户名和邮箱，请执行下面两条命令：
echo        git config --global user.name "你的名字"
echo        git config --global user.email "你的邮箱"
goto :fail

:pushFail
echo.
echo [错误] git push 失败！
echo        常见原因：网络不通、未关联远程仓库，或远程有新提交需要先执行 git pull。
goto :fail

:fail
echo.
echo ==============================================
echo    [失败] 同步中断，请按上面的提示处理后重试。
echo ==============================================
echo.
pause
exit /b 1
