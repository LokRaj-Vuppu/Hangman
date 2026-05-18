# Hangman 🎯

A full-stack implementation of the classic Hangman word-guessing game. The backend is a REST API built with **Django** and **Django REST Framework**, and the frontend is a **React** single-page application.

---

## Features

- Random word selection served from the Django backend
- Letter-by-letter guessing with win/loss tracking
- REST API communication between React frontend and Django backend
- Game state managed on the backend
- Clean React UI with CSS styling

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django, Django REST Framework |
| Frontend | React, JavaScript, CSS |
| API | REST (JSON) |

---

## Project Structure

```
Hangman/
├── backend/          # Django project
│   ├── manage.py
│   ├── requirements.txt
│   └── ...           # Django apps, API views, URLs
│
└── frontend/
    └── hangman/      # React app
        ├── src/
        ├── public/
        └── package.json
```

---

## Getting Started

### Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API runs at: **http://127.0.0.1:8000/**

### Frontend (React)

```bash
cd frontend/hangman
npm install
npm start
```

App runs at: **http://localhost:3000/**

> Make sure the Django backend is running before starting the frontend.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/word/` | Get a new random word |
| POST | `/api/guess/` | Submit a letter guess |
| GET | `/api/status/` | Get current game state |

*(Update these endpoints to match your actual URLs)*

---

## How to Play

1. A hidden word is shown as blank dashes
2. Click a letter or type to make a guess
3. Correct guesses reveal the letter in the word
4. Wrong guesses draw parts of the hangman figure
5. You win by guessing the word before 6 wrong guesses

---

## Author

**LokRaj Vuppu** — [GitHub](https://github.com/LokRaj-Vuppu)
