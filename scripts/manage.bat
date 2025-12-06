@echo off
REM ==========================================
REM Restaurant Chatbot - Gestionnaire Principal
REM ==========================================

setlocal enabledelayedexpansion

:menu
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║   Restaurant Chatbot - Gestionnaire Principal   ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  [1] 🚀 Quick Start (Installation complete)
echo  [2] 🐳 Docker - Demarrer
echo  [3] 🛑 Docker - Arreter
echo  [4] 📊 Docker - Voir les logs
echo  [5] 🗄️  Base de donnees - Setup
echo  [6] 🔄 Base de donnees - Reset
echo  [7] 🔧 Django - Runserver (local)
echo  [8] 📝 Django - Shell
echo  [9] 👤 Django - Creer superuser
echo  [0] ❌ Quitter
echo.
set /p choice="  Votre choix: "

if "%choice%"=="1" goto quick_start
if "%choice%"=="2" goto docker_start
if "%choice%"=="3" goto docker_stop
if "%choice%"=="4" goto docker_logs
if "%choice%"=="5" goto db_setup
if "%choice%"=="6" goto db_reset
if "%choice%"=="7" goto runserver
if "%choice%"=="8" goto shell
if "%choice%"=="9" goto createsuperuser
if "%choice%"=="0" goto end

echo.
echo  ❌ Choix invalide!
timeout /t 2 >nul
goto menu

REM ==========================================
REM 1. QUICK START
REM ==========================================
:quick_start
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║           Quick Start - Installation            ║
echo  ╚══════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo  [1/6] Creation de l'environnement virtuel...
    python -m venv .venv
    if errorlevel 1 (
        echo  ❌ Erreur lors de la creation du venv
        pause
        goto menu
    )
    echo  ✅ Environnement virtuel cree!
) else (
    echo  [1/6] ✅ Environnement virtuel existe deja
)
echo.

REM Activate virtual environment
echo  [2/6] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat
echo.

REM Install dependencies
echo  [3/6] Installation des dependances...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo  ❌ Erreur lors de l'installation
    pause
    goto menu
)
echo  ✅ Dependances installees!
echo.

REM Check if .env exists
if not exist ".env" (
    echo  [4/6] Creation du fichier .env...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo  ✅ Fichier .env cree!
        echo  ⚠️  Veuillez editer .env avec votre configuration
        echo.
        pause
    ) else (
        echo  ❌ .env.example introuvable
        pause
        goto menu
    )
) else (
    echo  [4/6] ✅ Fichier .env existe deja
)
echo.

REM Run migrations
echo  [5/6] Execution des migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo  ❌ Erreur lors des migrations
    pause
    goto menu
)
echo  ✅ Migrations appliquees!
echo.

REM Create superuser prompt
echo  [6/6] Creation du superuser...
echo  Voulez-vous creer un superuser maintenant? (o/n)
set /p create_super=
if /i "%create_super%"=="o" (
    python manage.py createsuperuser
)
echo.

echo  ╔══════════════════════════════════════════════════╗
echo  ║            Installation Terminee! ✅             ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  Pour demarrer:
echo  - Django API:  python manage.py runserver
echo  - Docker:      docker-start.bat
echo.
echo  URLs:
echo  - Admin:   http://127.0.0.1:8000/admin/
echo  - API:     http://127.0.0.1:8000/api/docs/
echo.
pause
goto menu

REM ==========================================
REM 2. DOCKER START
REM ==========================================
:docker_start
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║            Demarrage Docker Stack               ║
echo  ╚══════════════════════════════════════════════════╝
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo  ❌ Docker n'est pas en cours d'execution!
    echo  Veuillez demarrer Docker Desktop.
    echo.
    pause
    goto menu
)

echo  Services a demarrer:
echo  - Django REST API (port 8000)
echo  - n8n Workflow (port 5678)
echo.
echo  Demarrage en cours...
echo.

docker-compose up -d --build

if errorlevel 1 (
    echo.
    echo  ❌ Erreur lors du demarrage
    pause
    goto menu
)

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║              Services Demarres! ✅               ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  URLs:
echo  - Django API:  http://localhost:8000
echo  - Admin:       http://localhost:8000/admin/
echo  - Swagger:     http://localhost:8000/api/docs/
echo  - n8n:         http://localhost:5678
echo.
echo  Login n8n:     admin / admin123
echo  Login Admin:   admin / admin123
echo.
echo  Commandes utiles:
echo  - docker-compose logs -f         Voir les logs
echo  - docker-compose ps              Liste des services
echo  - docker-compose down            Tout arreter
echo.

