# Python Game Hub

**Pygame** gaming hub featuring three classic games with **10x10 Tic-Tac-Toe** (5-in-a-row Gomoku rules), **Battleship**, and **Minesweeper**. All games include **single-player bot opponents**.

## 🎮 Games

### 🚢 Battleship
**Key features and Co-authors:**
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
      
- **10x10 Tic-Tac-Toe**: 100-field board, **win by 5-in-a-row** (horizontal/vertical/diagonal) + unbeatable AI

## 💣 Minesweeper
* **Author: Weronika Hes**
** Key features:**
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

## 🚀 Features
- Central hub with game selection menu
- **Single-player vs Bot opponent** across all games
- Full Pygame GUI (10x10 grids, sprites, click feedback)
- Strategic bot opponent: Minimax for Tic-Tac-Toe, smart targeting for Battleship

## 🛠️ Tech Stack
- pygame==2.6.1
- numpy==2.1.1
- random
- minimax algorithm
