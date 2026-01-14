"""
PC API Client - Handles PC registration with server
"""

import os
import keyring
import requests
from typing import Any, TypedDict
from dotenv import load_dotenv
from interfaces.interface_response import IResponse

# Load environment variables
load_dotenv()

SERVER_API_URL = os.getenv("SERVER_API_URL", "http://localhost:9000/api/v1")

# Keyring service configuration (same as auth bridge)
SERVICE_NAME = "AutomationToolPhones"
TOKEN_KEY = "auth_token"


# DTO Definitions
class CreatePCPhoneDto(TypedDict):
    """
    DTO for creating/registering a PC.
    Matches server's CreatePCDto structure.
    """

    name: str  # PC name (computer name)
    alias: str  # PC alias (default to name)
    machineGUID: str  # Unique machine GUID
    ip: str  # PC IP address
    os: str  # Operating system information


class ApiPC:
    """
    PC API Client - Handles PC registration and management
    """

    def __init__(self) -> None:
        """Initialize PC API client"""
        self.token = None
        self.headers = {
            "Content-Type": "application/json",
        }
        print("🖥️ ApiPC initialized")

    def _get_token(self) -> str:
        """
        Get stored token from keyring.

        Returns:
            str: Token or None if not found
        """
        try:
            token = keyring.get_password(SERVICE_NAME, TOKEN_KEY)
            return token
        except Exception as e:
            print(f"⚠️ Could not get token from keyring: {e}")
            return None

    def create(self, payload: CreatePCDto) -> IResponse:
        """
        Register PC with the server.

        Args:
            payload: CreatePCDto containing PC information

        Returns:
            IResponse with message, statusCode, result, and reasonStatusCode
        """
        try:
            # Get token from keyring
            token = self._get_token()
            if not token:
                return {
                    "message": "Authentication required",
                    "statusCode": 401,
                    "result": None,
                    "reasonStatusCode": "No authentication token found",
                }

            url = f"{SERVER_API_URL}/pc/create"
            cookies = {"token": token}

            print(f"📡 Registering PC with server: {url}")
            print(f"   Name: {payload['name']}")
            print(f"   GUID: {payload['machineGUID']}")
            print(f"   IP: {payload['ip']}")
            print(f"   OS: {payload['os']}")

            response = requests.post(
                url, json=payload, headers=self.headers, cookies=cookies, timeout=10
            )

            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ PC registered successfully")
                return {
                    "message": "PC registered successfully",
                    "statusCode": response.status_code,
                    "result": result.get("metadata"),
                    "reasonStatusCode": "OK",
                }
            else:
                error_msg = f"Server returned status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", error_msg)
                except:
                    pass
                print(f"⚠️ PC registration failed: {error_msg}")
                return {
                    "message": "PC registration failed",
                    "statusCode": response.status_code,
                    "result": None,
                    "reasonStatusCode": error_msg,
                }

        except requests.exceptions.Timeout:
            error_msg = "Request timeout - server not responding"
            print(f"⚠️ PC registration failed: {error_msg}")
            return {
                "message": "PC registration failed",
                "statusCode": 408,
                "result": None,
                "reasonStatusCode": error_msg,
            }
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error - cannot reach server"
            print(f"⚠️ PC registration failed: {error_msg}")
            return {
                "message": "PC registration failed",
                "statusCode": 503,
                "result": None,
                "reasonStatusCode": error_msg,
            }
        except Exception as e:
            error_msg = str(e)
            print(f"❌ PC registration error: {error_msg}")
            return {
                "message": "PC registration failed",
                "statusCode": 500,
                "result": None,
                "reasonStatusCode": error_msg,
            }


# Singleton instance
api_pc = ApiPC()
