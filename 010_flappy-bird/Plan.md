# Implementation Plan - Task 010: Flappy Bird

Create a functional Flappy Bird clone using the `pygame` library.

## Proposed Changes

### [010_flappy-bird]

#### [NEW] [main.py](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/010_flappy-bird/main.py)
The main game script containing:
- Game loop and event handling.
- `Bird` class with gravity and jump physics.
- `Pipe` class for obstacles and movement.
- Score tracking and UI rendering.

#### [NEW] [requirements.txt](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/010_flappy-bird/requirements.txt)
- `pygame-ce` (recommended over standard pygame for performance and features).

### Features

#### Scrolling Clouds
- **Clouds**: Semi-transparent or white rectangles/ellipses moving slowly in the background.
- **Parallax**: Clouds should move slower than pipes to create a sense of depth.
- **Spawning**: Random heights and intervals.

#### Collectible Coins
- **Coins**: Small yellow circles that appear randomly.
- **Spawning**: Coins will spawn at regular intervals, often between pipes.
- **Interaction**: If the bird overlaps with a coin, the coin vanishes and the score increases by 1.

#### Difficulty Selection
- **States**: `START`, `PLAYING`, `GAMEOVER`.
- **Difficulty Levels**:
    - **Easy**: Larger pipe gap, slower pipe speed, lower pipe frequency.
    - **Medium**: Balanced values (current defaults).
    - **Hard**: Narrower gap, faster pipes, higher gravity.
- **UI**: A simple menu on startup where the user clicks or presses a key (1, 2, 3) to choose.

#### Sound Effects
- **Assets**: A script will generate simple synthetic sounds (`flap.wav`, `score.wav`, `crash.wav`, `select.wav`) using `numpy` and `scipy.io.wavfile`.
- **Integration**:
    - **Flap**: Play whenever the `SPACE` bar is pressed.
    - **Score**: Play when a pipe is passed or a coin is collected.
    - **Crash**: Play on collision.
    - **Select**: Play when a difficulty level is chosen on the menu.

#### Background Music
- **Assets**: Generate a longer loopable wave file (`music.wav`) with a simple upbeat rhythm/melody.
- **Integration**:
    - Start music when the game launches.
    - Loop indefinitely.
    - Lower volume to ensure SFX are audible.

#### Bird and Coin Visuals
- **Assets**:
    - **Bird**: Using `bird.png` (generated icon).
    - **Coin**: Using Pygame's `draw.circle` but with improved details (border, shine).
- **Integration**:
    - Load `bird.png` in `main.py`.
    - Scale it to `BIRD_SIZE`.
    - Rotate the bird image based on vertical velocity.
    - Improve the `Coin.draw()` method for a more "iconic" look.

## Game Mechanics
- **Physics**: Vertical velocity incremented by gravity, decremented by jump event.
- **Pipes**: Spawn at regular intervals with randomized gap positions.
- **Collision**: Screen boundaries and Pipe rectangles.
- **Scoring**: Increments when passing a pipe.

## Verification Plan

### Automated Tests
- N/A (Manual playtesting is more effective for game feel).

### Manual Verification
- Run `python3 main.py` and verify:
    - Bird jumps on spacebar.
    - Gravity pulls bird down.
    - Pipes move left and respawn.
    - Collision with pipes or ground triggers Game Over.
    - Scoring works correctly.
    - Restarting after Game Over works.