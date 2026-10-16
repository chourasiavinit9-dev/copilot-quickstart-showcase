# GitHub Copilot Prompt Engineering Handbook
### Building Applications with AI Coding Assistants

This repository was created as part of the **Global Hack Week & GitHub Copilot Quickstart Challenge**. It illustrates how developer prompts translate into production-ready web and CLI applications.

---

## 🧭 Prompting Principles for GitHub Copilot

1. **Role & Context Framing:** Always specify the persona and domain context (e.g., *"Act as a senior frontend architect specializing in vanilla CSS design tokens"*).
2. **Explicit Constraints:** Detail required constraints early (e.g., *"Zero external frontend dependencies, WCAG AA contrast compliance, semantic HTML5, pure CSS variables"*).
3. **Behavioral State Definitions:** Define models and state transitions step-by-step (e.g., *"Represent story nodes as an acyclic directed graph with executable side-effect closures"*).
4. **Test-Driven Prompts:** Prompt for unit tests using the Arrange-Act-Assert (AAA) pattern with negative test cases and boundary conditions.

---

## 📋 Catalog of Prompts Used

### Prompt 1: Portfolio Web Architecture & Visual Aesthetics
```text
Act as a senior front-end design technologist.
Scaffold a modern, futuristic developer portfolio website for Vinit Chaurasia (AI Systems Engineer) using semantic HTML5, modern CSS3, and vanilla JavaScript.

Design Requirements:
- Dark glassmorphism aesthetic with a base background of #07090e and glowing cyan/purple mesh accents
- Sticky glass navbar with status indicator and quick play button
- Hero section with dynamic typing effect, developer avatar with rotating glow ring, metric stat counters, and CTAs
- Interactive skills matrix with real-time category filtering (AI, Web, Backend, DevOps)
- Featured projects showcase with interactive hover states and tags
- A dedicated Copilot Prompt Vault with one-click clipboard copying and toast notifications
- Zero heavy dependencies (no Tailwind, no bulky runtime libraries)
```

### Prompt 2: Command-Line CYOA Game Engine
```text
Create a modular command-line Choose Your Own Adventure game in Python 3 titled 'The Hacker's Heist: Breach of the AI Core'.

Game Logic Requirements:
1. Define a Player class that tracks:
   - name (str)
   - hp (int, 0-100)
   - stealth (int, 0-100)
   - credits (int)
   - inventory (list of str)
   - history of visited nodes
2. Implement methods for take_damage(amount), heal(amount), add_item(item), remove_item(item), and is_alive().
3. Structure the narrative into a dictionary of nodes containing description, options, and optional action callbacks.
4. Support branching decision trees leading to 4 distinct victories (Architect, Ghost, Mercenary, Meltdown) and a game_over condition if HP hits 0.
5. Provide a mock_inputs argument to play_game() to allow automated deterministic unit testing without blocking stdin.
```

### Prompt 3: In-Browser JavaScript Terminal Simulation
```text
Write a browser-based terminal emulator in vanilla JavaScript that mirrors the Python CYOA game engine.
Features needed:
- Retro terminal window styling with macOS control dots (close, minimize, maximize)
- Command parser supporting choices ('1', '2', '3') and utility commands ('help', 'stats', 'inventory', 'clear', 'restart')
- Real-time text rendering with colored spans matching ANSI terminal aesthetics
- Auto-scroll to latest output
- Synchronized player HUD displaying Agent, HP, Stealth, Credits, and Inventory.
```

### Prompt 4: Pytest Unit Test Suite
```text
Write a Pytest test suite for our Python CYOA game adhering to the AAA (Arrange, Act, Assert) testing pattern:
- Test initial player state, default stats, and starting inventory.
- Test damage calculation and boundary conditions (ensure health caps at 100 on heal and floors at 0 on lethal damage).
- Test inventory mechanics (prevent duplicate items, handle item removal).
- Test story graph integrity: ensure every option in non-ending nodes points to an existing node key.
- Test full deterministic walkthrough reaching 'ending_architect'.
- Test full deterministic walkthrough verifying 'game_over' trigger upon lethal damage.
```

---

## 💡 Copilot Best Practices & Tips

- **Use `/explain` in VS Code:** Highlight unfamiliar regular expressions or algorithms to get instant line-by-line breakdowns.
- **Use `/fix` for Lint Errors:** Copilot will propose targeted edits that respect existing indentation and type signatures.
- **Use `/tests` to Generate Edge Cases:** Prompt Copilot with: *"Identify edge cases where player health could underflow or choices could cause unhandled index exceptions."*
- **Iterative Refinement:** Start with the core data structure, verify it, then prompt for UI and styling refinements.
