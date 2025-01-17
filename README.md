# NBA Player Guessing Game 🏀

A fun and challenging game where you try to guess NBA players based on their attributes. Similar to Wordle, but for basketball fans! Test your NBA knowledge by guessing players based on their team, position, height, and weight.

## How to Play 🎮

1. A random NBA player is selected as the target
2. Type any NBA player's name in the search box
3. Get feedback on your guess:
   - ✓ = Exact match
   - ↑ = Higher than target
   - ↓ = Lower than target
   - ≈ = Close to target
4. Use the feedback to make better guesses
5. Try to guess the player within 8 attempts!

## Features ⭐

- Complete database of current NBA players (2023-24 season)
- Real-time feedback on guesses
- Visual indicators for attribute comparisons
- Player search autocomplete
- Celebration animations on winning
- Game statistics tracking

## Installation 🛠️

1. Clone the repository:

```bash
git clone https://github.com/yourusername/nba-guessing-game.git
cd nba-guessing-game
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Game 🎯

Start the game with:
```bash
streamlit run app.py
```

Then open your browser and go to http://localhost:8501

## Tech Stack 💻

- Python
- Streamlit
- Pandas
- NumPy

## Data 📊

The game uses current NBA player data including:
- Player names
- Teams
- Positions
- Heights
- Weights

Data is updated for the 2023-24 NBA season.

## Contributing 🤝

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- NBA data from official NBA statistics
- Inspired by Wordle and similar guessing games
- Built with Streamlit framework

---
Made with ❤️ for NBA fans