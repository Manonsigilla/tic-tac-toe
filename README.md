# 🍺🍷 Tic Tac Toe - Belgium vs France

A modern, animated Tic Tac Toe game built with Pygame, featuring a unique Belgium (beer) vs France (wine) theme with liquid wavy button animations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎮 Game Modes
- **1 Player Mode**: Play against AI with 3 difficulty levels
  - 🟢 **Easy**: Random moves
  - 🟡 **Medium**: Mix of strategic and random moves (50/50)
  - 🔴 **Hard**: Unbeatable AI using minimax-inspired strategy

- **2 Players Mode**: Local multiplayer on the same device

### 🎨 Visual Polish
- **Pastel gradient background** (peach → powder blue)
- **Liquid wavy button animations** with ripple effects on hover
- **Victory fireworks** with particle system
- **Custom icons**: Beer (Belgium/X) and Wine (France/O)
- **Glowing borders** and smooth transitions

### 🔊 Audio
- **Background music** (looping)
- **Sound effects**: Beer click, wine click, UI clicks
- **Volume controls** with interactive sliders
- **Mute toggle** for music and SFX independently

### 📊 Statistics
- **Persistent game history** (JSON-based storage)
- **Pie chart visualization** of wins distribution
- **Track total games, draws, and last played date**
- **Reset stats** option

### ⚙️ Settings
- **Music volume slider** (0-100%)
- **SFX volume slider** (0-100%)
- **Toggle buttons** for quick mute/unmute
- **Smooth, animated UI**

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Pygame 2.0 or higher

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Manonsigilla/tic-tac-toe.git
   cd tic-tac-toe
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

---

## 📁 Project Structure

```
tic-tac-toe/
│
├── main.py                 # Main game file
├── stats.json             # Game statistics (auto-generated)
│
└── assets/
    ├── images/
    │   ├── beer.png       # Belgium/X icon
    │   └── wine.png       # France/O icon
    │
    └── sounds/
        ├── music.wav      # Background music
        ├── beer_click.wav # Beer placement sound
        ├── wine_click.wav # Wine placement sound
        └── click.wav      # UI click sound
```

---

## 🎮 How to Play

### Menu Navigation
1. Launch the game
2. Choose your mode:
   - **1 Player**: Select difficulty (Easy/Medium/Hard)
   - **2 Players**: Play against a friend locally
3. Click **Stats** to view your game history
4. Click the **⚙️ icon** (top-right) to open settings

### Gameplay
- **Belgium (Beer 🍺)** always plays first as **X**
- **France (Wine 🍷)** plays second as **O**
- Click on any empty cell to place your symbol
- First to get 3 in a row (horizontal, vertical, or diagonal) wins!
- Victory triggers fireworks celebration 🎆

### Controls
- **Mouse**: All interactions (click to play, navigate menus)

---

## 🧠 AI Strategy (Hard Mode)

The AI uses a strategic decision tree:

1. **Win**: If AI can win in one move, take it
2. **Block**: If opponent can win next turn, block them
3.  **Center**: Take the center cell if available (position 4)
4. **Corner**: Take a random available corner (0, 2, 6, 8)
5.  **Any**: Take any remaining position

This makes the **Hard** difficulty nearly unbeatable!

---

## 🎨 Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Peach | `#FFBE98` | Top gradient (Belgium side) |
| Powder Blue | `#A8DADC` | Bottom gradient (France side) |
| Turquoise | `#81ECEC` | Active buttons (1P, Easy, Restart) |
| Sky Blue | `#74B9FF` | 2 Players button, France wins |
| Salmon | `#FA7F6F` | France wins, Hard difficulty |
| Butter Yellow | `#FDCB6E` | Belgium wins |
| Midnight Blue | `#34495E` | Text, borders |
| Clouds | `#ECF0F1` | Button backgrounds |

---

## 🌊 Liquid Button Animation

The signature feature of this game is the **liquid wavy button effect**:

- **40-point polygon** creates smooth button perimeter
- **3 superimposed sine waves** for chaotic water ripples
- **Unique seed per button** for varied animations
- **Glow layers** that pulse with the waves
- **Matches the beer/wine theme** ("drunk" visual effect)

```python
# Wave parameters (adjustable in code)
wave1 = math.sin(time * 4.0 + i * 0.5 + seed) * 3      # Fast ripple
wave2 = math.sin(time * 2.0 + i * 0.3 - seed * 0.5) * 4  # Slow wave
wave3 = math.cos(time * 3.0 + i * 0.4 + seed * 0.3) * 2.5 # Circular wave
```

---

## 🐛 Known Issues / Future Improvements

- [ ] Add keyboard shortcuts (ESC to close menus, R to restart)
- [ ] Implement online multiplayer (requires backend)
- [ ] Add more AI difficulties (e. g., "Drunk" mode with random mistakes)
- [ ] Add animation when placing symbols
- [ ] Add "undo last move" feature for 2P mode
- [ ] Localization (French, Dutch for Belgium theme)

---

## 📜 License

This project is licensed under the MIT License. 

```
MIT License

Copyright (c) 2025 Manonsigilla

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
```

---

## 🙏 Acknowledgments

- **Pygame community** for excellent documentation
- **ChatGPT & GitHub Copilot** for development assistance
- **Belgium & France** for the eternal beer vs wine rivalry 🍺🍷

---

## 📧 Contact

**Manonsigilla** - [GitHub Profile](https://github.com/Manonsigilla)

⭐ **Star this repo** if you enjoyed the game! 

---

## 🎯 Development Stats

- **Language**: 100% Python
- **Lines of Code**: ~1,400
- **Features**: 3 AI difficulties, 2 game modes, persistent stats, animated UI
- **Coffee Consumed**: ☕☕☕ (Many!)

---

**Enjoy the game!  May the best beverage win!  🍺🍷**
