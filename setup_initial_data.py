"""
Script to populate database with initial test data.
Usage: python manage.py shell < setup_initial_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.menu.models import Category, Product
from apps.wallet.models import Wallet
from decimal import Decimal

User = get_user_model()


def create_categories() -> None:
    """Create product categories."""
    categories_data = [
        {
            'name': 'Plats Principaux',
            'description': 'Nos délicieux plats traditionnels sénégalais',
            'order': 1
        },
        {
            'name': 'Accompagnements',
            'description': 'Accompagnements pour vos plats',
            'order': 2
        },
        {
            'name': 'Boissons',
            'description': 'Boissons fraîches et naturelles',
            'order': 3
        },
        {
            'name': 'Desserts',
            'description': 'Desserts et douceurs',
            'order': 4
        },
    ]

    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        status = "✓ Créée" if created else "→ Existe déjà"
        print(f"{status}: Catégorie '{category.name}'")


def create_products() -> None:
    """Create products."""
    plats = Category.objects.get(name='Plats Principaux')
    accompagnements = Category.objects.get(name='Accompagnements')
    boissons = Category.objects.get(name='Boissons')
    desserts = Category.objects.get(name='Desserts')

    products_data = [
        # Plats principaux
        {
            'name': 'Thiéboudienne',
            'description': 'Plat national sénégalais à base de riz et poisson',
            'category': plats,
            'price': Decimal('2500.00'),
            'preparation_time': 30,
            'order': 1
        },
        {
            'name': 'Mafé',
            'description': 'Ragoût à la sauce d\'arachide',
            'category': plats,
            'price': Decimal('2000.00'),
            'preparation_time': 25,
            'order': 2
        },
        {
            'name': 'Yassa Poulet',
            'description': 'Poulet mariné aux oignons et citron',
            'category': plats,
            'price': Decimal('2200.00'),
            'preparation_time': 30,
            'order': 3
        },
        {
            'name': 'Thiébou Yapp',
            'description': 'Riz à la viande',
            'category': plats,
            'price': Decimal('2300.00'),
            'preparation_time': 35,
            'order': 4
        },

        # Accompagnements
        {
            'name': 'Riz blanc',
            'description': 'Riz blanc nature',
            'category': accompagnements,
            'price': Decimal('500.00'),
            'preparation_time': 10,
            'order': 1
        },
        {
            'name': 'Attiéké',
            'description': 'Semoule de manioc',
            'category': accompagnements,
            'price': Decimal('800.00'),
            'preparation_time': 5,
            'order': 2
        },
        {
            'name': 'Aloco',
            'description': 'Bananes plantains frites',
            'category': accompagnements,
            'price': Decimal('700.00'),
            'preparation_time': 10,
            'order': 3
        },

        # Boissons
        {
            'name': 'Bissap',
            'description': 'Jus d\'hibiscus glacé',
            'category': boissons,
            'price': Decimal('500.00'),
            'preparation_time': 2,
            'order': 1
        },
        {
            'name': 'Bouye',
            'description': 'Jus de pain de singe',
            'category': boissons,
            'price': Decimal('500.00'),
            'preparation_time': 2,
            'order': 2
        },
        {
            'name': 'Gingembre',
            'description': 'Jus de gingembre frais',
            'category': boissons,
            'price': Decimal('600.00'),
            'preparation_time': 2,
            'order': 3
        },
        {
            'name': 'Eau minérale',
            'description': 'Eau minérale 1.5L',
            'category': boissons,
            'price': Decimal('300.00'),
            'preparation_time': 1,
            'order': 4
        },

        # Desserts
        {
            'name': 'Thiakry',
            'description': 'Couscous au lait et yaourt',
            'category': desserts,
            'price': Decimal('800.00'),
            'preparation_time': 5,
            'order': 1
        },
        {
            'name': 'Salade de fruits',
            'description': 'Fruits frais de saison',
            'category': desserts,
            'price': Decimal('1000.00'),
            'preparation_time': 5,
            'order': 2
        },
    ]

    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            category=prod_data['category'],
            defaults=prod_data
        )
        status = "✓ Créé" if created else "→ Existe déjà"
        print(f"{status}: Produit '{product.name}' - {product.price} FCFA")


def create_test_users() -> None:
    """Create test users with wallets."""
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@restaurant.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'Restaurant',
            'phone_number': '+221771234567',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'client_test',
            'email': 'client@test.com',
            'password': 'client123',
            'first_name': 'Client',
            'last_name': 'Test',
            'phone_number': '+221777654321',
            'telegram_id': 123456789,
            'telegram_username': 'client_test'
        },
        {
            'username': 'cuisinier',
            'email': 'cuisinier@restaurant.com',
            'password': 'cuisinier123',
            'first_name': 'Chef',
            'last_name': 'Cuisine',
            'phone_number': '+221779876543',
            'is_staff': True
        }
    ]

    for user_data in users_data:
        username = user_data.pop('username')
        password = user_data.pop('password')

        user, created = User.objects.get_or_create(
            username=username,
            defaults=user_data
        )

        if created:
            user.set_password(password)
            user.save()

            # Create wallet for non-staff users
            if not user.is_staff or user.is_superuser:
                wallet, _ = Wallet.objects.get_or_create(
                    user=user,
                    defaults={'balance': Decimal('10000.00')}
                )
                print(f"✓ Créé: Utilisateur '{user.username}' avec wallet (10,000 FCFA)")
            else:
                print(f"✓ Créé: Utilisateur staff '{user.username}'")
        else:
            print(f"→ Existe déjà: Utilisateur '{user.username}'")


def main() -> None:
    """Run all setup functions."""
    print("\n" + "="*60)
    print("🚀 INITIALISATION DES DONNÉES")
    print("="*60 + "\n")

    print("📂 Création des catégories...")
    create_categories()

    print("\n🍽️  Création des produits...")
    create_products()

    print("\n👥 Création des utilisateurs de test...")
    create_test_users()

    print("\n" + "="*60)
    print("✅ INITIALISATION TERMINÉE")
    print("="*60)
    print("\n📝 Informations de connexion:")
    print("   Admin: username=admin, password=admin123")
    print("   Client: username=client_test, password=client123")
    print("   Cuisinier: username=cuisinier, password=cuisinier123")
    print("\n🌐 Accès admin: http://127.0.0.1:8000/admin/")
    print("📚 Documentation API: http://127.0.0.1:8000/api/docs/")
    print("\n")


if __name__ == '__main__':
    main()
