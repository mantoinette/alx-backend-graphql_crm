# CRM Project

This is a Django-based CRM project with scheduled jobs using **django-crontab** and **Celery Beat**.  
The project uses **XAMPP (MySQL + Apache)** for the database and server environment.

---

## 🚀 Requirements

- Python 3.10+
- Django 5.x
- XAMPP (Apache + MySQL)
- pip (Python package manager)
- Virtual environment (recommended)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
git clone https://github.com/your-username/alx-backend-graphql_crm.git
cd crm
2. Set Up a Virtual Environment

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Git Bash:
source .venv/Scripts/activate
# On Windows CMD:
.venv\Scripts\activate
3. Install Dependencie
Django>=5.0
celery
django-celery-beat
django-crontab
mysqlclient

Then install:
pip install --upgrade pip
pip install -r requirements.txt

4. Configure Environment Variables
   DEBUG=True
SECRET_KEY=your_secret_key_here
DB_NAME=crm_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306