echo  Voulez-vous voir les logs? (o/n)
set /p viewlogs=
if /i "%viewlogs%"=="o" (
    docker-compose logs -f
) else (
    pause
)
goto menu

REM ==========================================
REM 3. DOCKER STOP
REM ==========================================
:docker_stop
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║              Arret Docker Stack                  ║
echo  ╚══════════════════════════════════════════════════╝
echo.

docker-compose down

if errorlevel 1 (
    echo  ❌ Erreur lors de l'arret
) else (
    echo  ✅ Tous les services ont ete arretes!
)
echo.
pause
goto menu

REM ==========================================
REM 4. DOCKER LOGS
REM ==========================================
:docker_logs
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║                  Logs Docker                     ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  [1] Tous les services
echo  [2] Django API uniquement
echo  [3] n8n uniquement
echo  [0] Retour
echo.
set /p logchoice="  Votre choix: "

if "%logchoice%"=="1" docker-compose logs -f
if "%logchoice%"=="2" docker-compose logs -f api
if "%logchoice%"=="3" docker-compose logs -f n8n
if "%logchoice%"=="0" goto menu

goto menu

REM ==========================================
REM 5. DATABASE SETUP
REM ==========================================
:db_setup
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║         Configuration Base de Donnees            ║
echo  ╚══════════════════════════════════════════════════╝
echo.

call .venv\Scripts\activate.bat

echo  [1/3] Creation des migrations...
python manage.py makemigrations
echo.

echo  [2/3] Application des migrations...
python manage.py migrate
echo.

echo  [3/3] Chargement des donnees initiales...
if exist "setup_initial_data.py" (
    python manage.py shell < setup_initial_data.py
) else (
    echo  ⚠️  setup_initial_data.py introuvable - ignore
)
echo.

echo  ╔══════════════════════════════════════════════════╗
echo  ║        Base de Donnees Configuree! ✅            ║
echo  ╚══════════════════════════════════════════════════╝
echo.
pause
goto menu

REM ==========================================
REM 6. DATABASE RESET
REM ==========================================
:db_reset
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║        Reset de la Base de Donnees               ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  ⚠️  ATTENTION: Toutes les donnees seront supprimees!
echo.
echo  Etes-vous sur? (o/n)
set /p confirm=
if /i not "%confirm%"=="o" goto menu

echo.
call .venv\Scripts\activate.bat

echo  Arret des processus Django...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo  [1/4] Suppression de la base de donnees...
if exist "db.sqlite3" (
    del /F db.sqlite3
    echo  ✅ Base de donnees supprimee
) else (
    echo  ℹ️  Pas de base de donnees trouvee
)
echo.

echo  [2/4] Creation des migrations...
python manage.py makemigrations
echo.

echo  [3/4] Application des migrations...
python manage.py migrate
echo.

echo  [4/4] Chargement des donnees initiales...
if exist "setup_initial_data.py" (
    python manage.py shell < setup_initial_data.py
)
echo.

echo  ╔══════════════════════════════════════════════════╗
echo  ║         Base de Donnees Resetee! ✅              ║
echo  ╚══════════════════════════════════════════════════╝
echo.
pause
goto menu

REM ==========================================
REM 7. RUNSERVER
REM ==========================================
:runserver
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║           Demarrage Serveur Django               ║
echo  ╚══════════════════════════════════════════════════╝
echo.

call .venv\Scripts\activate.bat

echo  Serveur Django demarre sur http://127.0.0.1:8000
echo.
echo  URLs disponibles:
echo  - Admin:   http://127.0.0.1:8000/admin/
echo  - Swagger: http://127.0.0.1:8000/api/docs/
echo  - ReDoc:   http://127.0.0.1:8000/api/redoc/
echo.
echo  Appuyez sur Ctrl+C pour arreter
echo.

python manage.py runserver

pause
goto menu

REM ==========================================
REM 8. SHELL
REM ==========================================
:shell
cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║              Django Shell Python                 ║
echo  ╚══════════════════════════════════════════════════╝
echo.

call .venv\Scripts\activate.bat
python manage.py shell

pause
goto menu

REM ==========================================
REM 9. CREATE SUPERUSER
REM ==========================================
:createsuperuser
cls
echo.
echo  ╔══════════════════════════════════════════════════╝
echo  ║         Creation d'un Superutilisateur           ║
echo  ╚══════════════════════════════════════════════════╝
echo.

call .venv\Scripts\activate.bat
python manage.py createsuperuser

pause
goto menu

REM ==========================================
REM 0. EXIT
REM ==========================================
:end
cls
echo.
echo  Merci d'avoir utilise Restaurant Chatbot! 👋
echo.
timeout /t 2 >nul
exit /b 0
