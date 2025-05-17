# Slime Volleyball AI Implementation

This project Minimax and Alpha-Beta pruning algorithms for the Slime Volleyball game environment. The implementation includes:

1. A custom Slime Volleyball game environment
2. Minimax algorithm implementation
3. Evaluation function for game states
4. Video recording of gameplay

## Requirements

- Python 3.8+
- Required packages (install using `pip install -r requirements.txt`):
  - numpy
  - pygame
  - opencv-python
  - moviepy

## Project Structure

- `slime_volleyball.py`: Game environment implementation
- `algorithms.py`: Minimax and Alpha-Beta pruning implementations
- `main.py`: Main game loop and AI vs AI gameplay
- `requirements.txt`: Project dependencies

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the game:

```bash
python main.py
```

## Features

- Real-time visualization of the game
- Automatic video recording of gameplay
- Configurable AI parameters (search depth, evaluation weights)
- Score tracking and game reset

## Evaluation Function

The evaluation function considers:

1. Distance to the ball (40% weight)
2. Ball velocity and direction (30% weight)
3. Ball height (30% weight)

## Results

The implementation demonstrates:

1. Alpha-Beta pruning's efficiency over Minimax
2. Strategic gameplay between AI agents
3. Real-time decision making
4. Smooth gameplay visualization

## Video Recording

The game automatically records gameplay to `slime_volleyball_gameplay.mp4`. This video can be used for presentation and analysis of the AI's performance.
