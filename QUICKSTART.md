# 🚀 Quick Start Guide - Login System

## Prerequisites

1. ✅ API Server running on `localhost:9000`
2. ✅ Python venv activated
3. ✅ All dependencies installed

## Running the Application

### Terminal 1: React UI (Vite)

```bash
cd ui
npm run dev
```

Server will start on `http://localhost:5173`

### Terminal 2: Python Backend (PyWebView)

```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Install Python dependencies (first time only)
pip install -r requirements.txt

# Run the app
python main.py
```

## 🔐 Login Flow

1. **PyWebView window opens** → Shows React UI from Vite dev server
2. **Navigate to login page** → Beautiful TailwindCSS form
3. **Enter credentials** → Form validates with Zod
4. **Submit** → React calls `window.pywebview.api.login(username, password)`
5. **Python backend** → Makes HTTP request to `localhost:9000/api/v1/auth/login`
6. **Token received** → Stored securely in Python Keyring
7. **User data** → Saved in Zustand store
8. **Redirect** → Dashboard page

## 🔑 Token Storage Architecture

```
┌─────────────────────────────────────┐
│         React UI (Vite)             │
│    - Zustand (user data only)       │
│    - No token in localStorage       │
└──────────────┬──────────────────────┘
               │ window.pywebview.api
               ▼
┌─────────────────────────────────────┐
│      Python Backend (main.py)       │
│    - Keyring (secure token)         │
│    - API calls to localhost:9000    │
└─────────────────────────────────────┘
```

## 📁 File Structure

```
phones/
├── main.py                    # PyWebView + Auth API
├── requirements.txt           # Python deps (includes keyring)
└── ui/
    ├── .env                   # VITE_API_URL=http://localhost:9000/api/v1
    ├── src/
    │   ├── App.tsx           # Router + Protected Routes
    │   ├── main.tsx          # Entry point
    │   ├── index.css         # TailwindCSS
    │   ├── stores/
    │   │   └── authStore.ts  # Zustand auth state
    │   ├── services/
    │   │   └── authService.ts # PyWebView API wrapper
    │   ├── types/
    │   │   └── pywebview.ts  # TypeScript types
    │   └── pages/
    │       ├── LoginPage.tsx  # Login form
    │       └── DashboardPage.tsx # Dashboard
    └── package.json
```

## 🎯 Key Features

✅ **Secure Token Storage** - Python Keyring (OS-level encryption)
✅ **Beautiful UI** - TailwindCSS with gradients & animations
✅ **Form Validation** - React Hook Form + Zod
✅ **State Management** - Zustand with persistence
✅ **Protected Routes** - React Router with auth checks
✅ **Error Handling** - User-friendly error messages
✅ **Loading States** - Spinner animations
✅ **Auto Redirect** - After login/logout

## 🔧 Python API Methods

Available via `window.pywebview.api`:

- `login(username, password)` - Login and store token
- `logout()` - Clear token and logout
- `is_authenticated()` - Check auth status
- `get_me()` - Get current user from API

## 🎨 UI Components

- **LoginPage** - Gradient background, form validation, error display
- **DashboardPage** - User info, stats cards, logout button
- **ProtectedRoute** - Auth check with loading state
- **PublicRoute** - Redirect if already logged in

## ⚡ Next Steps

1. Run both terminals
2. PyWebView window opens
3. Login with your credentials
4. Token stored securely
5. Dashboard loads
6. Start building your automation features!
