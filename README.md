# 🎓 Ultimate Quiz App (W3Schools Style)

A high-performance, interactive, and beautiful full-stack Quiz Application built with **FastAPI** and **React (Vite/TS)**. This app features a "Glassmorphism" UI, an AI Tutor for deep-dive explanations, and a robust scoring system.

🚀 **Live Demo:** [https://week1-hackathon-b4b1.vercel.app](https://week1-hackathon-b4b1.vercel.app)

---

## ✨ Features

- **Dynamic Question Engine**: Choose from 120+ unique questions across HTML, CSS, JavaScript, and Python.
- **AI Tutor Integration**: Stuck on a question? Get a "Deep Dive" explanation from the AI tutor.
- **Glassmorphism UI**: Beautiful, modern, and responsive design with topic-specific color themes.
- **Streak System**: Keep the fire burning! Tracks your correct answer streaks with visual feedback.
- **Final Summary**: Detailed review of all your answers, showing correct vs. wrong with detailed explanations.
- **Quiz Timer**: 30-minute global timer to keep you on your toes.
- **Confetti Celebrations**: High scores are celebrated with high-performance canvas-confetti.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast Python framework for the REST API.
- **Gunicorn/Uvicorn**: Production-grade servers for deployment on Render.
- **Pydantic**: Robust data validation.

### Frontend
- **React 18**: Interactive UI components.
- **Vite**: Ultra-fast build tool.
- **TypeScript**: For type-safe development.
- **Lucide Icons**: Beautiful, lightweight icons.
- **Canvas-Confetti**: High-performance animations.

---

## 📂 Project Structure

```text
├── backend/                # FastAPI source code
│   ├── main.py             # API endpoints and logic
│   ├── requirements.txt    # Python dependencies
│   ├── Procfile            # Render deployment config
│   └── .python-version     # Environment versioning
├── frontend/               # React (Vite) source code
│   ├── src/                # Component logic and styles
│   ├── package.json        # Frontend dependencies
│   ├── vercel.json         # Routing for Vercel
│   └── vite.config.ts      # Vite configuration
└── render.yaml             # Render Blueprint configuration
```

---

## 🚀 Local Setup

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend will be available at `http://localhost:8000`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at `http://localhost:3000`.

---

## 🌐 Deployment

This project is configured for automated deployment:
- **Backend**: Deployed on **Render** via [render.yaml](render.yaml).
- **Frontend**: Deployed on **Vercel** with custom routing in [vercel.json](frontend/vercel.json).

---

## 🤝 Contributing
Feel free to fork this project and add your own questions or features!

---

**Built with ❤️ by Keerthana & Trae IDE**
