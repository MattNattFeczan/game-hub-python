# Python Game Hub

**Pygame** gaming hub featuring three classic games with **10x10 Tic-Tac-Toe** (5-in-a-row Gomoku rules), **Battleship**, and **Minesweeper**. All games include **single-player AI bot opponents**. [web:53][web:94]

## 🎮 Games
- **10x10 Tic-Tac-Toe**: 100-field board, **win by 5-in-a-row** (horizontal/vertical/diagonal) + unbeatable AI [web:97]
- **Battleship**: 10x10 board, random ship placement (1-4 cells) + smart AI opponent
- **Minesweeper**: Grid with hidden mines, flagging/revealing mechanics [memory:2]

## 🚀 Features
- Central hub with game selection menu
- **Single-player vs AI** across all games
- Full Pygame GUI (10x10 grids, sprites, click feedback)
- Strategic AI: Minimax for Tic-Tac-Toe, smart targeting for Battleship [web:97]

## 🛠️ Tech Stack
- pygame==2.6.0        # Graphics, sprites, event loop, 10x10 grid rendering
- numpy==2.1.1         # 10x10 grid arrays, 5-in-row win detection
- random               # Ship/mine generation, random AI moves
- minimax algorithm    # Perfect Tic-Tac-Toe AI (recursive depth-first search)

