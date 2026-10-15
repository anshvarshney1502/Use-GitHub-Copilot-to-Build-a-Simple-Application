# ⚔️ Chronicles of Aetheria: The Forgotten Sanctum

[![Tests](https://github.com/anshvarshney1502/Use-GitHub-Copilot-to-Build-a-Simple-Application/actions/workflows/test.yml/badge.svg)](https://github.com/anshvarshney1502/Use-GitHub-Copilot-to-Build-a-Simple-Application/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MLH GHW](https://img.shields.io/badge/MLH-Global%20Hack%20Week-red.svg)](https://mlh.io)
[![Built with Copilot](https://img.shields.io/badge/Built%20with-GitHub%20Copilot-green.svg)](https://docs.github.com/en/copilot)

A feature-rich **Choose Your Own Adventure** application and portfolio showcase built using **GitHub Copilot** prompt engineering for the **MLH Global Hack Week Challenge**: *Use GitHub Copilot to Build a Simple Application*.

---

```
  ___  ____ _____ _   _ _____ ____  ___    _    
 / _ \| ____|_   _| | | | ____|  _ \|_ _|  / \   
| |_| |  _|   | | | |_| |  _| | |_) || |  / _ \  
|  _  | |___  | | |  _  | |___|  _ < | | / ___ \ 
|_| |_|_____| |_| |_| |_|_____|_| \_\___/_/   \_\
   ⚔️  THE FORGOTTEN SANCTUM: AN INTERACTIVE QUEST  ⚔️
```

---

## 🌟 Features

### 🐍 Python Command-Line RPG (`adventure_game.py`)
- **Multiple Archetypes**: Choose between **Warrior**, **Mage**, or **Rogue**, each with tailored attributes (HP, Mana, Strength, Agility, Intelligence).
- **Dynamic Decision Graph**: Over 15 interconnected story nodes, secret passages, and hidden caches.
- **Skill Checks & Dice Rolls**: d20 skill tests based on character stats (Agility for climbing, Intelligence for deciphering runes, Strength for brute force).
- **Turn-Based Combat Engine**: Fight monsters like the *Skeletal Warden* and the dreaded *Obsidian Wyrmling* with physical attacks, critical hits, spells, potion healing, and tactical retreats.
- **Save / Load Persistence**: Easily save progress and restore it at any time (`savegame.json`).
- **Retro ASCII Art & ANSI Colors**: Typewriter effect with styled terminal art and vibrant status monitors.

### 🌐 Modern Web Showcase (`index.html`, `styles.css`, `app.js`)
- **Interactive Browser Game**: Play the entire adventure directly in any web browser.
- **Real-Time HUD**: Dynamic progress bars for Health, Mana, and Enemy HP.
- **Synthesized Retro Audio**: Integrated retro sound effects powered by the Web Audio API (no external asset downloads required).
- **Local Storage Saves**: Save and resume your quest directly from your browser.
- **Responsive Terminal Design**: Clean retro-futuristic theme that adapts seamlessly to desktop and mobile screens.

---

## 🚀 Quick Start

### 1. Run the Python Command-Line Game
No external dependencies required! Uses standard Python 3:

```bash
# Clone the repository
git clone https://github.com/anshvarshney1502/Use-GitHub-Copilot-to-Build-a-Simple-Application.git
cd Use-GitHub-Copilot-to-Build-a-Simple-Application

# Start the adventure
python3 adventure_game.py
```

### 2. Run the Web Application
Simply open `index.html` in your browser, or spin up a local static server:

```bash
# Using Python's built-in HTTP server:
python3 -m http.server 8000
```
Then visit **`http://localhost:8000`** in your browser.

### 3. Run the Automated Tests
```bash
python3 -m unittest test_adventure.py
```

---

## 📂 Project Architecture

```
├── .github/
│   └── workflows/
│       └── test.yml          # GitHub Actions CI workflow
├── adventure_game.py         # Full Python CLI Choose-Your-Own-Adventure game
├── app.js                    # Web edition game engine & Web Audio SFX
├── COPILOT_PROMPTS.md        # Documented GitHub Copilot prompt workflow
├── index.html                # Web game interface & developer portfolio
├── styles.css                # Custom retro-modern styling & responsiveness
├── test_adventure.py         # Python unit tests verifying mechanics & graph
└── README.md                 # Project documentation
```

---

## 🤖 GitHub Copilot Prompting Workflow

This project was built following the official [GitHub Copilot Quickstart Guide](https://docs.github.com/en/copilot/get-started/quickstart-for-using-github-copilot-on-github-com). 

See [COPILOT_PROMPTS.md](COPILOT_PROMPTS.md) for full transcripts of the prompts used, including:
1. **Architecture & Schema Prompts**: Modeling `Player`, `StoryNode`, and `Choice` classes.
2. **Mechanics Prompts**: Implementing turn-based combat, dice rolls, and critical strikes.
3. **Web Conversion Prompts**: Porting state management and game loop logic into JavaScript.
4. **Testing Prompts**: Generating boundary assertions and node graph traversal tests.

---

## 📜 License
Released under the [MIT License](LICENSE).
