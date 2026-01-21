# README - 011_flappy-bird-refactored

## Changes Made
- **Extracted `GameObject` base class**: Created a foundation for all game entities to share common logic for positioning, movement, and off-screen detection.
- **Refactored `Bird`, `Pipe`, `Cloud`, and `Coin`**:
    - Each class now inherits from `GameObject`.
    - Removed redundant `update` and `is_off_screen` implementations.
    - Unified bird movement under the standard `update` method.
- **Improved Code Maintainability**: Centralizing the movement logic makes it easier to change global behavior in the future.

## Verification Results
- **Launch Check**: The game launches and loads assets correctly.
- **Physics Check**: Bird jumping and gravity work as before.
- **Entity Movement**: Pipes, coins, and clouds move across the screen correctly.
- **Collision Detection**: Collisions with pipes and collection of coins are functioning.
- **Off-screen Cleanup**: Objects are correctly removed when they leave the screen side.
