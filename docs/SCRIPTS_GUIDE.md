# Development Scripts Guide

## Available Scripts

### 1. `build.bat` - Build Application

Packages the application into a standalone `.exe` file.

**Usage:**

```bash
.\build.bat
```

**What it does:**

- ✅ Checks and installs PyInstaller
- ✅ Cleans previous builds
- ✅ Builds React UI (`npm run build`)
- ✅ Creates standalone `.exe` with PyInstaller
- ✅ Includes version.json and UI assets
- ✅ Output: `dist/AutomationTool-{version}.exe`

---

### 2. `push.bat` - Git Commit & Push

Commits all changes and pushes to GitHub.

**Usage:**

```bash
.\push.bat
```

**What it does:**

- ✅ Shows git status
- ✅ Prompts for commit message
- ✅ Adds all files (respects .gitignore)
- ✅ Commits changes
- ✅ Pushes to `hs/main` branch

**Example:**

```
> .\push.bat
Enter commit message: Added auto-update system
[... commits and pushes ...]
```

---

### 3. `release.bat` - Complete Release (RECOMMENDED)

**Full automation:** Build → Commit → Push → GitHub Release

**Usage:**

```bash
.\release.bat
```

**What it does:**

1. ✅ Reads version from `version.json`
2. ✅ Confirms release with user
3. ✅ Builds application (`build.bat`)
4. ✅ Commits with auto-generated message
5. ✅ Pushes to GitHub
6. ✅ Creates GitHub Release (if `gh` CLI installed)
7. ✅ Uploads `.exe` to release

**Example:**

```
> .\release.bat
Current version: 1.0.0
Release version 1.0.0? (y/n): y
[... builds, commits, pushes, creates release ...]
Release v1.0.0 completed!
```

---

## Workflow

### For Regular Development

```bash
# Make your changes...

# Commit and push
.\push.bat
```

### For New Version Release

1. **Update version.json**:

   ```json
   {
     "version": "1.0.1",
     "build_date": "2026-01-09",
     "changelog": "Bug fixes and improvements"
   }
   ```

2. **Run release script**:

   ```bash
   .\release.bat
   ```

3. **Done!** Users will see update notification in app.

---

## Requirements

### Required

- ✅ Python 3.x
- ✅ Node.js & npm (for UI build)
- ✅ Git

### Optional

- GitHub CLI (`gh`) - for automated release creation
  - Install: https://cli.github.com/
  - Alternative: Manual release creation on GitHub web

---

## Troubleshooting

### Build fails

```bash
# Install dependencies
pip install pywebview keyring requests pyinstaller
cd ui
npm install
```

### Push fails

```bash
# Pull first
git pull hs main --rebase

# Then retry
.\push.bat
```

### GitHub CLI not found

- Install from: https://cli.github.com/
- Or create release manually on GitHub web

---

## Git Configuration

**Remote:** `hs` → `https://github.com/HaiSonMin/AutomationPhones.git`  
**Branch:** `main`

To verify:

```bash
git remote -v
git branch
```

---

## Files Generated

```
dist/
└── AutomationTool-{version}.exe  # Standalone executable

build/                             # Temporary build files
*.spec                             # PyInstaller spec (auto-generated)
```

**Note:** `dist/` and `build/` are in `.gitignore` - not committed to repo.
