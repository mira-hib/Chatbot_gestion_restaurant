"""
Setup script for Restaurant Chatbot API.
"""
from setuptools import setup, find_packages

setup(
    name='restaurant-chatbot-api',
    version='1.0.0',
    description='API Backend pour chatbot de gestion de restaurant',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=5.0.1',
        'djangorestframework>=3.14.0',
        'drf-spectacular>=0.27.1',
        'django-cors-headers>=4.3.1',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'phonenumbers>=8.13.27',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.4',
            'pytest-django>=4.7.0',
            'black>=24.1.1',
            'flake8>=7.0.0',
            'mypy>=1.8.0',
            'django-stubs>=4.2.7',
        ]
    },
    python_requires='>=3.10',
)
