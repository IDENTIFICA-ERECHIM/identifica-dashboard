@echo off
setlocal

:: Entra na pasta onde este arquivo .bat está localizado
cd /d "%~dp0"

:: Verifica se a rede identifica existe
docker network inspect identifica >nul 2>&1
if errorlevel 1 (
    echo Rede 'identifica' nao encontrada.
    echo Suba o MySQL no identifica-etl primeiro:
    echo docker compose up -d mysql
    exit /b 1
)

:: Constroi e inicia os containers
docker compose up --build -d
if errorlevel 1 exit /b 1

echo.
echo Tentando rodar dashboard...

set "tentativas=0"

:aguardar
curl.exe -fsS http://localhost:8501/_stcore/health >nul 2>&1
if not errorlevel 1 goto pronto

set /a tentativas+=1

if %tentativas% GEQ 60 goto timeout

timeout /t 1 /nobreak >nul
goto aguardar

:timeout
echo.
echo Dashboard nao respondeu em 60s. Logs:
docker compose logs dashboard
set "codigo_saida=1"
goto encerrar

:pronto
echo Dashboard iniciado!
start "" "http://localhost:8501"

docker compose logs -f dashboard
set "codigo_saida=%errorlevel%"

:encerrar
echo.
echo Encerrando containers...
docker compose down

exit /b %codigo_saida
