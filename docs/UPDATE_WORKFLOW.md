# GitHub Auto-Update Deployment Workflow

This guide explains how to deploy new versions of the Automation Tool using GitHub Releases.

---

## Prerequisites

1. **GitHub Repository** setup with releases enabled
2. **GitHub CLI** installed (optional, for command-line releases)
3. **Build tools** configured (PyInstaller or similar)

---

## Step-by-Step Release Process

### 1. Update Version Number

Edit `version.json` in the project root:

```json
{
  "version": "1.0.1",
  "build_date": "2026-01-09",
  "changelog": "Bug fixes and performance improvements"
}
```

**Version Format**: Use semantic versioning `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

---

### 2. Build the Application

#### Option A: Using build script (if available)

```bash
cd d:\MyFolder\Bo\Auto\api\tools\phones
.\build.bat
```

#### Option B: Manual PyInstaller build

```bash
# Install pywebview and dependencies
pip install pywebview keyring requests

# Build .exe
pyinstaller --onefile --name AutomationTool-1.0.1 main.py

# Output: dist/AutomationTool-1.0.1.exe
```

---

### 3. Create GitHub Release

#### Option A: Using GitHub Web UI

1. Go to your repository: `https://github.com/YourUsername/AutomationToolPhones`
2. Click **Releases** → **Draft a new release**
3. Fill in release details:
   - **Tag version**: `v1.0.1` (must match version.json)
   - **Release title**: `Version 1.0.1`
   - **Description**: Copy changelog from version.json
4. Upload `.exe` file: `dist/AutomationTool-1.0.1.exe`
5. Click **Publish release**

#### Option B: Using GitHub CLI

```bash
# Create release and upload .exe
gh release create v1.0.1 \
  --title "Version 1.0.1" \
  --notes "Bug fixes and performance improvements" \
  dist/AutomationTool-1.0.1.exe
```

---

### 4. Verify Release

1. Go to **Releases** page on GitHub
2. Verify:
   - Tag version matches `version.json`
   - `.exe` file is attached
   - Download URL is accessible

---

### 5. Users Auto-Update

**Automatic Process** (no manual intervention needed):

1. User opens app → App checks GitHub API on startup
2. If new version found → "Update Available" button appears in Sidebar
3. User clicks button → Modal shows changelog
4. User clicks "Download & Install" → App downloads new .exe
5. App replaces old file → Restarts automatically

---

## Configuration

### GitHub Repository Settings

1. **Repository Name**: Must match `UpdateManager` configuration in `update_manager.py`:

   ```python
   github_owner = "YourUsername"
   github_repo = "AutomationToolPhones"
   ```

2. **Public vs Private Repo**:
   - **Public**: No authentication needed
   - **Private**: Requires Personal Access Token (advanced setup)

---

## Troubleshooting

### "No releases found" error

- ✅ Check repository name in `update_manager.py`
- ✅ Verify release is published (not draft)
- ✅ Ensure tag starts with `v` (e.g., `v1.0.1`)

### "No .exe file found" error

- ✅ Upload `.exe` file to release assets
- ✅ File must have `.exe` extension

### GitHub API rate limit

- Free tier: 60 requests/hour (unauthenticated)
- Authenticated: 5000 requests/hour
- Solution: Add authentication token (advanced)

---

## Best Practices

### Testing Before Release

1. **Test locally** with a dummy release
2. **Verify download URL** is accessible
3. **Test update process** on a separate PC

### Version Strategy

- **Patch releases** (1.0.1 → 1.0.2): Bug fixes
- **Minor releases** (1.0.0 → 1.1.0): New features
- **Major releases** (1.0.0 → 2.0.0): Breaking changes

### Rollback Plan

If update fails:

1. User can manually download previous version
2. Keep previous releases published
3. Update `version.json` to previous version

---

## Advanced: Private Repository Setup

If using a private repo:

1. **Create Personal Access Token**:

   - GitHub → Settings → Developer Settings → Personal Access Tokens
   - Scope: `repo` (full control)

2. **Update `update_manager.py`**:

   ```python
   headers = {
       "Authorization": f"token {YOUR_GITHUB_TOKEN}"
   }
   response = requests.get(url, headers=headers)
   ```

3. **Securely store token** (don't commit to repo!)

---

## Support

For issues, contact: [your-email@example.com]

Or open an issue on GitHub: `https://github.com/YourUsername/AutomationToolPhones/issues`
