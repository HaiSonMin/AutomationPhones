"""
Phone Setup Center - UI Automator 2 Implementation
Main service that orchestrates all device setup actions
"""

import time
import uiautomator2 as u2
from typing import Optional

# Import all action modules
from actions.setup_language import setup_language
from actions.setup_wifi import setup_wifi
from actions.setup_turn_off_location import turn_off_location
from actions.setup_turnoff_auto_update import turnoff_auto_update
from actions.setup_keyboard import setup_keyboard
from actions.setup_timezone import setup_timezone
from actions.setup_lock_screen import setup_lock_screen


class ServicePhoneSetupCenter:
    def __init__(self, device_key: str):
        self.device_key = device_key
        self.device: Optional[u2.Device] = None

    def connect_device(self) -> bool:
        """Connect to the Android device"""
        try:
            print(f"Connecting to device {self.device_key}...")
            self.device = u2.connect(self.device_key)

            # Verify connection
            device_info = self.device.info
            print(
                f"Connected to device: {device_info.get('brand')} {device_info.get('model')}"
            )
            return True

        except Exception as e:
            print(f"Failed to connect to device: {e}")
            return False

    def execute(self) -> bool:
        """Execute all device setup actions"""
        if not self.connect_device():
            return False

        try:
            print("\n========== Starting Phone Setup ==========")

            # 1. Setup Language
            print("\n---------- Setting up Language ----------")
            if not setup_language(self.device, self.device_key):
                print("Language setup failed")

            # 3. Setup WiFi
            print("\n---------- Setting up WiFi ----------")
            if not setup_wifi(self.device):
                print("WiFi setup failed")

            # 4. Turn off Location
            print("\n---------- Turning off Location ----------")
            if not turn_off_location(self.device):
                print("Location setup failed")

            # 5. Turn off Auto Update
            print("\n---------- Turning off Auto Update ----------")
            if not turnoff_auto_update(self.device):
                print("Auto update setup failed")

            # 6. Setup Keyboard
            print("\n---------- Setting up Keyboard ----------")
            if not setup_keyboard(self.device):
                print("Keyboard setup failed")

            # 7. Setup Timezone
            print("\n---------- Setting up Timezone ----------")
            if not setup_timezone(self.device):
                print("Timezone setup failed")

            # 8. Setup Lock Screen
            print("\n---------- Setting up Lock Screen ----------")
            if not setup_lock_screen(self.device):
                print("Lock screen setup failed")

            # Final steps
            print("\n---------- Finalizing Setup ----------")
            self.device.press("home")
            time.sleep(1)

            # Clear recent apps
            self.device.press("recent")
            time.sleep(1)
            self.device.press("home")

            print("\n========== Device Setup Complete ==========")
            return True

        except Exception as e:
            print(f"Error during setup: {e}")
            return False
