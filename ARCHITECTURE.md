# 🌉 Python-React Bridge Architecture

## Flow

```
┌────────────────────────────────────────────────────────────┐
│                    React UI (Vite)                         │
│                                                            │
│  1. User Login → Axios POST /auth/login → Server           │
│  2. Receive { token, user } from server                    │
│  3. Call: window.pywebview.api.on_login_success(token,user)│
│  4. Update React state                                     │
└───────────────────────┬────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────────┐
│                Python Bridge (main.py)                     │
│                                                            │
│  PythonBridge class exposed via js_api:                    │
│  • on_login_success(token, user) → keyring.set_password()  │
│  • on_logout() → keyring.delete_password()                 │
│  • get_token() → keyring.get_password()                    │
│  • get_current_user() → return stored user                 │
│  • is_authenticated() → check token exists                 │
└───────────────────────┬────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────────┐
│              Python Keyring (OS Secure Storage)            │
│                                                            │
│  Windows: Credential Manager                               │
│  macOS: Keychain                                           │
│  Linux: Secret Service                                     │
└────────────────────────────────────────────────────────────┘
```

## File Structure

```
phones/
├── main.py                      # Entry point - opens UI, exposes bridge
├── src/
│   └── bridge/
│       ├── __init__.py
│       └── auth.py              # Auth handlers with keyring
└── ui/
    └── src/
        ├── services/
        │   └── authService.ts   # API calls + bridge notifications
        ├── lib/
        │   └── axios.ts         # Axios + token interceptor
        └── types/
            └── pywebview.ts     # Bridge types
```

## How to Run

```bash
# Terminal 1 - Start React UI
cd ui
npm run dev

# Terminal 2 - Start Python (opens window with UI)
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Bridge Methods

| Method                          | Called By     | Purpose                    |
| ------------------------------- | ------------- | -------------------------- |
| `on_login_success(token, user)` | React         | Save token to keyring      |
| `on_logout()`                   | React         | Clear token from keyring   |
| `get_token()`                   | React (Axios) | Get token for API requests |
| `get_current_user()`            | React         | Get cached user data       |
| `is_authenticated()`            | React         | Check auth status          |

## Browser Fallback

When testing in browser (without PyWebView), the service falls back to localStorage.
