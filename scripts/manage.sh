#!/bin/bash
# ==========================================
# Restaurant Chatbot - Gestionnaire Principal
# ==========================================

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction pour afficher le menu
show_menu() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   Restaurant Chatbot - Gestionnaire Principal   ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${GREEN}[1]${NC} 🚀 Quick Start (Installation complete)"
    echo -e "  ${GREEN}[2]${NC} 🐳 Docker - Demarrer"
    echo -e "  ${GREEN}[3]${NC} 🛑 Docker - Arreter"
    echo -e "  ${GREEN}[4]${NC} 📊 Docker - Voir les logs"
    echo -e "  ${GREEN}[5]${NC} 🗄️  Base de donnees - Setup"
    echo -e "  ${GREEN}[6]${NC} 🔄 Base de donnees - Reset"
    echo -e "  ${GREEN}[7]${NC} 🔧 Django - Runserver (local)"
    echo -e "  ${GREEN}[8]${NC} 📝 Django - Shell"
    echo -e "  ${GREEN}[9]${NC} 👤 Django - Creer superuser"
    echo -e "  ${RED}[0]${NC} ❌ Quitter"
    echo ""
    echo -n "  Votre choix: "
}

# ==========================================
# 1. QUICK START
# ==========================================
quick_start() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           Quick Start - Installation            ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo -e "  ${YELLOW}[1/6]${NC} Creation de l'environnement virtuel..."
        python3 -m venv .venv
        if [ $? -ne 0 ]; then
            echo -e "  ${RED}❌ Erreur lors de la creation du venv${NC}"
            read -p "Appuyez sur Entree pour continuer..."
            return
        fi
        echo -e "  ${GREEN}✅ Environnement virtuel cree!${NC}"
    else
        echo -e "  ${YELLOW}[1/6]${NC} ${GREEN}✅ Environnement virtuel existe deja${NC}"
    fi
    echo ""

    # Activate virtual environment
    echo -e "  ${YELLOW}[2/6]${NC} Activation de l'environnement virtuel..."
    source .venv/bin/activate
    echo ""

    # Install dependencies
    echo -e "  ${YELLOW}[3/6]${NC} Installation des dependances..."
    pip install -r requirements.txt -q
    if [ $? -ne 0 ]; then
        echo -e "  ${RED}❌ Erreur lors de l'installation${NC}"
        read -p "Appuyez sur Entree pour continuer..."
        return
    fi
    echo -e "  ${GREEN}✅ Dependances installees!${NC}"
    echo ""

    # Check if .env exists
    if [ ! -f ".env" ]; then
        echo -e "  ${YELLOW}[4/6]${NC} Creation du fichier .env..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "  ${GREEN}✅ Fichier .env cree!${NC}"
            echo -e "  ${YELLOW}⚠️  Veuillez editer .env avec votre configuration${NC}"
            echo ""
            read -p "Appuyez sur Entree pour continuer..."
        else
            echo -e "  ${RED}❌ .env.example introuvable${NC}"
            read -p "Appuyez sur Entree pour continuer..."
            return
        fi
    else
        echo -e "  ${YELLOW}[4/6]${NC} ${GREEN}✅ Fichier .env existe deja${NC}"
    fi
    echo ""

    # Run migrations
    echo -e "  ${YELLOW}[5/6]${NC} Execution des migrations..."
    python manage.py makemigrations
    python manage.py migrate
    if [ $? -ne 0 ]; then
        echo -e "  ${RED}❌ Erreur lors des migrations${NC}"
        read -p "Appuyez sur Entree pour continuer..."
        return
    fi
    echo -e "  ${GREEN}✅ Migrations appliquees!${NC}"
    echo ""

    # Create superuser prompt
    echo -e "  ${YELLOW}[6/6]${NC} Creation du superuser..."
    echo -n "  Voulez-vous creer un superuser maintenant? (o/n) "
    read -r create_super
    if [[ "$create_super" =~ ^[Oo]$ ]]; then
        python manage.py createsuperuser
    fi
    echo ""

    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║            Installation Terminee! ✅             ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  Pour demarrer:"
    echo "  - Django API:  python manage.py runserver"
    echo "  - Docker:      ./scripts/start.sh"
    echo ""
    echo "  URLs:"
    echo "  - Admin:   http://127.0.0.1:8000/admin/"
    echo "  - API:     http://127.0.0.1:8000/api/docs/"
    echo ""
    read -p "Appuyez sur Entree pour continuer..."
}

# ==========================================
# 2. DOCKER START
# ==========================================
docker_start() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║            Demarrage Docker Stack               ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        echo -e "  ${RED}❌ Docker n'est pas en cours d'execution!${NC}"
        echo "  Veuillez demarrer Docker Desktop."
        echo ""
        read -p "Appuyez sur Entree pour continuer..."
        return
    fi

    echo "  Services a demarrer:"
    echo "  - Django REST API (port 8000)"
    echo "  - n8n Workflow (port 5678)"
    echo ""
    echo "  Demarrage en cours..."
    echo ""

    docker-compose up -d --build

    if [ $? -ne 0 ]; then
        echo ""
        echo -e "  ${RED}❌ Erreur lors du demarrage${NC}"
        read -p "Appuyez sur Entree pour continuer..."
        return
    fi

    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║              Services Demarres! ✅               ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  URLs:"
    echo "  - Django API:  http://localhost:8000"
    echo "  - Admin:       http://localhost:8000/admin/"
    echo "  - Swagger:     http://localhost:8000/api/docs/"
    echo "  - n8n:         http://localhost:5678"
    echo ""
    echo "  Login n8n:     admin / admin123"
    echo "  Login Admin:   admin / admin123"
    echo ""
    echo "  Commandes utiles:"
    echo "  - docker-compose logs -f         Voir les logs"
    echo "  - docker-compose ps              Liste des services"
    echo "  - docker-compose down            Tout arreter"
    echo ""

    echo -n "  Voulez-vous voir les logs? (o/n) "
    read -r viewlogs
    if [[ "$viewlogs" =~ ^[Oo]$ ]]; then
        docker-compose logs -f
    else
        read -p "Appuyez sur Entree pour continuer..."
    fi
}

