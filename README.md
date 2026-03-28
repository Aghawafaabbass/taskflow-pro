# ✦ TaskFlow Pro
### Professional Django Task Management System

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Aghawafaabbass-181717?style=flat&logo=github&logoColor=white)

> A full-featured, production-ready task management web application built with Django — designed to demonstrate real-world **Full Stack Development** skills for professional job applications.

---

## 👨‍💻 Developer

**Agha Wafa Abbas**
**Full Stack Developer | Lecturer, School of Computing**

| Institution | Location | Email |
|------------|----------|-------|
| University of Portsmouth | Winston Churchill Ave, Southsea, Portsmouth PO1 2UP, UK | agha.wafa@port.ac.uk |
| Arden University | Coventry, United Kingdom | awabbas@arden.ac.uk |
| Pearson | London, United Kingdom | — |
| IVY College of Management Sciences | Lahore, Pakistan | wafa.abbas.lhr@rootsivy.edu.pk |

---

## 🚀 Live Demo

> Deploying on Railway.app — link coming soon

---

## ✨ Features

- 🔐 **Multi-user Authentication** — Register, Login, Logout
- ✅ **Full Task CRUD** — Create, Read, Update, Delete
- 🎯 **4 Priority Levels** — Low, Medium, High, Critical
- 📊 **4 Status Types** — To Do, In Progress, In Review, Done
- 🏷️ **Custom Categories** — Color-coded per user
- 📅 **Due Dates** — With overdue detection
- 🔖 **Tagging System** — Comma-separated tags
- 📌 **Pin Tasks** — Important tasks stay on top
- 🔍 **Search & Filter** — Real-time multi-filter system
- 📈 **Stats Dashboard** — Completion rate, overdue count
- ⚙️ **Django Admin** — Fully configured
- 📱 **Responsive UI** — Works on all devices and browsers

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+ / Django 4.x |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Fonts | Google Fonts (Syne + DM Sans) |
| Auth | Django contrib.auth |
| Admin | Django Admin (customized) |
| Version Control | Git + GitHub |
| Deployment | Gunicorn + Nginx (production ready) |

---

## 🗄️ 1. Entity Relationship Diagram (ERD)

```
┌──────────────┐       ┌──────────────────┐       ┌─────────────────────┐
│     USER     │       │    CATEGORY      │       │        TASK         │
│──────────────│       │──────────────────│       │─────────────────────│
│ id (PK)      │◄──1───│ id (PK)          │       │ id (PK)             │
│ username     │       │ name             │◄──1───│ title               │
│ email        │       │ color (#hex)     │   N   │ description         │
│ password     │       │ user_id (FK)     │       │ user_id (FK)        │
│ is_staff     │       │ created_at       │       │ category_id (FK)    │
└──────┬───────┘       └──────────────────┘       │ priority            │
       │ 1                                         │ status              │
       │ N                                         │ due_date            │
       └───────────────────────────────────────────│ completed           │
                                                   │ is_pinned           │
                                                   │ tags                │
                                                   │ created_at          │
                                                   └─────────────────────┘
```

---

## 🔄 2. Request Sequence Diagram

```
Browser          URL Router       Middleware        View           Database
   │                 │                │               │                │
   │──GET /dashboard─►               │               │                │
   │                 │──route match──►│               │                │
   │                 │               │──auth check───►               │
   │                 │               │               │──Task.filter()──►
   │                 │               │               │◄──queryset──────│
   │◄──────────────── 200 HTML Response ─────────────│                │
   │                 │                │               │                │
   │──POST /task/add─►               │               │                │
   │                 │──route match──►│               │                │
   │                 │               │──CSRF check───►               │
   │                 │               │               │──Task.create()──►
   │                 │               │               │◄──saved─────────│
   │◄──────────────── 302 redirect to /dashboard ────│                │
```

---

## 🏗️ 3. System Architecture

```
┌──────────────────────────────────────────────────────┐
│                   PRODUCTION                          │
│                                                       │
│  Internet                                             │
│     │                                                 │
│     ▼                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐  │
│  │  NGINX   │──►│GUNICORN  │──►│   DJANGO APP     │  │
│  │Port 80   │   │Workers   │   │Views·Models·Auth │  │
│  │SSL/TLS   │   │WSGI      │   └────────┬─────────┘  │
│  └──────────┘   └──────────┘            │             │
│                                         ▼             │
│                                  ┌─────────────┐      │
│                                  │ PostgreSQL  │      │
│                                  └─────────────┘      │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│                   DEVELOPMENT                         │
│                                                       │
│  Browser ──► Django runserver (8000) ──► SQLite       │
└──────────────────────────────────────────────────────┘
```

---

## 📊 4. Task State Machine

```
                    Priority (independent):
         [Low] ──► [Medium] ──► [High] ──► [Critical]

  ┌─────────┐  Start   ┌─────────────┐  Review  ┌───────────┐
  │  To Do  │─────────►│ In Progress │─────────►│ In Review │
  └────▲────┘          └─────────────┘          └─────┬─────┘
       │                                              │ Approve
       │  Reopen                                      ▼
       │                                         ┌─────────┐
       └─────────────────────────────────────────│  Done   │
                                                 └─────────┘
              ↑ Checkbox toggle from ANY state → Done ↑
```

---

## ⚡ 5. URL & API Flow

```
FRONTEND (HTML)             BACKEND (Django Views)
                            
GET  /                  ──► login_view()
GET  /register/         ──► register_view()
GET  /dashboard/        ──► dashboard()  → filters, stats, render
POST /task/add/         ──► add_task()   → Task.create() → redirect
GET  /task/edit/<id>/   ──► edit_task()  → Task.get() → render form
POST /task/edit/<id>/   ──► edit_task()  → task.save() → redirect
GET  /task/delete/<id>/ ──► delete_task()→ task.delete() → redirect
GET  /task/toggle/<id>/ ──► toggle_task()→ flip completed → redirect
GET  /task/pin/<id>/    ──► toggle_pin() → flip is_pinned → redirect
POST /category/add/     ──► add_category()→ Category.create() → redirect
GET  /admin/            ──► Django Admin (superuser only)
```

---

## 📦 Quick Setup

```bash
# 1. Clone
git clone https://github.com/Aghawafaabbass/taskflow-pro.git
cd taskflow-pro

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install
pip install -r requirements.txt

# 4. Database
python manage.py migrate

# 5. Admin user
python manage.py createsuperuser

# 6. Run
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
taskflow-pro/
├── manage.py
├── requirements.txt
├── README.md
├── taskflow_pro/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── todo/
    ├── models.py        ← Task, Category models
    ├── views.py         ← All view functions
    ├── urls.py          ← URL routing
    ├── admin.py         ← Admin config
    └── templates/
        └── todo/
            ├── login.html
            ├── register.html
            ├── dashboard.html
            └── edit_task.html
```

---

## 🔮 Future Enhancements

- [ ] REST API with Django REST Framework (DRF)
- [ ] Email notifications for due tasks
- [ ] Team collaboration — shared task boards
- [ ] Drag-and-drop Kanban board
- [ ] PostgreSQL for production
- [ ] Docker containerization
- [ ] Deploy on Railway.app

---

## 📄 License

MIT License — free to use for learning and portfolio purposes.

---

<div align="center">
<strong>TaskFlow Pro</strong> — Built with Django<br/>
<em>Full Stack Developer · Agha Wafa Abbas</em><br/>
<a href="https://github.com/Aghawafaabbass">github.com/Aghawafaabbass</a>
</div>
