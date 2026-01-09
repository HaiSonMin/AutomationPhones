"""
Update Manager - GitHub Releases Integration
Checks for updates and manages app updates via GitHub Releases API
"""

import json
import requests
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class UpdateManager:
    """
    Manages application updates via GitHub Releases
    """

    def __init__(
        self,
        github_owner: str = "HaiSonMin",
        github_repo: str = "AutomationPhones",
        github_token: Optional[str] = None,
    ):
        self.github_owner = github_owner
        self.github_repo = github_repo
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"
        self.current_version = self._load_current_version()

        # Log authentication status
        if self.github_token:
            print("🔐 GitHub authentication enabled (private repo access)")
        else:
            print("⚠ No GitHub token - only public repos accessible")

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with optional authentication for private repos"""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
        return headers

    def _load_current_version(self) -> str:
        """Load current version from version.json"""
        try:
            version_file = Path(__file__).parent.parent.parent.parent / "version.json"
            if version_file.exists():
                with open(version_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("version", "0.0.0")
            return "0.0.0"
        except Exception as e:
            print(f"⚠ Failed to load version: {e}")
            return "0.0.0"

    def get_current_version(self) -> Dict[str, Any]:
        """
        Get current app version

        Returns:
            {
                "success": True,
                "version": "1.0.0",
                "build_date": "2026-01-09"
            }
        """
        try:
            version_file = Path(__file__).parent.parent.parent.parent / "version.json"
            if version_file.exists():
                with open(version_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {
                        "success": True,
                        "version": data.get("version", "0.0.0"),
                        "build_date": data.get("build_date", ""),
                        "changelog": data.get("changelog", ""),
                    }
            return {"success": False, "error": "version.json not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_for_updates(self) -> Dict[str, Any]:
        """
        Check GitHub for latest release

        Returns:
            {
                "success": True,
                "has_update": True,
                "current_version": "1.0.0",
                "latest_version": "1.0.1",
                "download_url": "...",
                "changelog": "Bug fixes",
                "release_date": "2026-01-09"
            }
        """
        try:
            # Call GitHub API with authentication
            url = f"{self.api_base}/repos/{self.github_owner}/{self.github_repo}/releases/latest"
            headers = self._get_headers()
            print(f"🔍 Checking for updates at: {url}")

            response = requests.get(url, headers=headers, timeout=10)

            # Handle rate limiting
            if response.status_code == 403:
                return {
                    "success": False,
                    "error": "GitHub API rate limit exceeded. Try again later.",
                }

            # Handle not found
            if response.status_code == 404:
                return {
                    "success": True,
                    "has_update": False,
                    "message": "No releases found on GitHub",
                }

            response.raise_for_status()
            release_data = response.json()

            # Extract version from tag (e.g., "v1.0.1" -> "1.0.1")
            latest_version = release_data.get("tag_name", "").lstrip("v")
            changelog = release_data.get("body", "No changelog provided")
            release_date = release_data.get("published_at", "")

            # Find .exe asset
            download_url = None
            for asset in release_data.get("assets", []):
                if asset.get("name", "").endswith(".exe"):
                    download_url = asset.get("browser_download_url")
                    break

            if not download_url:
                return {
                    "success": False,
                    "error": "No .exe file found in latest release",
                }

            # Compare versions
            has_update = self._compare_versions(self.current_version, latest_version)

            return {
                "success": True,
                "has_update": has_update,
                "current_version": self.current_version,
                "latest_version": latest_version,
                "download_url": download_url,
                "changelog": changelog,
                "release_date": release_date,
            }

        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return {"success": False, "error": f"Network error: {str(e)}"}
        except Exception as e:
            print(f"❌ Error checking updates: {e}")
            return {"success": False, "error": str(e)}

    def _compare_versions(self, current: str, latest: str) -> bool:
        """
        Compare version strings (semantic versioning)
        Returns True if latest > current
        """
        try:
            current_parts = [int(x) for x in current.split(".")]
            latest_parts = [int(x) for x in latest.split(".")]

            # Pad shorter version with zeros
            while len(current_parts) < 3:
                current_parts.append(0)
            while len(latest_parts) < 3:
                latest_parts.append(0)

            return latest_parts > current_parts
        except Exception:
            return False

    def download_and_install_update(self, download_url: str) -> Dict[str, Any]:
        """
        Download update and install

        Args:
            download_url: Direct download URL from GitHub

        Returns:
            {"success": True, "message": "Update installed, restarting..."}
        """
        try:
            print(f"📥 Downloading update from: {download_url}")

            # Download to temp directory
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, "AutomationTool_Update.exe")

            # Download with progress (with auth if private repo)
            headers = self._get_headers()
            response = requests.get(
                download_url, headers=headers, stream=True, timeout=30
            )
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(temp_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        # Print progress
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"📥 Progress: {percent:.1f}%", end="\r")

            print(f"\n✅ Download complete: {temp_file}")

            # Get current exe path
            if getattr(sys, "frozen", False):
                # Running as compiled .exe
                current_exe = sys.executable
            else:
                # Running as Python script (development)
                print("⚠ Running in development mode, skipping installation")
                return {
                    "success": True,
                    "message": "Development mode: Update downloaded but not installed",
                    "temp_file": temp_file,
                }

            # Create update script (batch file to replace exe and restart)
            update_script = os.path.join(temp_dir, "update.bat")
            with open(update_script, "w") as f:
                f.write("@echo off\n")
                f.write("echo Updating application...\n")
                f.write("timeout /t 2 /nobreak >nul\n")  # Wait for app to close
                f.write(f'copy /Y "{temp_file}" "{current_exe}"\n')
                f.write(f'del "{temp_file}"\n')
                f.write(f'start "" "{current_exe}"\n')
                f.write(f'del "%~f0"\n')  # Delete this script

            # Execute update script and exit
            subprocess.Popen(
                update_script,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            print("✅ Update script started, exiting app...")

            return {
                "success": True,
                "message": "Update installed, restarting application...",
            }

        except Exception as e:
            print(f"❌ Error downloading update: {e}")
            return {"success": False, "error": str(e)}


# Singleton instance
update_manager = UpdateManager()
