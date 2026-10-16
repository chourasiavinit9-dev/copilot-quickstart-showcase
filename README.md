# ⚡ Copilot Quickstart Showcase & CYOA Game

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Pytest: 100% Passed](https://img.shields.io/badge/Pytest-6%20Passed-brightgreen?logo=pytest&logoColor=white)](tests/)
[![GitHub Copilot](https://img.shields.io/badge/Pair%20Programmed%20With-GitHub%20Copilot-8A2BE2?logo=githubcopilot&logoColor=white)](https://github.com/features/copilot)

A modern developer portfolio website and cyber-themed command-line "Choose Your Own Adventure" game created as part of the **[GitHub Copilot Quickstart Challenge](https://mlh.link/ghwHF1026-github-copilot-quickstart)**.

---

## 🌟 Highlights

1. **Futuristic Developer Portfolio:**
   - Dark glassmorphism aesthetic (`#07090e` base, cyan/purple mesh gradients).
   - Dynamic typing title, metrics counter, and category-filtered tech stack.
   - **Copilot Prompt Vault:** Interactive gallery with one-click clipboard copying.
   - Zero external libraries or bloated CSS frameworks.

2. **The Hacker's Heist: Breach of the AI Core (CYOA Game):**
   - **Python CLI Edition (`adventure_game.py`):** Rich ANSI colors, typewriter effects, state machine engine, inventory system, and 5 distinct endings.
   - **In-Browser Web Terminal (`index.html`):** Fully playable terminal emulator with interactive commands (`stats`, `inventory`, `choose [1-3]`, `restart`).
   - **Automated Verification:** 100% Pytest suite covering damage formulas, boundary caps, story graph validation, and branch simulations.

---

## 🚀 Quickstart

### 1. Run the Python CLI Adventure Game

```bash
# Navigate to the project directory
cd copilot-quickstart-showcase

# Run the game in your terminal
python3 adventure_game.py
```

### 2. Run the Pytest Test Suite

```bash
# Execute unit tests
python3 -m pytest test_adventure_game.py -v
```

### 3. Preview the Portfolio Website

Simply open `index.html` in your browser:
```bash
open index.html
```
Or start a local lightweight web server:
```bash
python3 -m http.server 8080
# Visit http://localhost:8080 in your browser
```

---

## 📁 Repository Structure

```
copilot-quickstart-showcase/
├── assets/
│   ├── avatar.jpg               # Custom AI developer avatar
│   └── cyber_matrix.jpg         # Cyberpunk AI terminal banner
├── index.html                   # Modern developer portfolio & web terminal
├── style.css                    # Glassmorphic CSS design system & animations
├── script.js                    # Typing effect, filters & terminal game engine
├── adventure_game.py            # Standalone Python CLI CYOA game
├── test_adventure_game.py       # Pytest test suite for game mechanics
├── PROMPTS.md                   # Full catalog of Copilot prompt templates
└── README.md                    # Project overview & documentation
```

---

## 💡 Prompt Engineering with Copilot

For a comprehensive breakdown of the exact prompts and prompt engineering techniques used to design, scaffold, and test this project, see **[PROMPTS.md](PROMPTS.md)**.

---

## 📜 License

Distributed under the MIT License. Built by [Vinit Chaurasia](https://github.com/chourasiavinit9-dev).
