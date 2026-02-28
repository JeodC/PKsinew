#!/usr/bin/env python3

from config import (
    ROMS_DIR,
    SAVES_DIR
)
from enum import StrEnum
import os
import subprocess
from sys import platform
from external_emulator import EmulatorProvider
from settings import save_sinew_settings

class LinuxRetroarchInstallation(StrEnum):
    PACKAGE = "package"
    FLATPAK = "flatpak"


class LinuxRetroarch(EmulatorProvider):
    """
    Checks for either the package "retroarch", the Flatpak org.libretro.retroarch, or the Steam installation of RetroArch, in that order.
    I'm too lazy to setup something like this working on other platforms so that's y'all's problem, sorry.
    """
    
    active = False
    retroarch_command: list[str] | None
    prefInst: LinuxRetroarchInstallation
    config_path: str
    core_path: str
    core_name: str

    @property
    def supported_os(self):
        return ["linux"]

    def __init__(self, sinew_settings, preferredInstallation : LinuxRetroarchInstallation = LinuxRetroarchInstallation.PACKAGE):
        self.settings = sinew_settings
    
        self.prefInst = preferredInstallation

        # These are read by main.py
        self.roms_dir = "/path/to/external/roms"
        self.saves_dir = "/path/to/external/saves"
        
        
        # Initialize internal cache reference
        if "emulator_cache" not in self.settings:
            self.settings["emulator_cache"] = {}
        self.cache = self.settings["emulator_cache"]

    def probe(self):
        """
            determine if a retroarch install exists, and how to open it.
            if there is no install, return false.
        """

        if self.prefInst == LinuxRetroarchInstallation.PACKAGE:
            self.retroarch_command = self._find_package_installation()
            if self.retroarch_command is None:
                self.retroarch_command = self._find_flatpak_installation()

        elif self.prefInst == LinuxRetroarchInstallation.FLATPAK:
            self.retroarch_command = self._find_flatpak_installation()
            if self.retroarch_command is None:
                self.retroarch_command = self._find_package_installation()

        if self.retroarch_command is None: #john travolta meme looking for the retroarch install
            print("[Linux_RE] no install found for Retroarch")
            return False
        
        # find config files
        xdgHome = os.environ["XDG_CONFIG_HOME"] + "/retroarch/retroarch.cfg"
        dotConRetro = "~/.config/retroarch/retroarch.cfg"
        etcRetro = "/etc/retroarch.cfg"

        if os.path.isfile(xdgHome):
            config_path = xdgHome
        elif os.path.isfile(dotConRetro):
            config_path = dotConRetro
        elif os.path.isfile(etcRetro):
            config_path = etcRetro

        if not config_path: #john travolta meme looking for the retroarch.cfg file
            print("[Linux_RE] no config found.")
            return False
        
        #now for the data
        config_file = open(config_path, "r").readlines
        for line in config_file:
            if line.startswith("libretro_directory = "):
                cutline = line[:21]
                if not os.path.isdir(cutline):
                    print("[Linux_RE] no cores directory found")
                    return False
                else:
                    self.core_path = cutline
            if line.startswith("savefile_directory = "):
                cutline = line[:21]
                if not os.path.isdir(cutline):
                    print("[Linux_RE] no saves found. using sinew directory")
                    self.saves_dir = SAVES_DIR

        #TODO i'm genuinely not sure how you're supposed to find where assets are imported from,
        #so we're just using the sinew dir for now
        self.roms_dir = ROMS_DIR

        if not self.core_path or not self.saves_dir:
            print("[Linux_RE] cores or saves directory missing.")
            return False

        return True

    def get_command(self, rom_path, selected_core):
        """
        Return the list of strings representing the shell command 
        to launch the emulator.
        """

        #the full command is 
        #RETROARCH_COMMAND -L CORE_NAME ROM
        
        core_name = self._find_core_name(selected_core)

        command_list = self.retroarch_command
        command_list.append("-L")
        command_list.append(core_name)
        command_list.append(rom_path)

        return command_list

    def get_save_path(self, rom_path):
        """
        Returns the absolute path to the expected save file.
        This is critical for the 'pull-back' logic after the game exits.
        """
        rom_name = os.path.splitext(os.path.basename(rom_path))[0]

        return os.path.join(self.saves_dir, f"{rom_name}{self._get_save_extension()}")

    def _update_sinew_cache(self, key, value):
        """Helper to update persistent settings only when changed."""
        if self.cache.get(key) != value:
            self.cache[key] = value
            save_sinew_settings(self.settings)

    #is RE installed by package? use "which retroarch" and see if it returns a file location
    def _find_package_installation():
        with subprocess.run(["which", "retroarch"], capture_output=True, text=True).stdout as result:
            if os.path.isfile(result):
                return [result]  
        return None

    #is RE installed by flatpak? use "flatpak info org.libretro.Retroarch" and see if it returns an error
    def _find_flatpak_installation():
        with subprocess.run(["flatpak", "info", "org.libretro.Retroarch"], capture_output=True, check=False) as result:
            if result.returnCode == 0:
                return ["flatpak", "run", "org.libretro.Retroarch"]
        return None

    def _find_core_name(self, selected_core):
        #this is an awful implementation but i don't know how cores tell
        #what content they're to be used with or their priority
        #so bollocks to it. cope. seethe. mald.
        cores = os.listdir(self.core_path)

        available_cores = []

        for core_file_name in cores:
            if core_file_name.lower().find("mgba") > -1:
                available_cores.append("mgba")
            if core_file_name.lower().find("vbam") > -1:
                available_cores.append("vbam")
            if core_file_name.lower().find("vba_next") > -1:
                available_cores.append("vba_next")
            if core_file_name.lower().find("gbsp") > -1:
                available_cores.append("gbsp")

        if not len(available_cores):
            return None
        
        if selected_core in available_cores:
            return selected_core
        
        return available_cores[0]

    def _get_save_extension(self):
        #all of the ones i found are .srm instead of .sav
        #keeping the function in case i missed something obvious
        return ".srm"