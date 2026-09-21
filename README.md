# 🚗 خودرومگ (Khodromag)

A modern automotive magazine and blog platform built with **Django 6.1**. Features RTL-first Persian UI, dark theme design, user authentication, and a rich car-focused content management system.

## ✨ Features

- **Dark garage-themed UI** — asphalt surfaces, amber accents, and tail-light red for alerts
- **RTL-first design** — full right-to-left support for Persian readers
- **Responsive layout** — mobile hamburger menu, fluid grids, and smooth transitions
- **User authentication** — register, login, logout with session persistence option
- **Rich post model** — brand, model, year, engine, horsepower, transmission, fuel type, and price fields
- **Auto-slug generation** — unique slugs with collision handling
- **Search functionality** — search across posts by title, brand, or model
- **Pagination** — paginated post listings
- **Comment system** — authenticated users can leave comments on posts
- **Technical specs display** — data sheet cards for each vehicle
- **Related posts** — auto-suggested related content
- **Blueprint hero section** — technical car line-art with grid background

## 🛠 Tech Stack

| Layer       | Technology                                      |
|-------------|------------------------------------------------|
| Backend     | Django 6.1                                      |
| Database    | PostgreSQL (configurable)                       |
| Templates   | Django Template Engine (DTL)                    |
| Frontend    | Custom CSS (CSS Variables), Vanilla JS          |
| Fonts       | Vazirmatn (display), JetBrains Mono (data)     |
| Icons       | Inline SVG                                      |

## 📁 Project Structure

```
django-test/
├── Rome/                  # Django project configuration
│   ├── settings.py        # App config, DB, static/media settings
│   ├── urls.py            # Root URL dispatcher
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── accounts/              # User authentication app
│   ├── forms.py           # RegisterForm (extends UserCreationForm)
│   ├── views.py           # Login, register, logout views
│   └── urls.py            # Auth URL routes
├── posts/                 # Core content app
│   ├── models.py          # Post model with specs & auto-slug
│   ├── views.py           # Post list & detail views
│   └── urls.py            # Post URL routes
├── pages/                 # Static pages app
│   ├── views.py           # Home & about views
│   └── urls.py            # Page URL routes
├── blogger/               # Blogger app (scaffold)
├── templates/             # HTML templates
│   ├── base.html          # Base layout (header, footer, nav)
│   ├── pages/             # Home & about templates
│   ├── posts/             # Post list, detail & search templates
│   └── accounts/          # Login & register templates
├── static/                # Static assets
│   ├── css/style.css      # Full design system (300+ lines)
│   └── js/script.js       # Mobile menu & interactions
├── manage.py
├── .gitignore
└── LICENSE
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/mjaghai/django-test.git
cd django-test

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install django psycopg2-binary

# Configure database in Rome/settings.py (update credentials)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 📦 Database Models

### Post

| Field         | Type                  | Description                    |
|---------------|-----------------------|--------------------------------|
| title         | CharField(200)        | Post title                     |
| slug          | SlugField(220)        | Auto-generated URL slug        |
| author        | ForeignKey(User)      | Post author                    |
| image         | ImageField            | Cover image                    |
| description   | CharField(300)        | Short description for cards    |
| content       | TextField             | Full post body                 |
| category      | CharField(100)        | Post category                  |
| brand         | CharField(100)        | Vehicle brand                  |
| model         | CharField(100)        | Vehicle model                  |
| year          | PositiveIntegerField  | Production year                |
| engine        | CharField(100)        | Engine spec                    |
| horsepower    | PositiveIntegerField  | Power (HP)                     |
| transmission  | ChoiceField           | Manual / Automatic             |
| fuel_type     | ChoiceField           | Petrol / Diesel / Hybrid / EV  |
| price         | PositiveBigInteger    | Price (Toman)                  |
| is_published  | BooleanField          | Published status               |
| created_at    | DateTimeField         | Auto-set on creation           |
| updated_at    | DateTimeField         | Auto-set on update             |

## 🔗 URL Routes

| URL Pattern           | View              | Name            | Description          |
|-----------------------|-------------------|-----------------|----------------------|
| `/`                   | `pages.views.home`| `home`          | Landing page         |
| `/about/`             | `pages.views.about`| `about`        | About page           |
| `/posts/`             | `posts.views.post_list`| `post_list`| All posts            |
| `/posts/<slug>/`      | `posts.views.post_detail`| `post_detail`| Single post      |
| `/accounts/login/`    | `accounts.views.login_view`| `login`| Login page           |
| `/accounts/register/` | `accounts.views.register_view`| `register`| Registration    |
| `/accounts/logout/`   | `accounts.views.logout_view`| `logout`| Logout (POST)   |
| `/admin/`             | Django Admin      | —               | Admin panel          |

## 🎨 Design System

The UI uses a **dark garage palette** with CSS custom properties:

```css
--asphalt-950: #121215    /* Deepest background */
--chalk:       #f2f1ec    /* Primary text */
--steel:       #96959d    /* Secondary text */
--amber:       #ff8c1a    /* Primary accent (turn-signal) */
--tail-red:    #e0303d    /* Alerts/errors only */
```

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ for the Iranian automotive community.
