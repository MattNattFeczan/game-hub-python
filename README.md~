# Python Game Hub

**Pygame** gaming hub featuring three classic games with **10x10 Tic-Tac-Toe** (5-in-a-row Gomoku rules), **Battleship**, and **Minesweeper**.

## 🎮 Games

## 🚢 Battleship
* **Key features and Co-authors:**
* **Aleksandra Urbańska**
  - **Bot opponent** - mimicking human-like behaviour by switching to targeted strikes after having found a ship and avoiding tiles adjacent to sunken ships.
  - **Visual effects** - particle-based burning ships, infinite water background and a screen shake effect on hit.
  - **Sources and Methodology:**
    - [Tutorial on particles](https://www.youtube.com/watch?v=F69-t33e8tk&t=1s). 
    - Consultation with Gemini regarding list comprehension and data structures (tuples vs lists).
    - To verify the bot's efficiency, a custom test script (consulted with Gemini) was used to simulate 1,000 games and collect the results (which resulted in introducing the **checkerboard shooting pattern** when ships longer than one tile are still available).
      
* **Bartosz Konat**🐀
  - **UI** - interface and its elements.
  - **UX** - dragging, message animations, interaction with game board.
  - **Sources and Methodology:**
    - https://www.pygame.org/docs/
    - https://docs.python.org/3/
      
## ❌ Tic-Tac-Toe 10x10
* **Key features and Co-authors:**
* **Bartłomiej Budziński**
  - **AI Architecture** - Designed and programmed the unbeatable bot using Minimax (depth 4) with alpha-peta pruning and forward pruning (limiting search to best candidates for performance).
  - **Heuristic Logic** - Created board evaluation algorithms (using string matching for patterns like "broken lines" or "open threes/fours") to optimize AI decisions.
  - **Visual Enhancements (HUD)** - Implemented the dynamic sidebar, turn indicators, flashing text prompts ("Player's turn"), fade-out animations for error messages, and last-move highlighting to improve user experience (UX).
  - **Menu Navigation** - Added "Esc" functionality for returning to the main menu.
  - **Sources and Methodology:**
    - https://www.youtube.com/watch?v=l-hh51ncgDI
    - https://docs.python.org/3/
    - https://www.pygame.org/docs/
    - Consultations with Gemini regarding algorithm optimization, Python syntax and Pygame basics

* **Mateusz Feczan**
  - **Core Engine** - Managing the main game loop, game states, move execution, and alternating turns between the player and the bot.
  - **Interactive Grid** - Implementation of the responsive 10x10 board logic, handling mouse input coordinates (including invalid move detection) and rendering the main game window.
  - **Sources and Methodology:**
    -

## 💣 Minesweeper
* **Author: Weronika Hes**
* **Key features:**
  - **Algorithms**
    - DFS for traversing the board
    - post-first click random map initialization, based on the chosen difficulty
  - **Visuals:**
    - minimalist dark-themed UI for better readability
    - custom assets designed specifically for the project
  - **Sources and Methodology:**
    - [Tutorial on buttons](https://www.youtube.com/watch?v=G8MYGDf_9ho)
    - [Pygame documentation](https://www.pygame.org/docs/)
    - [Pixel art website](https://www.pixilart.com/)
    - Consultations with Gemini: assistance with learning Python basics, code formatting and debugging

## 🏠 Menu

* **Author: Maja Pazera**
* **Key features:**
    * **Centralized Navigation** – a unified interface designed for seamless switching between all available game modules (Battleship, Tic-Tac-Toe, Minesweeper).
    * **Procedural Vector Icons** – custom icons for each game, drawn dynamically using Pygame’s drawing functions for a clean and scalable look.
    * **Interactive UI** – dark-themed, modern interface featuring semi-transparent buttons and responsive hover-state animations.
    * **Audio System** – background music integration with a functional "mute" toggle button.
* **Sources and Methodology:**
    * [Pygame documentation](https://www.pygame.org/docs/) – specifically regarding [Surface alpha](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.set_alpha) and [mixer](https://www.pygame.org/docs/ref/mixer.html) modules.
    * [Python documentation](https://docs.python.org/3/)
    * Consultations with Gemini regarding modular code integration, UI component architecture, and optimizing vector-based rendering logic.

## 🚀 Features
- **Central Hub:** Unified menu for easy game selection.
- **Single-player vs Bot:** Challenge the computer in Tic-Tac-Toe and Battleship.
- **Interactive Pygame GUI:** Custom sprites, responsive click feedback, and dynamic grid rendering.
- **Strategic AI:**
  - **Tic-Tac-Toe:** Unbeatable bot using the Minimax algorithm.
  - **Battleship:** Smart targeting strategy.
- **Minesweeper:** Classic mechanics with DFS-based auto-reveal and multiple difficulty levels.

## 🛠️ Tech Stack
- pygame==2.6.1
- numpy==2.1.1
- random
- minimax algorithm