# ==========================================
# 3. DOCKER STOP
# ==========================================
docker_stop() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║              Arret Docker Stack                  ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    docker-compose down

    if [ $? -ne 0 ]; then
        echo -e "  ${RED}❌ Erreur lors de l'arret${NC}"
    else
        echo -e "  ${GREEN}✅ Tous les services ont ete arretes!${NC}"
    fi
    echo ""
    read -p "Appuyez sur Entree pour continuer..."
}

# ==========================================
# 4. DOCKER LOGS
# ==========================================
docker_logs() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                  Logs Docker                     ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  [1] Tous les services"
    echo "  [2] Django API uniquement"
    echo "  [3] n8n uniquement"
    echo "  [0] Retour"
    echo ""
    echo -n "  Votre choix: "
    read -r logchoice

    case $logchoice in
        1) docker-compose logs -f ;;
        2) docker-compose logs -f api ;;
        3) docker-compose logs -f n8n ;;
        0) return ;;
    esac
}

# ==========================================
# 5. DATABASE SETUP
# ==========================================
db_setup() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         Configuration Base de Donnees            ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    source .venv/bin/activate

    echo -e "  ${YELLOW}[1/3]${NC} Creation des migrations..."
    python manage.py makemigrations
    echo ""

    echo -e "  ${YELLOW}[2/3]${NC} Application des migrations..."
    python manage.py migrate
    echo ""

    echo -e "  ${YELLOW}[3/3]${NC} Chargement des donnees initiales..."
    if [ -f "setup_initial_data.py" ]; then
        python manage.py shell < setup_initial_data.py
    else
        echo -e "  ${YELLOW}⚠️  setup_initial_data.py introuvable - ignore${NC}"
    fi
    echo ""

    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║        Base de Donnees Configuree! ✅            ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    read -p "Appuyez sur Entree pour continuer..."
}

# ==========================================
# 6. DATABASE RESET
# ==========================================
db_reset() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║        Reset de la Base de Donnees               ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${RED}⚠️  ATTENTION: Toutes les donnees seront supprimees!${NC}"
    echo ""
    echo -n "  Etes-vous sur? (o/n) "
    read -r confirm
    if [[ ! "$confirm" =~ ^[Oo]$ ]]; then
        return
    fi

    echo ""
    source .venv/bin/activate

    echo "  Arret des processus Django..."
    pkill -f "python.*manage.py" 2>/dev/null
    sleep 2

    echo -e "  ${YELLOW}[1/4]${NC} Suppression de la base de donnees..."
    if [ -f "db.sqlite3" ]; then
        rm -f db.sqlite3
        echo -e "  ${GREEN}✅ Base de donnees supprimee${NC}"
    else
        echo -e "  ${BLUE}ℹ️  Pas de base de donnees trouvee${NC}"
    fi
    echo ""

    echo -e "  ${YELLOW}[2/4]${NC} Creation des migrations..."
    python manage.py makemigrations
    echo ""

    echo -e "  ${YELLOW}[3/4]${NC} Application des migrations..."
    python manage.py migrate
    echo ""

    echo -e "  ${YELLOW}[4/4]${NC} Chargement des donnees initiales..."
    if [ -f "setup_initial_data.py" ]; then
        python manage.py shell < setup_initial_data.py
    fi
    echo ""

    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         Base de Donnees Resetee! ✅              ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    read -p "Appuyez sur Entree pour continuer..."
}

# ==========================================
# 7. RUNSERVER
# ==========================================
runserver() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           Demarrage Serveur Django               ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    source .venv/bin/activate

    echo "  Serveur Django demarre sur http://127.0.0.1:8000"
    echo ""
    echo "  URLs disponibles:"
    echo "  - Admin:   http://127.0.0.1:8000/admin/"
    echo "  - Swagger: http://127.0.0.1:8000/api/docs/"
    echo "  - ReDoc:   http://127.0.0.1:8000/api/redoc/"
    echo ""
    echo "  Appuyez sur Ctrl+C pour arreter"
    echo ""

    python manage.py runserver

    read -p "Appuyez sur Entree pour continuer..."
}

# ==========================================
# 8. SHELL
# ==========================================
shell() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║              Django Shell Python                 ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    source .venv/bin/activate
    python manage.py shell

    read -p "Appuyez sur Entree pour continuer..."
}

# ==========================================
# 9. CREATE SUPERUSER
# ==========================================
createsuperuser() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         Creation d'un Superutilisateur           ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    source .venv/bin/activate
    python manage.py createsuperuser

    read -p "Appuyez sur Entree pour continuer..."
}

# ==========================================
# MAIN LOOP
# ==========================================
main() {
    while true; do
        show_menu
        read -r choice

        case $choice in
            1) quick_start ;;
            2) docker_start ;;
            3) docker_stop ;;
            4) docker_logs ;;
            5) db_setup ;;
            6) db_reset ;;
            7) runserver ;;
            8) shell ;;
            9) createsuperuser ;;
            0)
                clear
                echo ""
                echo "  Merci d'avoir utilise Restaurant Chatbot! 👋"
                echo ""
                sleep 1
                exit 0
                ;;
            *)
                echo ""
                echo -e "  ${RED}❌ Choix invalide!${NC}"
                sleep 1
                ;;
        esac
    done
}

# Lancer le programme
main
