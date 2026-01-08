# 📱 Automation Tool - Phone Manager

Desktop application built with **PyWebView** + **React** + **Python** for mobile automation tasks.

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         React UI (Vite)             │
│    TypeScript + Modern React        │
└──────────────┬──────────────────────┘
               │ window.pywebview.api
               ▼
┌─────────────────────────────────────┐
│      PyWebView Bridge (main.py)     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Python Backend (src/)           │
│  - Services (checkers, handlers)    │
│  - Utils (ADB, automation)          │
│  - Appium automation logic          │
└─────────────────────────────────────┘
```

## 📦 Tech Stack

### Frontend

- **React 19** - UI framework
- **Vite** - Build tool
- **TypeScript** - Type safety

### Backend

- **Python 3.12** - Backend logic
- **PyWebView** - Desktop wrapper
- **Appium** - Mobile automation
- **OpenCV** - Image processing
- **Selenium** - WebDriver

## 🚀 Getting Started

### 1. Setup Python Environment

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup React UI

```bash
cd ui
npm install
```

### 3. Run Development Mode

**Terminal 1 - Start Vite Dev Server:**

```bash
cd ui
npm run dev
```

**Terminal 2 - Start PyWebView:**

```bash
python main.py
```

## 🔧 Development

### Python Backend API

Add methods to `main.py` API class:

```python
class API:
    def your_method(self, param):
        # Your logic here
        return {"success": True, "data": result}
```

### React Frontend

Call Python methods from React:

```typescript
// In your React component
const callPython = async () => {
  const result = await window.pywebview.api.your_method(param);
  console.log(result);
};
```

## 📁 Project Structure

```
phones/
├── src/                    # Python backend
│   ├── services/
│   │   ├── checkers/      # Cronjob checkers
│   │   ├── handlers/      # Task handlers
│   │   └── socials/       # Social platform logic
│   ├── utils/             # Utilities
│   │   ├── UtilAdbs.py   # ADB operations
│   │   └── drive/        # Driver actions
│   ├── constants/         # Constants
│   ├── helpers/          # Helper functions
│   └── packages/         # Custom packages
├── ui/                    # React frontend
│   ├── src/
│   ├── public/
│   └── dist/             # Production build
├── venv/                  # Python virtual env
├── main.py               # Application entry
└── requirements.txt      # Python dependencies
```

## 🏗️ Build for Production

### 1. Build React UI

```bash
cd ui
npm run build
```

### 2. Run Production Mode

```bash
# Disable dev mode in main.py
# os.environ["DEV_MODE"] = "false"
python main.py
```

### 3. Create Executable (Optional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## 🔌 Available Python APIs

- `test_connection()` - Test Python-React bridge
- `get_devices()` - Get ADB device list
- Add more in `main.py` API class...

## 📝 Notes

- **Development**: Runs Vite dev server (hot reload)
- **Production**: Serves built React files from `ui/dist`
- **ADB**: Ensure Android SDK tools are in PATH
- **Appium**: Requires Appium server running for automation

## 🐛 Troubleshooting

**PyWebView not starting:**

- Check if Vite dev server is running on port 5173
- Verify virtual environment is activated

**ADB not found:**

- Add Android SDK platform-tools to system PATH
- Run `adb devices` to verify

**Import errors:**

- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.12.x)
