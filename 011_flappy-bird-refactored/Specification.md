# Project Specification: Vibe Flappy Bird

This document defines the requirements, features, and technical architecture for a polished Flappy Bird clone. It is designed to be used as a source of truth for AI coding agents to recreate or extend the game.

## 1. Project Overview
- **Objective**: Create a functional and visually appealing Flappy Bird game.
- **Technology Stack**: Python 3.12, `pygame-ce` (Community Edition).
- **Primary OS**: macOS (cross-platform compatible).

## 2. Feature Specification

### 2.1 Core Gameplay
- **Physics**: Vertical movement controlled by gravity and user "flaps". The bird should rotate upward when jumping and downward when falling.
- **Pipes**: Procedurally generated obstacles with random gap heights.
- **Scoring**: Incremental score based on passing pipes and collecting items.
- **Collisions**: Game ends upon hitting pipes or screen boundaries.

### 2.2 Visual Elements
- **Bird**: Animated sprite using `bird.png`, rotating based on vertical velocity.
- **Clouds**: Procedural, semi-transparent background clouds with parallax scrolling (slower than foreground elements).
- **Coins**: Collectible gold coins with a border and "shine" effect.
- **Theme**: Sky blue background with high-contrast UI elements.

### 2.3 Audio System
- **Background Music**: Loopable track (`music.wav`) played at a low volume.
- **Sound Effects (SFX)**:
    - `flap.wav`: Triggered on jump.
    - `score.wav`: Triggered on passing pipes or collecting coins.
    - `crash.wav`: Triggered on collision/game over.
    - `select.wav`: Triggered during menu interaction.

### 2.4 Difficulty System
Three distinct modes selectable at the start screen:

| Parameter | Easy | Medium | Hard |
| :--- | :--- | :--- | :--- |
| Gravity | 0.2 | 0.25 | 0.3 |
| Flap Strength | -5.5 | -6.5 | -7.5 |
| Pipe Gap | 180px | 150px | 120px |
| Pipe Speed | 2 | 3 | 4 |
| Pipe Frequency | 2000ms | 1500ms | 1200ms |
| Coin Frequency | 2500ms | 3000ms | 4000ms |

## 3. Technical Architecture

### 3.1 State Management
- `STATE_START`: Main menu showing title and difficulty options (keys 1, 2, 3).
- `STATE_PLAYING`: Active gameplay loop.
- `STATE_GAMEOVER`: End screen showing final score and restart options.

### 3.2 Class Definitions
- `Bird`: Properties for `rect`, `velocity`, and `angle`. Methods for `jump()`, `apply_gravity()`, and `draw()`.
- `Pipe`: Properties for `top_rect`, `bottom_rect`, and `passed` flag. Methods for `update()`, `draw()`, and `is_off_screen()`.
- `Cloud`: Properties for `rect`, `speed` (randomized for parallax). Methods for `update()`, `draw()`, and `is_off_screen()`.
- `Coin`: Properties for `rect`, `speed` (matches pipes). Methods for `update()`, `draw()`, and `is_off_screen()`.

## 4. Prompt Summary
To recreate this game, use the following logical sequence of prompts:

1. **Base Game**: "Create a basic Flappy Bird clone in Pygame with a Bird class (gravity/jump), Pipe class (moving left), and score tracking."
2. **Visuals & Parallax**: "Add procedural bubbly clouds to the background that move slower than the pipes. Scale and rotate the bird sprite based on its velocity."
3. **Collectibles**: "Implement collectible gold coins that spawn between pipes and increase the score when touched."
4. **Difficulty Selection**: "Create a start menu with Easy, Medium, and Hard modes. Adjust gravity, pipe gaps, and speeds based on the selection (1, 2, or 3)."
5. **Polished Audio**: "Integrate background music and SFX for flapping, scoring, crashing, and menu selection."

## 5. Directory Structure
```text
010_flappy-bird/
├── assets/
│   ├── bird.png
│   ├── crash.wav
│   ├── flap.wav
│   ├── music.wav
│   ├── score.wav
│   └── select.wav
├── main.py
├── Plan.md
├── README.md
├── requirements.txt
└── Specification.md
```
