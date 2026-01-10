# PKsinew 🎮

**PKsinew** is a companion app for **Gen 3 Pokémon games** that lets you **track your progress across all 5 GBA games**.  

It helps you:  
- Manage **achievements and rewards**  
- Handle **mass storage & transferring Pokémon between games**  
- Access **mythical rewards**  
- Explore **re-imagined abandoned features** from the original games  

PKsinew supports **Windows, macOS, and Linux**, and works best with a **controller** for seamless gameplay tracking.

💡 **Devlog / Updates:** [Sinew Devlog](https://pksinew.hashnode.dev/pksinew-devlog-index-start-here)  

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Platform](https://img.shields.io/badge/platform-Windows%2FmacOS%2FLinux-lightgrey)  

---

## Table of Contents

1. [Quick Setup](#quick-setup)  
2. [Install Python 3](#install-python-3)  
3. [Install Dependencies](#install-dependencies)  
4. [Prepare the Launcher](#prepare-the-launcher)  
5. [Add ROMs](#add-roms)  
6. [Run the App](#run-the-app)  
7. [First-time In-App Setup](#first-time-in-app-setup)  
8. [Tips & Notes](#tips--notes)  

---

## Quick Setup

Clone the repo:

```bash
git clone https://github.com/Cambotz/PKsinew.git
cd PKsinew

    ⚠️ On older macOS/Linux, HTTPS may fail. Use SSH or bypass SSL when cloning.

Install Python 3

    Windows: Download Python 3

    macOS: Download Python 3

    Linux:

sudo apt install python3 python3-pip

Check installation:

python3 --version

Install Dependencies

pip3 install pillow numpy

    Pillow replaces PIL. Numpy is required for internal calculations in Sinew.

Prepare the Launcher
<details> <summary>Windows</summary>

    Double-click sinew.bat to launch.

</details> <details> <summary>macOS/Linux</summary>

    Make the launcher executable:

chmod +x sinew.bat

    macOS: Right-click sinew.bat → “Always Launch in Terminal”

    Linux: Ensure it’s executable and run from a terminal or create a shortcut

</details>
Add ROMs

    Place your ethically sourced ROMs in the rom folder.

    Ensure the files are in the correct format required by the app.

Run the App

python3 main.py

    Tip: Using a controller is strongly recommended for the best experience.

First-time In-App Setup

    Map your controller buttons

    Build the database and wallpapers

After this, Sinew is ready to play.
Tips & Notes

    Always run the app from the project folder for proper file paths.

    Keep Python packages updated:

pip3 install --upgrade pillow numpy

    For older systems, SSH is recommended to avoid GitHub SSL issues.

    On macOS/Linux, consider using ed25519 keys for SSH.

    This README assumes you are running the latest supported version of Python 3 for your system.

💡 Optional Enhancements

    Add a .command launcher on macOS for double-click convenience

    Organize ROMs into subfolders for easier navigation


---

✅ **How to use this**:  

1. Open **VS Code, Sublime, Atom**, or terminal editor like **nano**.  
2. Create a file named exactly `README.md`.  
3. Paste the contents **as plain text** (don’t use Word/Google Docs).  
4. Save, commit, push — GitHub will render it perfectly.  

---

If you want, I can make a **next-level version** that adds:  

- **Step emojis** (🎯, ⚠️, ✅)  
- **Checkmarks for recommended actions**  
- **Warnings highlighted**  
- Looks like a **professional polished guidebook** for GitHub  

Do you want me to make that version too?