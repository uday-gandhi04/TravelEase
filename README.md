# TravelEase

A simple travel booking web application built with Django that allows users to explore travel options (flights, trains, buses), book tickets, and manage their bookings.

🔗 **Live Demo:** [https://travelease-lslq.onrender.com/](https://travelease-lslq.onrender.com/)

---

## 🚀 Features

- **User Management**
  - Registration, login, and logout using Django’s built-in authentication
  - Profile view and edit with extended fields (phone, address, date of birth)

- **Travel Options**
  - Browse flights, trains, and buses
  - Filter by type, source, destination, and date
  - Pagination (10 items per page)

- **Booking Flow**
  - Select seats and enter passenger details
  - Validation against available seats
  - View current and past bookings
  - Cancel bookings (returns seats to inventory)

- **Admin Interface**
  - Add, edit, and delete travel options and bookings
  - Manage users and their profiles

- **Responsive Frontend**
  - Built with Bootstrap 5 and custom CSS
  - Consistent, mobile-friendly UI

- **Database**
  - MySQL in development (`travel_app` database)
  - PostgreSQL in production (via Render’s PostgreSQL add-on)

- **Extras**
  - Seed script to populate sample travel options
  - Unit tests for core functionality
  - Whitenoise for static file serving

---

## 📦 Tech Stack

- **Backend:** Python 3.11, Django 5.2
- **Frontend:** Django Templates, Bootstrap 5, FontAwesome
- **Database (Development):** MySQL
- **Database (Production):** PostgreSQL
- **Deployment:** Render.com (free tier)
- **Others:**
  - `django-crispy-forms`, `django-widget-tweaks`
  - `dj-database-url`, `whitenoise`

---

## 🔧 Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL server (for local development)
- `pipenv` or `venv` for virtual environments

### Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/uday-gandhi04/TravelEase.git
   cd TravelEase
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL Database**
   Create a MySQL database and user:
   ```sql
   CREATE DATABASE travel_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'traveluser'@'localhost' IDENTIFIED BY 's3cret123';
   GRANT ALL PRIVILEGES ON travel_app.* TO 'traveluser'@'localhost';
   FLUSH PRIVILEGES;
   ```
   Update `travel_site/settings.py` if you used different credentials.

5. **Run Migrations and Seed Data**
   ```bash
   python manage.py migrate
   python manage.py seed_travel
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://localhost:8000` to access the application and log in.

### 🧪 Testing
Run the test suite:
```bash
python manage.py test
```

**Test Coverage:**
- Profile update flow
- Booking and cancellation processes
- List view filters and pagination
- Login-required redirects

### 🌐 Deployment on Render
1. Push your branch to GitHub (`backup-recurring-attempt` is the main branch).
2. In the Render dashboard, create a **New Web Service** and connect your GitHub repository.

**Build Command:**
```bash
./render-build.sh
```

**Start Command:**
```bash
gunicorn travel_site.wsgi
```

**Environment Variables in Render:**
- `SECRET_KEY`: Your Django secret key
- `DEBUG`: Set to `False`
- `DATABASE_URL`: PostgreSQL add-on URL (provided by Render)

Deploy the application. It will be live at `https://<your-app-name>.onrender.com`.

---

## 📂 Project Structure
```
TravelEase/
├── travel_site/           # Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── bookings/              # Main app
│   ├── migrations/
│   ├── management/commands/seed_travel.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
│       └── bookings/
│           ├── travel_list.html
│           ├── book_travel.html
│           └── ...
├── requirements.txt
├── render-build.sh
└── README.md
```

---

## 🤝 Contributing
1. Fork and clone the repository.
2. Create a feature branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes and push to the branch.
4. Open a pull request.
5. Ensure all tests pass before submitting.
