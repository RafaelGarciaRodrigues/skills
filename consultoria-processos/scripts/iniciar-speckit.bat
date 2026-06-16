@echo off
setlocal

REM ============================================================
REM iniciar-speckit.bat
REM
REM Uso:
REM   iniciar-speckit.bat "<WORK_DIR>"
REM
REM Exemplo:
REM   iniciar-speckit.bat "C:\Users\usuario\OneDrive\Projetos\MeuProjeto"
REM
REM Pre-requisito: specify-cli instalado via uv
REM   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
REM ============================================================

if "%~1"=="" (
    echo ERRO: Informe o WORK_DIR como primeiro argumento.
    echo Uso: iniciar-speckit.bat "C:\caminho\do\projeto"
    exit /b 1
)

set "WORK_DIR=%~1"

echo Inicializando Spec Kit em: %WORK_DIR%

specify init "%WORK_DIR%" --integration cursor

if errorlevel 1 (
    echo ERRO: Falha ao executar specify init.
    echo Verifique se o specify-cli esta instalado: specify --version
    exit /b 1
)

echo.
echo Spec Kit inicializado com sucesso.
echo Abra o Cursor na pasta: %WORK_DIR%
echo Em seguida use os comandos /speckit.* no chat.

endlocal
