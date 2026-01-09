# GitHub Repository Setup Guide

This guide explains how to set up your GitHub repository for auto-updates.

---

## Initial Setup

### 1. Create GitHub Repository

1. Go to **github.com** → **New Repository**
2. Repository settings:
   - **Name**: `AutomationToolPhones` (or your preferred name)
   - **Visibility**: Public (recommended) or Private
   - **Initialize**: Don't add README/LICENSE (optional)
3. Click **Create repository**

---

### 2. Configure Repository in Code

Update `update_manager.py` with your repository details:

```python
# File: src/bridge/update/update_manager.py
class UpdateManager:
    def __init__(
        self,
        github_owner: str = "YourGitHubUsername",  # ← Change this
        github_repo: str = "AutomationToolPhones",  # ← Change this
    ):
        # ...
```

---

### 3. Create Initial Release

Before users can update, you need at least one release:

#### Via GitHub Web UI:

1. Go to your repository
2. Click **Releases** → **Create a new release**
3. Fill in:
   - **Tag**: `v1.0.0`
   - **Title**: `Version 1.0.0`
   - **Description**: `Initial release`
4. Upload: `AutomationTool-1.0.0.exe`
5. Click **Publish release**

---

## Repository Structure

```
YourUsername/AutomationToolPhones
├── README.md (optional)
├── .gitignore
└── Releases
    ├── v1.0.0
    │   └── AutomationTool-1.0.0.exe
    ├── v1.0.1
    │   └── AutomationTool-1.0.1.exe
    └── v1.0.2
        └── AutomationTool-1.0.2.exe
```

**Note**: The actual .exe files are stored as **Release Assets**, not in the git repository.

---

## GitHub CLI Setup (Optional)

For faster release creation via command line:

### 1. Install GitHub CLI

Download from: https://cli.github.com/

Or via package manager:

```bash
# Windows (winget)
winget install GitHub.cli

# Homebrew
brew install gh
```

### 2. Authenticate

```bash
gh auth login
```

Follow the prompts to authenticate.

### 3. Test CLI

```bash
# List releases
gh release list

# Create release
gh release create v1.0.1 \
  --title "Version 1.0.1" \
  --notes "Bug fixes" \
  dist/AutomationTool-1.0.1.exe
```

---

## Release Naming Convention

**Tag Format**: `v{MAJOR}.{MINOR}.{PATCH}`

Examples:

- ✅ `v1.0.0` - Correct
- ✅ `v1.2.3` - Correct
- ❌ `1.0.0` - Missing 'v' prefix
- ❌ `v1.0` - Missing patch version

**Why?** The `UpdateManager` strips the 'v' prefix to compare versions.

---

## Testing Your Setup

### 1. Create a Test Release

```bash
# Build app
pyinstaller --onefile --name AutomationTool-Test main.py

# Create release
gh release create v0.0.1-test \
  --title "Test Release" \
  --notes "Test update system" \
  --prerelease \
  dist/AutomationTool-Test.exe
```

### 2. Test API Access

Open Python console:

```python
import requests

# Check latest release
url = "https://api.github.com/repos/YourUsername/AutomationToolPhones/releases/latest"
response = requests.get(url)
print(response.json()['tag_name'])  # Should print: v0.0.1-test
```

### 3. Test in App

1. Start app
2. Check console logs for version check
3. Verify "Update Available" button appears (if version is newer)

---

## Private Repository (Advanced)

If you need a private repository:

### 1. Create Personal Access Token

1. GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Click **Generate new token**
3. Scopes: Select `repo` (full control of private repositories)
4. Click **Generate token**
5. **Copy token** (you won't see it again!)

### 2. Store Token Securely

**Do NOT hardcode in source!** Use environment variables:

```python
# update_manager.py
import os

class UpdateManager:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")  # From environment
        # ...

    def check_for_updates(self):
        headers = {}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        response = requests.get(url, headers=headers)
        # ...
```

### 3. Set Environment Variable

```bash
# Windows
setx GITHUB_TOKEN "ghp_your_token_here"

# Or add to .env file (don't commit!)
```

---

## Repository Settings

### Recommended Settings

1. **Releases**: Enable
2. **Issues**: Enable (for user feedback)
3. **Wiki**: Optional (for documentation)
4. **Discussions**: Optional

### Security

- ✅ Enable **Dependabot alerts**
- ✅ Add `.gitignore` for Python:
  ```
  __pycache__/
  *.pyc
  dist/
  build/
  *.spec
  .env
  ```
- ❌ Never commit: API keys, tokens, passwords

---

## Monitoring

### GitHub API Rate Limits

Check your rate limit:

```bash
curl https://api.github.com/rate_limit
```

- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5000 requests/hour

### Release Analytics

GitHub provides download statistics:

- Repository → Insights → Traffic → Releases

---

## Troubleshooting

### "Repository not found" error

- ✅ Check `github_owner` and `github_repo` in code
- ✅ Verify repository is public (or token provided for private)

### API rate limit exceeded

- ✅ Wait 1 hour for reset
- ✅ Use authentication token
- ✅ Reduce check frequency in app

---

## Next Steps

1. ✅ Create initial release (v1.0.0)
2. ✅ Test update check in app
3. ✅ Document release process for your team
4. ✅ Set up automated build pipeline (optional)

---

**Pro Tip**: Keep your releases organized with clear changelogs. Users appreciate knowing what changed!
