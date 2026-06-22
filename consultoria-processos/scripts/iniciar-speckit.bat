@echo off
setlocal

REM ============================================================
REM iniciar-speckit.bat
REM
REM Inicializa o Spec Kit no WORK_DIR.
REM Instala o specify-cli automaticamente se nao estiver presente.
REM
REM Uso:
REM   iniciar-speckit.bat "<WORK_DIR>"
REM ============================================================

if "%~1"=="" (
    echo ERRO: Informe o WORK_DIR como primeiro argumento.
    echo Uso: iniciar-speckit.bat "C:\caminho\do\projeto"
    exit /b 1
)

set "WORK_DIR=%~1"

REM Necessario para evitar UnicodeEncodeError no Windows com o banner do Rich
set PYTHONUTF8=1
set NO_COLOR=1

REM ── Verifica se specify esta instalado ─────────────────────
where specify >nul 2>&1
if errorlevel 1 (
    echo [INFO] specify-cli nao encontrado. Instalando via uv...
    uv tool install specify-cli
    if errorlevel 1 (
        echo ERRO: Falha ao instalar specify-cli.
        echo Verifique se o uv esta instalado: uv --version
        exit /b 1
    )
    echo [OK] specify-cli instalado com sucesso.
) else (
    echo [OK] specify-cli ja instalado.
)

REM ── Verifica se ja foi inicializado ────────────────────────
if exist "%WORK_DIR%\.cursor\skills\speckit-specify\SKILL.md" (
    echo [INFO] Spec Kit ja inicializado em %WORK_DIR%.
    exit /b 0
)

REM ── Inicializa no WORK_DIR ──────────────────────────────────
echo Inicializando Spec Kit em: %WORK_DIR%

pushd "%WORK_DIR%"
specify init --here --integration cursor-agent --force
set INIT_ERR=%ERRORLEVEL%
popd

if %INIT_ERR% neq 0 (
    echo ERRO: Falha ao executar specify init. Codigo: %INIT_ERR%
    exit /b 1
)

echo.
echo [OK] Spec Kit inicializado com sucesso em: %WORK_DIR%

endlocal
