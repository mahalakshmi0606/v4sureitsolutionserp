# V4Sure IT Solutions ERP

V4Sure IT Solutions ERP is a complete **Enterprise Resource Planning (ERP)** backend system built using **Flask (Python)**.  
This project provides API endpoints to manage users, departments, attendance, leaves, permissions, tasks, roles, and more.  
It is designed to work with a frontend application for a complete ERP solution.

---

## 🚀 Features

- User Management (CRUD)
- Department & Designation Management
- Attendance Management
- Leave & Permission Requests
- Task & Project Tracking
- Role and Access Control
- JWT Authentication
- Modular REST API Structure

---

## 🛠️ Tech Stack

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- MySQL / SQLite
- REST API Architecture

---

## 📁 Project Structure

```
v4sureitsolutionserp/
│
├── app/
│   ├── auth/
│   ├── users/
│   ├── departments/
│   ├── attendance/
│   ├── permissions/
│   ├── leaves/
│   ├── tasks/
│   └── __init__.py
│
├── migrations/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```
git clone https://github.com/mahalakshmi0606/v4sureitsolutionserp.git
cd v4sureitsolutionserp
```

### 2. Create Virtual Environment

```
python -m venv venv
```

Activate Virtual Environment:

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

Create a database (MySQL or SQLite) and update `config.py`:

Example MySQL connection:

```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/erp_db"
```

Or SQLite:

```
SQLALCHEMY_DATABASE_URI = "sqlite:///erp.db"
```

---

## 🔄 Database Migrations

```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## ▶️ Run the Application

```
python run.py
```

The backend server will run at:

```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints (Examples)

### Authentication
- `POST /api/auth/login` – Login a user

### Users
- `GET /api/users` – List all users
- `POST /api/users` – Create new user
- `PUT /api/users/<id>` – Update user
- `DELETE /api/users/<id>` – Delete user

### Departments
- `GET /api/departments`
- `POST /api/departments`
- `PUT /api/departments/<id>`
- `DELETE /api/departments/<id>`

### Attendance
- `POST /api/attendance`
- `GET /api/attendance`

### Leaves & Permissions
- `POST /api/leaves`
- `POST /api/permissions`
- `GET /api/leaves`
- `GET /api/permissions`

### Tasks
- `GET /api/tasks`
- `POST /api/tasks`

---

## 🔐 Environment Variables (Optional)

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch  
3. Make changes  
4. Commit & push  
5. Open a Pull Request

---

## 👩‍💻 Author

**Mahalakshmi M**  
Full Stack Developer
