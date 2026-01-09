# GitHub Token Configuration

## For Private Repository Access

Create a `.env` file in the project root (d:\MyFolder\Bo\Auto\api\tools\phones\.env):

```bash
# GitHub Personal Access Token for private repo access
GITHUB_TOKEN=ghp_your_token_here
```

## How to Generate GitHub Token

1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "AutomationPhones Update Access"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Paste into `.env` file

## Security

⚠️ **IMPORTANT**: Add `.env` to `.gitignore` to prevent committing the token!

```gitignore
# .gitignore
.env
*.env
GITHUB_TOKEN
```

## Testing

```bash
# Set environment variable (Windows)
$env:GITHUB_TOKEN="ghp_your_token_here"

# Test update check
python -c "from src.bridge.update.update_manager import update_manager; import json; result = update_manager.check_for_updates(); print(json.dumps(result, indent=2))"
```

You should see authentication enabled in logs:

```
🔐 GitHub authentication enabled (private repo access)
🔍 Checking for updates at: https://api.github.com/repos/HaiSonMin/AutomationPhones/releases/latest
```
