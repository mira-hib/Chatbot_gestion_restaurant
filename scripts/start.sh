#!/bin/bash
# ==========================================
# Restaurant Chatbot - Quick Start
# Script rapide pour demarrer l'application
# ==========================================

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     Restaurant Chatbot - Demarrage Rapide       ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo -e "  ${GREEN}[1]${NC} Demarrer avec Docker (Recommande)"
    echo -e "  ${YELLOW}[2]${NC} Demarrer en mode local (Django uniquement)"
    echo ""
    echo -n "  Votre choix: "
    read -r choice
    echo ""

    if [ "$choice" == "1" ]; then
        # Docker mode
        echo -e "${CYAN}Demarrage Docker...${NC}"
        echo ""

        if ! docker info > /dev/null 2>&1; then
            echo -e "${RED}❌ Docker n'est pas en cours d'execution!${NC}"
            echo "Veuillez demarrer Docker et reessayer."
            exit 1
        fi

        echo "Building and starting containers..."
        docker-compose up -d --build

        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║            Services Demarres! ✅                 ║${NC}"
            echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
            echo ""
            echo "URLs disponibles:"
            echo "  - Django API:  http://localhost:8000"
            echo "  - Admin:       http://localhost:8000/admin/"
            echo "  - Swagger:     http://localhost:8000/api/docs/"
            echo "  - n8n:         http://localhost:5678"
            echo ""
            echo "Logins:"
            echo "  - n8n:    admin / admin123"
            echo "  - Admin:  admin / admin123"
            echo ""
            echo "Commandes utiles:"
            echo "  - docker-compose logs -f     Voir les logs"
            echo "  - docker-compose down        Arreter tout"
            echo "  - ./scripts/manage.sh        Menu complet"
            echo ""

            echo -n "Voulez-vous voir les logs? (o/n) "
            read -r viewlogs
            if [[ "$viewlogs" =~ ^[Oo]$ ]]; then
                docker-compose logs -f
            fi
        else
            echo -e "${RED}❌ Erreur lors du demarrage${NC}"
            exit 1
        fi
    else
        # Local mode
        echo -e "${CYAN}Demarrage en mode local...${NC}"
        echo ""

        # Activate venv
        if [ -d ".venv" ]; then
            source .venv/bin/activate
        else
            echo -e "${YELLOW}⚠️  Environnement virtuel introuvable${NC}"
            echo "Executez d'abord: ./scripts/manage.sh et choisissez [1] Quick Start"
            exit 1
        fi

        echo "Demarrage du serveur Django..."
        echo ""
        echo "URLs disponibles:"
        echo "  - API:     http://127.0.0.1:8000"
        echo "  - Admin:   http://127.0.0.1:8000/admin/"
        echo "  - Swagger: http://127.0.0.1:8000/api/docs/"
        echo ""
        echo "Appuyez sur Ctrl+C pour arreter"
        echo ""

        python manage.py runserver
    fi
else
    # No Docker - local only
    echo -e "${YELLOW}Docker non disponible - demarrage en mode local${NC}"
    echo ""

    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        echo -e "${RED}❌ Environnement virtuel introuvable${NC}"
        echo "Executez d'abord: ./scripts/manage.sh et choisissez [1] Quick Start"
        exit 1
    fi

    echo "Demarrage du serveur Django..."
    echo ""
    echo "URLs disponibles:"
    echo "  - API:     http://127.0.0.1:8000"
    echo "  - Admin:   http://127.0.0.1:8000/admin/"
    echo "  - Swagger: http://127.0.0.1:8000/api/docs/"
    echo ""
    echo "Appuyez sur Ctrl+C pour arreter"
    echo ""

    python manage.py runserver
fi
