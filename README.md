# Django Blog

A simple and clean Django-based blog application.

## Features
- User authentication
- Create, edit, delete posts
- Basic comments
- Responsive design

## Requirements
- Python 3.x
- Django 3.x+

## Installation
```bash
git clone https://github.com/AissaNouacer/Django_blog.git
cd Django_blog

# Create virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
