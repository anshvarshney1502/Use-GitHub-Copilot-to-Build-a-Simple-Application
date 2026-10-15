# GitHub Copilot Prompting & Development Guide

This guide documents the prompt engineering process and iterative conversational development workflows used with **GitHub Copilot** to build the **Chronicles of Aetheria** Choose-Your-Own-Adventure game and portfolio web showcase.

---

## 1. System Architecture & Data Modeling

### Copilot Prompt:
> *"Create a clean Python object-oriented data structure for a command-line Choose-Your-Own-Adventure game. Include a `Player` dataclass with attributes for name, class archetype, health, mana, gold, and inventory list. Define a `StoryNode` and `Choice` class supporting conditional requirements like inventory items and d20 dice checks."*

### Resulting Output:
- Dataclass models for `Player`, `Choice`, and `StoryNode`.
- Serialization methods (`to_dict` and `from_dict`) for persistent save/load capabilities.
- Type-safe branching logic.

---

## 2. Interactive Combat Engine & Dice Mechanics

### Copilot Prompt:
> *"Generate a turn-based combat function in Python between the Player and a Monster. Include actions for physical attack with critical hit chances based on agility, spellcasting consuming mana, drinking health potions from inventory, and fleeing using an agility check."*

### Resulting Output:
- Dynamic turn-based combat loop.
- Critical hit calculations and dodge mechanics.
- Gold and item drop mechanics upon enemy defeat.

---

## 3. Terminal Experience & ANSI Styling

### Copilot Prompt:
> *"Provide a lightweight helper in Python for printing retro typewriter animations with ANSI terminal colors, plus ASCII art banners for titles, weapons, and victory/defeat screens."*

### Resulting Output:
- `Style` class with ANSI color codes.
- `slow_print()` function with typewriter delay.
- Scalable ASCII banners for titles, skulls, and victory goblets.

---

## 4. Web Engine & Dynamic State

### Copilot Prompt:
> *"Convert the Python Choose-Your-Own-Adventure game into a modern, responsive web application using vanilla HTML5, CSS3, and JavaScript. Include a retro cyberpunk terminal theme, live health/mana HUD bars, inventory tags, and a browser-based combat card."*

### Resulting Output:
- Modular `AdventureGame` class in JavaScript.
- Web Audio API synthesizer for retro sound effects.
- `localStorage` persistence matching the Python save file feature.

---

## 5. Automated Unit Tests

### Copilot Prompt:
> *"Write comprehensive Python `unittest` test cases to verify: 1) player damage/healing bounds, 2) inventory addition and consumption, 3) story graph node connectivity (ensuring no dead-end broken links), and 4) JSON save/load state round-trip."*

### Resulting Output:
- 7 rigorous test assertions in `test_adventure.py` validating state boundaries and node references.
