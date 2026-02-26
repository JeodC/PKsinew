#!/usr/bin/env python3
"""
external_emulator.py

    If the user does not wish to use the built-in mgba libretro core, they can opt to use their external emulator.
    This script handles the launch skeleton, while providers are collected from the providers folder. For example,
    the SBC handheld firmware ROCKNIX has its own launch control method, which is performed in providers/rocknix.py.
    
    More providers can be added in this way, simply by creating a new provider.py file.
"""

import os
import platform
import inspect
import subprocess
from abc import ABC, abstractmethod

from settings import load_sinew_settings, save_sinew_settings

# --- Provider Interface ---

class EmulatorProvider(ABC):
    @property
    @abstractmethod
    def supported_os(self):
        pass

    @abstractmethod
    def get_command(self, rom_path, core="auto"):
        pass

    @abstractmethod
    def probe(self, distro_id):
        pass

# --- Import providers ---    
from providers import *

# --- Main ExternalEmulator Controller ---

class ExternalEmulator:
    def __init__(self):
        self.process = None
        self.active_provider = None
        self.current_os = platform.system().lower()
        self.distro_id = self._get_linux_distro() if self.current_os == "linux" else None
        
        # Load settings
        current_settings = load_sinew_settings()
        
        # Register Providers
        import providers
        self.providers = [
            cls(current_settings) 
            for name, cls in inspect.getmembers(providers, inspect.isclass)
            if issubclass(cls, EmulatorProvider) 
            and cls is not EmulatorProvider
            and getattr(cls, 'active', False)
        ]
        
        self._detect_environment()
        
    def _get_linux_distro(self):
        if os.path.exists("/etc/os-release"):
            try:
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        if line.startswith('OS_NAME='):
                            return line.split('=')[1].strip().replace('"', '').lower()
            except: pass
        return "generic"

    def _detect_environment(self):
        for provider in self.providers:
            if self.current_os in provider.supported_os:
                if provider.probe(self.distro_id):
                    self.active_provider = provider
                    print(f"[ExternalEmu] Initialized {type(provider).__name__} on {self.current_os}")
                    break

    def launch(self, rom_path, core="auto"):
        if not self.active_provider:
            print(f"[ExternalEmu] No provider for {self.current_os}. Launch failed.")
            return False

        cmd = self.active_provider.get_command(rom_path, core)
        if not cmd: return False

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
            return True
        except Exception as e:
            print(f"[ExternalEmu] Launch Error: {e}")
            return False

    def is_running(self):
        return self.process is not None and self.process.poll() is None